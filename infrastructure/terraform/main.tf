provider "aws" {
  region                   = var.aws_region
  shared_credentials_files = ["./credentials/aws_learnerlab_credentials"]
  profile                  = "awslearnerlab"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["*ubuntu-*24.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  filter {
    name   = "state"
    values = ["available"]
  }
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    description = "SSH from anywhere"
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
    Name = "allow_ssh"
  }
}

resource "aws_security_group" "allow_http_s" {
  name        = "allow_http_s"
  description = "Allow HTTP/S inbound traffic"

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
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
    Name = "allow_http_s"
  }
}

# Instance API
resource "aws_instance" "api_instance" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.api_instance_type
  key_name               = "vockey"
  vpc_security_group_ids = [aws_security_group.allow_ssh.id, aws_security_group.allow_http_s.id]

  tags = {
    Name = "API_Instance"
  }
}

# Instance Training
resource "aws_instance" "training_instance" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.training_instance_type
  key_name               = "vockey"
  vpc_security_group_ids = [aws_security_group.allow_ssh.id]

  tags = {
    Name = "Training_Instance"
  }
}

output "api_public_ip" {
  description = "Public IP de l'instance API"
  value       = aws_instance.api_instance.public_ip
}

output "training_public_ip" {
  description = "Public IP de l'instance Training"
  value       = aws_instance.training_instance.public_ip
}
