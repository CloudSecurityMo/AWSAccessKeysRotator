variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "access-key-rotator"
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

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 300
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 14
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
