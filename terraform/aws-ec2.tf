provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for the deployment"
  type        = string
  default     = "ap-south-1"
}

variable "app_image" {
  description = "Docker image to deploy"
  type        = string
  default     = "josesamuel14/multicloud-app:latest"
}

variable "ssh_cidr" {
  description = "CIDR block allowed to access SSH"
  type        = string
}

resource "aws_security_group" "multicloud_sg" {
  name        = "multicloud-cicd-sg"
  description = "Allow application traffic and controlled SSH access"

  # SSH access - must be explicitly provided during deployment
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  # Flask application
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "multicloud-cicd-sg"
    Project = "multicloud-cicd"
  }
}

resource "aws_instance" "multicloud_app" {
  ami           = "ami-0f58b397bc5c1f2e8"
  instance_type = "t2.micro"
  key_name      = "multicloud-key"

  vpc_security_group_ids = [
    aws_security_group.multicloud_sg.id
  ]

  user_data = <<-SCRIPT
    #!/bin/bash

    apt-get update -y
    apt-get install -y docker.io

    systemctl start docker
    systemctl enable docker

    docker pull ${var.app_image}

    docker run -d \
      -p 5000:5000 \
      --name multicloud-app \
      --restart unless-stopped \
      -e CLOUD_PROVIDER=aws \
      -e CLOUD_REGION=${var.aws_region} \
      ${var.app_image}
  SCRIPT

  tags = {
    Name    = "multicloud-cicd-app"
    Project = "multicloud-cicd"
    Type    = "ec2"
  }
}

resource "aws_eip" "multicloud_ip" {
  instance = aws_instance.multicloud_app.id
  domain   = "vpc"
}

output "app_url" {
  value       = "http://${aws_eip.multicloud_ip.public_ip}:5000"
  description = "AWS application URL"
}

output "instance_id" {
  value       = aws_instance.multicloud_app.id
  description = "EC2 instance ID"
}

output "public_ip" {
  value       = aws_eip.multicloud_ip.public_ip
  description = "Public IP of the EC2 instance"
}