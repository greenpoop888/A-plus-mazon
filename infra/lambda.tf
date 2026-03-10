data "aws_caller_identity" "current" {}

data "archive_file" "pos_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_code/pos"
  output_path = "${path.module}/lambda_code/pos-${random_id.id.hex}.zip"
}

data "archive_file" "report_dispatcher_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_code/report_dispatcher"
  output_path = "${path.module}/lambda_code/report_dispatcher-${random_id.id.hex}.zip"
}

data "archive_file" "report_generator_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_code/report_generator"
  output_path = "${path.module}/lambda_code/report_generator-${random_id.id.hex}.zip"
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
  filename         = data.archive_file.pos_zip.output_path
  function_name    = "InventoryService-${random_id.id.hex}"
  
  role             = aws_iam_role.lab_role.arn
  
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  timeout          = 15 
  memory_size      = 128

  source_code_hash = data.archive_file.pos_zip.output_base64sha256

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

resource "aws_lambda_function" "report_dispatcher" {
  filename      = data.archive_file.report_dispatcher_zip.output_path
  function_name = "report-dispatcher"
  role          = aws_iam_role.lab_role.arn
  handler       = "report_dispatcher.handler"
  runtime       = "python3.11"
  timeout       = 60
  layers = [aws_lambda_layer_version.python_libs.arn]
  source_code_hash = data.archive_file.pos_zip.output_base64sha256

  vpc_config {
    subnet_ids         = data.aws_subnets.default.ids
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = {
      DB_HOST   = aws_db_instance.postgres.address
      DB_NAME   = aws_db_instance.postgres.db_name
      DB_PASSWORD = var.db_password
      SQS_URL   = aws_sqs_queue.report_queue.id
    }
  }
}

resource "aws_lambda_function" "worker" {
  filename      = data.archive_file.report_generator_zip.output_path
  function_name = "report-worker"
  role          = aws_iam_role.lab_role.arn
  handler       = "report_generator.handler"
  runtime       = "python3.11"
  timeout       = 300 
  layers = [aws_lambda_layer_version.python_libs.arn]
  source_code_hash = data.archive_file.pos_zip.output_base64sha256

  vpc_config {
    subnet_ids         = data.aws_subnets.default.ids
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = {
      DB_HOST       = aws_db_instance.postgres.address
      DB_NAME   = aws_db_instance.postgres.db_name
      DB_PASSWORD = var.db_password
      REPORT_BUCKET = aws_s3_bucket.reports.id
    }
  }
}

resource "aws_lambda_layer_version" "python_libs" {
  filename   = "${path.module}/lambda_code/report_layer.zip"
  layer_name = "report_generator_libs"
  compatible_runtimes = ["python3.11"]
}