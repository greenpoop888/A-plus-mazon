resource "aws_iam_role" "lab_role" {
  name = "LabRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = [
          "lambda.amazonaws.com",
          "ec2.amazonaws.com"
        ]
      }
    }]
  })
}

resource "aws_iam_instance_profile" "lab_instance_profile" {
  name = "LabInstanceProfile"
  role = aws_iam_role.lab_role.name
}

resource "aws_iam_role_policy" "lab_combined_policy" {
  name = "LabCombinedPolicy"
  role = aws_iam_role.lab_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:*"]
        Resource = ["*"]
      },
      {
        Effect   = "Allow"
        Action   = ["sqs:*"]
        Resource = ["*"]
      },
      {
        Effect   = "Allow"
        Action   = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface"
        ]
        Resource = ["*"]
      },
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = ["*"]
      }
    ]
  })
}