#!/bin/bash
# Main Entry Script: Infrastructure Setup, Shared Tasks, & Orchestration
set -e

# Path setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "--- STEP 1: AWS Configuration ---"
aws configure

echo "--- STEP 2: Infrastructure Management (Terraform) ---"
cd "$PROJECT_ROOT/infra"
terraform init

echo "Please enter your Database Password:"
read -r DB_PASSWORD

terraform plan -out=tfplan -detailed-exitcode -input=false -var="db_password=$DB_PASSWORD" || PLAN_STATUS=$?
PLAN_STATUS=${PLAN_STATUS:-0}

if [ $PLAN_STATUS -eq 2 ]; then
    echo "Applying infrastructure changes..."
    terraform apply -auto-approve tfplan
fi

echo "--- STEP 3: Retrieving Shared Resource Information ---"
CLIENT_SITE_IP=$(terraform output -raw client_ec2_ip)
RDS_ENDPOINT=$(terraform output -raw rds_endpoint)
USER_POOL_ID=$(terraform output -raw user_pool_id)
CLIENT_ID=$(terraform output -raw user_pool_client_id)
S3_DOMAIN=$(terraform output -raw s3_bucket_domain_name)
S3_BUCKET_NAME=$(terraform output -raw s3_bucket_name)
MANAGEMENT_SITE_IP=$(terraform output -raw management_ec2_ip)
AWS_REGION=$(terraform output -raw aws_region)

# Shared Variables
S3_BUCKET_URL="${S3_DOMAIN}/"
DB_URL="postgresql://dbadmin:${DB_PASSWORD}@${RDS_ENDPOINT}/grocery"

echo "--- STEP 4: Shared SSH Key Setup ---"
echo "Enter your .pem key path (e.g., ../vockey.pem): "
read -r INPUT_PATH
if [ -f "$INPUT_PATH" ]; then
    KEY_DIR=$(dirname "$INPUT_PATH")
    KEY_NAME=$(basename "$INPUT_PATH")
    ABS_KEY_DIR=$(cd "$KEY_DIR" && pwd)
    SSH_KEY="$ABS_KEY_DIR/$KEY_NAME"
    chmod 600 "$SSH_KEY"
else
    echo "ERROR: Key not found!" && exit 1
fi

echo "--- STEP 5: Shared S3 Image Sync ---"
cd "$PROJECT_ROOT"
if [ -d "./s3_images" ]; then
    aws s3 sync ./s3_images "s3://$S3_BUCKET_NAME" --acl public-read
fi

# --- STEP 6: Execute Deployment Workers ---
chmod +x "$SCRIPT_DIR/deploy_ec2.sh"

echo "--- STEP 6.1: Deploying Client Site ---"
# Passing backend folder ($9) and frontend folder ($10)
"$SCRIPT_DIR/deploy_ec2.sh" \
    "grocery-client-server" \
    "$PROJECT_ROOT/server" \
    "$CLIENT_SITE_IP" \
    "$RDS_ENDPOINT" \
    "$USER_POOL_ID" \
    "$CLIENT_ID" \
    "$S3_BUCKET_URL" \
    "$DB_PASSWORD" \
    "$SSH_KEY" \
    "$PROJECT_ROOT/client" \
    "$AWS_REGION"

echo "--- STEP 6.2: Running Database Seed (Run Once via Client Site) ---"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "ec2-user@$CLIENT_SITE_IP" << EOF
    cd "/home/ec2-user/project/grocery-client-server"
    source venv/bin/activate
    python3 -m src.seeds.database
    python3 -m src.seeds.seed_data
EOF

echo "--- STEP 6.3: Deploying Management Site ---"
"$SCRIPT_DIR/deploy_ec2.sh" \
    "grocery-mgmt-server" \
    "$PROJECT_ROOT/management_server" \
    "$MANAGEMENT_SITE_IP" \
    "$RDS_ENDPOINT" \
    "$USER_POOL_ID" \
    "$CLIENT_ID" \
    "$S3_BUCKET_URL" \
    "$DB_PASSWORD" \
    "$SSH_KEY" \
    "$PROJECT_ROOT/management_web" \
    "$AWS_REGION"

echo "--- ALL TASKS COMPLETE ---"