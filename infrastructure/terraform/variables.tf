variable "aws_region" {
  description = "La région AWS"
  type        = string
  default     = "us-east-1"
}


variable "api_instance_type" {
  description = "Type d'instance pour API"
  type        = string
  default     = "t3.micro"
}

variable "training_instance_type" {
  description = "Type d'instance pour Training"
  type        = string
  default     = "t3.medium"
}
