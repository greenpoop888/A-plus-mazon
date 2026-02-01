output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "ec2_instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "ec2_instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.app_server.public_dns
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket for build artifacts"
  value       = aws_s3_bucket.app_bucket.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.app_bucket.arn
}

output "s3_bucket_id" {
  value = aws_s3_bucket.app_bucket.id
}

output "s3_bucket_domain_name" {
  value = "https://${aws_s3_bucket.app_bucket.bucket_regional_domain_name}"
}

output "eip_ip" {
  description = "The public Elastic IP address assigned to the EC2 instance"
  value       = aws_eip.app_eip.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}