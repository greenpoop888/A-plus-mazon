data "aws_caller_identity" "current" {}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_code"
  output_path = "${path.module}/lambda_function-${random_id.id.hex}.zip"
}

resource "aws_security_group" "lambda_sg" {
  name        = "inventory-lambda-sg-${random_id.id.hex}"
  description = "Security group for inventory lambda to access RDS"
  vpc_id      = data.aws_vpc.default.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "inventory-lambda-sg"
  }
}

resource "aws_lambda_function" "inventory_api" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "InventoryService-${random_id.id.hex}"
  
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"
  
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  timeout          = 15 
  memory_size      = 128

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  vpc_config {
    subnet_ids         = data.aws_subnets.default.ids
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = {
      DB_HOST     = aws_db_instance.postgres.address
      DB_NAME     = aws_db_instance.postgres.db_name
      DB_USER     = aws_db_instance.postgres.username
      DB_PASSWORD = var.db_password
    }
  }
}

output "lambda_function_name" {
  value = aws_lambda_function.inventory_api.function_name
}