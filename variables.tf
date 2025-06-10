variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "max_key_age_days" {
  description = "Maximum age of access keys in days before they are disabled"
  type        = number
  default     = 90
}

variable "schedule_expression" {
  description = "CloudWatch Events schedule expression for running the rotator"
  type        = string
  default     = "rate(1 day)"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Project = "access-key-rotator"
  }
}
