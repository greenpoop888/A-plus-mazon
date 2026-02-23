#!/bin/bash
set -e

# Get the absolute path of the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "--- Cognito User Creation Tool (Temporary Password Mode) ---"

# 1. Automatically retrieve IDs from Terraform
cd "$PROJECT_ROOT/infra"
USER_POOL_ID=$(terraform output -raw user_pool_id)
CLIENT_ID=$(terraform output -raw user_pool_client_id)

echo "Using User Pool: $USER_POOL_ID"

# 2. Get User Info
read -p "Enter new admin email: " ADMIN_EMAIL
read -s -p "Enter temporary password (min 8 chars): " ADMIN_PASSWORD
echo ""

# Simple validation for length
if [ ${#ADMIN_PASSWORD} -lt 8 ]; then
    echo "ERROR: Password must be at least 8 characters long."
    exit 1
fi

# 3. Create the user in Cognito
echo "Creating user in AWS..."
aws cognito-idp admin-create-user \
    --user-pool-id "$USER_POOL_ID" \
    --username "$ADMIN_EMAIL" \
    --user-attributes Name=email,Value="$ADMIN_EMAIL" Name=email_verified,Value=true \
    --message-action SUPPRESS

# 4. Set the password as TEMPORARY
echo "Setting temporary password..."
aws cognito-idp admin-set-user-password \
    --user-pool-id "$USER_POOL_ID" \
    --username "$ADMIN_EMAIL" \
    --password "$ADMIN_PASSWORD"

echo "--- SUCCESS: User $ADMIN_EMAIL created with a temporary password! ---"
echo "The user will be prompted to change their password upon first login."