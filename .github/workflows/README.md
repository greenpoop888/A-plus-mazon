# GITHUB Action CI/CD
Using GitHub Actions workflow for automated full-stack deployment. This template handles building the React frontend, synchronizing it with Nginx, and managing a FastAPI backend using systemd.

## Prerequisites
Before pushing to main, ensure your EC2 instance is prepared:

Configure GitHub Secrets:
- EC2_HOST: Your EC2 Public IP(in this project, Elastic IP for permanent public IP).
- EC2_USER: The SSH username (e.g., ec2-user).
- EC2_SSH_KEY: Your private .pem key.

SSH Access:
Ensure your EC2 has an SSH Deploy Key added to GitHub to allow git clone.

## Deployment Logic
This project utilizes GitHub Actions to:
 1. Build the frontend assets in the cloud.
 2. Sync static files to the Nginx web root.
 3. Pull or Clone the latest Python code directly on the EC2 via git reset --hard.
 4. Auto-Configuration: If the systemd service is not found on the EC2, the workflow will automatically:
    - Create a new .service configuration file.
    - Enable the service to auto-start on system boot.
    - Start the service immediately.
 5. Restart: If the service already exists, it triggers a restart to apply code changes.