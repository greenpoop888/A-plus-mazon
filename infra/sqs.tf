resource "aws_sqs_queue" "report_queue" {
  name                        = "report-task-queue"
  visibility_timeout_seconds  = 300
  message_retention_seconds   = 86400
}

resource "aws_vpc_endpoint" "sqs" {
  vpc_id              = data.aws_vpc.default.id
  service_name        = "com.amazonaws.us-east-1.sqs"
  vpc_endpoint_type   = "Interface"
  
  subnet_ids          = data.aws_subnets.default.ids
  security_group_ids  = [aws_security_group.vpc_endpoint_sg.id]
  private_dns_enabled = true
}

resource "aws_security_group" "vpc_endpoint_sg" {
  name        = "vpc-endpoint-sg"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
  }
}