resource "aws_security_group" "rds_sg" {
  name        = "grocery-rds-sg-${random_id.id.hex}"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "ecommerce-db-subnet-group"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_db_instance" "postgres" {
  identifier             = "grocery-db-instance-${random_id.id.hex}"
  allocated_storage      = 20
  max_allocated_storage  = 100
  engine                 = "postgres"
  engine_version         = "18.1"
  instance_class         = "db.t3.micro"
  
  db_name                = "grocery"
  username               = "dbadmin"
  password               = var.db_password
  
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  
  storage_type           = "gp3"
  publicly_accessible    = false
  skip_final_snapshot    = true
  multi_az               = false
}