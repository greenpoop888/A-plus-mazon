# Infrastructure Terraform Configuration

Using Terraform for AWS infrastructure set up.

## Resources Created

- **EC2 Instance**: Amazon Linux 2023 AMI 2023.10.20260105.0 x86_64 HVM kernel-6.1
- **S3 Bucket**: Stores produc images for public access
- **Security Group**: Allows HTTP (port 80) for web portal, HTTP (port 8000) for backend api development and SSH (port 22) access
- **Elastic IP**: Set up fixed public IP, associated EC2 instance with it for permanent public IP address.

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
- EC2 instance ID and public IP/DNS
- S3 bucket ID, name, domain name and arn
- Elastic IP for EC2