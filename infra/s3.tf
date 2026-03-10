resource "random_id" "id" {
  byte_length = 4
}

resource "aws_s3_bucket" "app_bucket" {
  bucket        = "${var.s3_bucket_name}-${random_id.id.hex}"
  force_destroy = true
  tags = {
    Name        = var.s3_bucket_name
    Environment = var.s3_environment
  }
}

resource "aws_s3_bucket_ownership_controls" "app_bucket_ownership" {
  bucket = aws_s3_bucket.app_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "app_bucket_block" {
  bucket = aws_s3_bucket.app_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "app_bucket_public_policy" {
  depends_on = [aws_s3_bucket_public_access_block.app_bucket_block]
  bucket     = aws_s3_bucket.app_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowLabRoleFullAccess"
        Effect    = "Allow"
        Principal = { AWS = aws_iam_role.lab_role.arn }
        Action    = ["s3:*"]
        Resource  = [
          "${aws_s3_bucket.app_bucket.arn}",
          "${aws_s3_bucket.app_bucket.arn}/*"
        ]
      },
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.app_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_s3_bucket_cors_configuration" "app_bucket_cors" {
  bucket = aws_s3_bucket.app_bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = []
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket" "reports" {
  bucket = "voc-grocery-reports-${random_id.id.hex}"
  force_destroy = true
}

data "aws_route_table" "selected" {
  vpc_id = data.aws_vpc.default.id
  filter {
    name   = "association.main"
    values = ["true"]
  }
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = [data.aws_route_table.selected.id]
}

resource "aws_s3_bucket_policy" "allow_role_access" {
  bucket = aws_s3_bucket.reports.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowRoleGetObject"
        Effect    = "Allow"
        Principal = {
          AWS = aws_iam_role.lab_role.arn
        }
        Action   = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "${aws_s3_bucket.reports.arn}",
          "${aws_s3_bucket.reports.arn}/*"
        ]
      }
    ]
  })
}


resource "aws_s3_bucket_cors_configuration" "report_cors" {
  bucket = aws_s3_bucket.reports.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"] 
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}