#!/bin/bash
set -e

echo "--- STEP 1: AWS Configuration ---"
echo "Please enter your AWS CLI credentials to proceed:"
aws configure

echo "--- STEP 2: Infrastructure Management (Terraform) ---"
echo "Navigating to infra directory..."
cd infra 

echo "Initializing Terraform..."
terraform init

echo "Please enter your Database Password:"
read -r DB_PASSWORD

echo "Running terraform plan..."
# Capture exit code: 0=no changes, 2=changes, 1=error
terraform plan -out=tfplan -detailed-exitcode -input=false -var="db_password=$DB_PASSWORD" || PLAN_STATUS=$?
PLAN_STATUS=${PLAN_STATUS:-0}

echo "Terraform plan finished with status: $PLAN_STATUS"

if [ $PLAN_STATUS -eq 2 ]; then
    echo "Infrastructure changes detected. Applying Terraform..."
    terraform apply -auto-approve tfplan
elif [ $PLAN_STATUS -eq 0 ]; then
    echo "No infrastructure changes detected. Skipping apply..."
else
    echo "ERROR: Terraform plan failed with error code $PLAN_STATUS"
    exit 1
fi

echo "--- STEP 3: Retrieving Resource Information ---"
EC2_HOST=$(terraform output -raw client_ec2_public_ip)
RDS_ENDPOINT=$(terraform output -raw rds_endpoint)
USER_POOL_ID=$(terraform output -raw user_pool_id)
CLIENT_ID=$(terraform output -raw user_pool_client_id)

# Configuration variables
EC2_USER="ec2-user"
PROJECT_ROOT="/home/ec2-user/project/server"
DB_URL="postgresql://dbadmin:${DB_PASSWORD}@${RDS_ENDPOINT}/grocery" 

cd .. 

TEMP_KEY_RAW="$(pwd)/.deploy_key_raw.pem"
TEMP_KEY_CLEAN="$(pwd)/.deploy_key.pem"

echo "--- STEP 3: SSH Key Setup ---"
echo "Enter your ssh key file (.pem) path (e.g., ./vockey.pem): "
read -r INPUT_PATH

# Check if the file exists at the input path
if [ -f "$INPUT_PATH" ]; then
    # Get the directory and filename separately to reconstruct an absolute path
    KEY_DIR=$(dirname "$INPUT_PATH")
    KEY_NAME=$(basename "$INPUT_PATH")
    
    # Use 'cd' to resolve the absolute directory path, then attach the filename
    ABS_KEY_DIR=$(cd "$KEY_DIR" && pwd)
    SSH_KEY="$ABS_KEY_DIR/$KEY_NAME"
else
    echo "ERROR: File not found at the path you entered: $INPUT_PATH"
    exit 1
fi

echo "Successfully resolved absolute path: $SSH_KEY"
chmod 600 "$SSH_KEY"

echo "Cleaned SSH key prepared successfully."

echo "--- STEP 4: Backend Packaging and Transfer ---"
echo "Target EC2 Host: $EC2_HOST"

echo "Creating backend archive (excluding venv and cache)..."
tar -czf backend.tar.gz \
    --exclude='venv' \
    --exclude='.env' \
    --exclude='__pycache__' \
    -C ./server .

echo "Creating remote project directory..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" "mkdir -p $PROJECT_ROOT"

echo "Uploading backend.tar.gz to EC2..."
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no backend.tar.gz "$EC2_USER@$EC2_HOST:$PROJECT_ROOT/"

echo "Extracting backend archive on EC2..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" << EOF
    echo "Remote: Extracting files in $PROJECT_ROOT"
    cd "$PROJECT_ROOT"
    tar -xzf backend.tar.gz
    rm backend.tar.gz
EOF

echo "Cleaning up local archive..."
rm backend.tar.gz

echo "--- STEP 5: Remote Backend Environment Setup ---"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" << EOF
    set -e
    
    # Re-declare variables inside the remote shell
    REMOTE_PROJECT_ROOT="$PROJECT_ROOT"
    
    echo "Remote: Checking for Python 3.11..."
    if ! command -v python3.11 &> /dev/null; then
        echo "Remote: Installing Python 3.11..."
        sudo yum update -y
        sudo yum install -y python3.11 python3.11-devel python3.11-pip
    fi

    echo "Remote: Navigating to \$REMOTE_PROJECT_ROOT"
    cd "\$REMOTE_PROJECT_ROOT"

    echo "Remote: Injecting environment variables into .env"
    echo "DATABASE_URL=$DB_URL" > .env
    echo "COGNITO_USER_POOL_ID=$USER_POOL_ID" >> .env
    echo "COGNITO_CLIENT_ID=$CLIENT_ID" >> .env

    echo "Remote: Setting up Virtual Environment..."
    if [ ! -d "venv" ]; then
        python3.11 -m venv venv
    fi

    echo "Remote: Installing Python dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "ERROR: requirements.txt not found!"
        exit 1
    fi

    echo "Remote: Running database migrations and seeding..."
    python3 -m src.seeds.database
    python3 -m src.seeds.seed_data

    echo "Remote: Configuring Systemd Service..."
    SERVICE_CONTENT="[Unit]
Description=My FastAPI Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=\$REMOTE_PROJECT_ROOT
ExecStart=\$REMOTE_PROJECT_ROOT/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target"

    echo "\$SERVICE_CONTENT" | sudo tee /etc/systemd/system/myproject.service > /dev/null
    
    echo "Remote: Starting myproject.service..."
    sudo systemctl daemon-reload
    sudo systemctl enable myproject.service
    sudo systemctl restart myproject.service
EOF

echo "--- STEP 6: Frontend Build and Deployment ---"
echo "Navigating to client directory..."
cd client

echo "Configuring frontend environment variables..."
echo "REACT_APP_USER_POOL_ID=$USER_POOL_ID" > .env
echo "REACT_APP_CLIENT_ID=$CLIENT_ID" >> .env

echo "Running npm install and build..."
npm install
CI=false npm run build

echo "Creating remote frontend build directory..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" "mkdir -p ~/frontend_build"

echo "Uploading frontend build artifacts..."
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -r build/* "$EC2_USER@$EC2_HOST:~/frontend_build/"

echo "Configuring Nginx on EC2..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" << EOF
    set -e
    if ! command -v nginx &> /dev/null; then
        echo "Remote: Installing Nginx..."
        sudo yum install -y nginx
        sudo systemctl enable nginx
        sudo systemctl start nginx
    fi

    echo "Remote: Deploying build files to /var/www/react"
    sudo mkdir -p /var/www/react
    sudo rm -rf /var/www/react/*
    sudo cp -r ~/frontend_build/* /var/www/react/
    rm -rf ~/frontend_build
    
    echo "Remote: Updating Nginx configuration..."
    sudo cp "$PROJECT_ROOT/nginx.conf" /etc/nginx/conf.d/grocery.conf
    sudo nginx -t && sudo systemctl restart nginx
EOF

echo "--- DEPLOYMENT SUCCESSFUL ---"
echo "Your application is now running and accessible."