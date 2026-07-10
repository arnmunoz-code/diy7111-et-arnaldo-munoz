terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

resource "aws_security_group" "amg_sg" {
  name        = "${var.proyecto}-sg"
  description = "Permite HTTP 80 y SSH 22"

  ingress {
    description = "HTTP publico"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.proyecto}-sg"
  }
}

resource "aws_instance" "amg_ec2" {
  ami                    = data.aws_ssm_parameter.al2023.value
  instance_type          = var.tipo_instancia
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.amg_sg.id]
  user_data              = file("${path.module}/user_data.sh")

  tags = {
    Name = "${var.proyecto}-ec2"
  }
}