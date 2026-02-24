# Infrastructure Terraform Configuration

Using Terraform for AWS infrastructure set up.

## Resources Created

- **EC2 Instance**: Amazon Linux 2023 AMI
- **S3 Bucket**: Stores produc images for public access
- **Security Group**: Allows HTTP (port 80) for web portal, HTTP (port 8000) for backend api development and SSH (port 22) access
- **RDS**: Set up a RDS with postgre18.1 for permenent data storage.
- **APIGateway**: For POS to gate and grant Api key
- **Lambda**: For POS system apis
- **Cognito**: Set up User pool for login


## Prerequisites

1. AWS CLI configured with appropriate credentials
2. Terraform >= 1.2 installed
3. AWS account with permissions to create EC2, S3, Elatic IPs

## Usage

### Initialize Terraform

```bash
cd infra
terraform init
```

### Validate terraform scripts

```bash
terraform validate
```

### Plan Changes

```bash
terraform plan
```

### Apply Configuration

```bash
terraform apply
```

### Destroy Infrastructure

```bash
terraform destroy
```

## Outputs

After applying, Terraform will output:
- 2 EC2 instance ID and public IP/DNS
- S3 bucket ID, name, domain name and arn
- Elastic IP for EC2
- RDS with postgres
- API router for POS system
- Lambda for POS api
- Cognito for management website's login