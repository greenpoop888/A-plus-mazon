variable "instance_name" {
  description = "Value of the EC2 instance's Name tag."
  type        = string
  default     = "product-service"
}

variable "instance_type" {
  description = "The EC2 instance's type."
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Existing EC2 Key Pair name"
  type        = string
  default     = "vockey"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket_name" {
  description = "S3 bucket name (must be globally unique)"
  type        = string
  default     = "cloud-computing-project-product-images"
}

variable "s3_environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}