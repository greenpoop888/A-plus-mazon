#!/bin/bash
# Reusable Deployment Worker
set -e

# Arguments passed from deploy.sh
SERVICE_NAME=$1
BACKEND_SRC_DIR=$2
EC2_HOST=$3
RDS_ENDPOINT=$4
USER_POOL_ID=$5
CLIENT_ID=$6
S3_BUCKET_URL=$7
DB_PASSWORD=$8
SSH_KEY=$9
FRONTEND_SRC_DIR=${10}

# Config constants
EC2_USER="ec2-user"
PROJECT_REMOTE_ROOT="/home/ec2-user/project/$SERVICE_NAME"
DB_URL="postgresql://dbadmin:${DB_PASSWORD}@${RDS_ENDPOINT}/grocery"

echo "--- [$SERVICE_NAME] Backend Packaging & Transfer ---"
tar -czf "${SERVICE_NAME}_backend.tar.gz" \
    --exclude='venv' --exclude='.env' --exclude='__pycache__' \
    -C "$BACKEND_SRC_DIR" .

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" "mkdir -p $PROJECT_REMOTE_ROOT"
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "${SERVICE_NAME}_backend.tar.gz" "$EC2_USER@$EC2_HOST:$PROJECT_REMOTE_ROOT/"

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" << EOF
    cd "$PROJECT_REMOTE_ROOT"
    tar -xzf "${SERVICE_NAME}_backend.tar.gz"
    rm "${SERVICE_NAME}_backend.tar.gz"
EOF
rm "${SERVICE_NAME}_backend.tar.gz"

echo "--- [$SERVICE_NAME] Remote Environment Setup ---"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" << EOF
    set -e
    REMOTE_ROOT="$PROJECT_REMOTE_ROOT"
    cd "\$REMOTE_ROOT"
    cat << ENV_EOF > .env
DATABASE_URL=$DB_URL
COGNITO_USER_POOL_ID=$USER_POOL_ID
COGNITO_CLIENT_ID=$CLIENT_ID
S3_BUCKET_URL=$S3_BUCKET_URL
ENV_EOF

    if [ ! -d "venv" ]; then python3.11 -m venv venv; fi
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

    SERVICE_CONTENT="[Unit]
Description=$SERVICE_NAME FastAPI Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=\$REMOTE_ROOT
ExecStart=\$REMOTE_ROOT/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target"

    echo "\$SERVICE_CONTENT" | sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_NAME}.service
    sudo systemctl restart ${SERVICE_NAME}.service
EOF

echo "--- [$SERVICE_NAME] Frontend Build & Deployment ---"
# Use the dynamic frontend source directory
cd "$FRONTEND_SRC_DIR"
echo "REACT_APP_USER_POOL_ID=$USER_POOL_ID" > .env
echo "REACT_APP_CLIENT_ID=$CLIENT_ID" >> .env

npm install
CI=false npm run build

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" "mkdir -p ~/frontend_build"
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no -r build/* "$EC2_USER@$EC2_HOST:~/frontend_build/"

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" << EOF
    set -e
    if ! command -v nginx &> /dev/null; then
        sudo yum install -y nginx
        sudo systemctl enable nginx
        sudo systemctl start nginx
    fi
    sudo mkdir -p /var/www/react
    sudo rm -rf /var/www/react/*
    sudo cp -r ~/frontend_build/* /var/www/react/
    rm -rf ~/frontend_build
    
    sudo cp "$PROJECT_REMOTE_ROOT/nginx.conf" /etc/nginx/conf.d/${SERVICE_NAME}.conf
    sudo nginx -t && sudo systemctl restart nginx
EOF