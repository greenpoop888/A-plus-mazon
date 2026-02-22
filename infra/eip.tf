/* resource "aws_eip" "app_eip" {
  instance = aws_instance.app_server.id
  domain   = "vpc"

  tags = {
    Name = "${var.ec2_instance_name}-eip-${random_id.id.hex}"
  }
} */