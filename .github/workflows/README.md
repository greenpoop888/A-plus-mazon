## Prerequisites

Before pushing to the `second_assignment` branch, ensure your AWS environment is configured as follows:

### 1. Configure GitHub Secrets
Navigate to `Settings > Secrets and variables > Actions` and add:
- `EC2_HOST`: Your EC2 Public IP (Elastic IP).
- `EC2_USER`: SSH username (e.g., `ec2-user`).
- `EC2_SSH_KEY`: Your private `.pem` key content.
- `DB_URL`: RDS connection string (`postgresql://user:password@endpoint:5432/grocery`).

---

## Deployment Logic

The workflow executes the following stages in sequence:

1.  **Environment Setup**:
    * Installs Git and Python 3.11 dependencies on the host.
    * Synchronizes code via scp to ensure the project directory matches the repository state.
    * Dynamically generates the .env file for backend database connectivity using GitHub Secrets.
2.  **Database Migrations**:
    * Activates the virtual environment and runs database.py and seed_data.py.
    * Synchronizes the RDS schema and seeds initial data to the PostgreSQL instance.
3.  **Process Management (systemd)**:
    * Generates a `myproject.service` file to ensure the FastAPI app runs as a background daemon.
    * Enables "restart on failure" and "start on boot" policies.
4.  **Frontend Build & Sync**:
    * Compiles React assets in the GitHub cloud environment (`CI=false` to bypass linting warnings).
    * Synchronizes the build folder to the EC2 via `scp`.
    * Fixes directory ownership for the `nginx` user.
5.  **Web Server (Nginx)**:
    * Deploys the project's `nginx.conf` to `/etc/nginx/conf.d/`.
    * Validates configuration syntax before restarting the service to ensure public uptime.

