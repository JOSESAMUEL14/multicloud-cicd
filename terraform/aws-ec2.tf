# ── AWS Provider ──
provider "aws" {
  region = var.aws_region
}

# ── Variables ──
variable "aws_region" {
  default = "ap-south-1"  # Mumbai — closest to India
}

variable "app_image" {
  default = "josesamuel14/multicloud-app:latest"
}

# ── Security Group ──
resource "aws_security_group" "multicloud_sg" {
  name        = "multicloud-cicd-sg"
  description = "Allow HTTP and SSH"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
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
    Name    = "multicloud-cicd-sg"
    Project = "multicloud-cicd"
  }
}

# ── EC2 Instance (Free Tier t2.micro) ──
resource "aws_instance" "multicloud_app" {
  ami           = "ami-0f58b397bc5c1f2e8"  # Ubuntu 22.04 Mumbai
  instance_type = "t2.micro"               # FREE TIER
  key_name      = "multicloud-key"

  vpc_security_group_ids = [aws_security_group.multicloud_sg.id]

  # Auto-install Docker and run app on startup
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
    Type    = "free-tier"
  }
}

# ── Elastic IP (Static IP) ──
resource "aws_eip" "multicloud_ip" {
  instance = aws_instance.multicloud_app.id
  domain   = "vpc"
}

# ── Outputs ──
output "app_url" {
  value       = "http://${aws_eip.multicloud_ip.public_ip}:5000"
  description = "Your app URL on AWS"
}

output "instance_id" {
  value       = aws_instance.multicloud_app.id
  description = "EC2 Instance ID — use this to stop/delete"
}

output "public_ip" {
  value       = aws_eip.multicloud_ip.public_ip
  description = "Public IP of your EC2 instance"
}
