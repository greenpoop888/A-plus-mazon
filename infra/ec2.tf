resource "aws_instance" "app_server" {
  ami           = var.ec2_ami_id
  instance_type = var.ec2_instance_type
  key_name      = var.ec2_key_name

  vpc_security_group_ids = [
    aws_security_group.app_sg.id
  ]

  tags = {
    Name = "${var.ec2_instance_name}-${random_id.id.hex}"
  }

  user_data = <<-EOF
              #!/bin/bash
              dnf update -y
              dnf install -y python3
              EOF
}
