
output "lambda_function_arn" {
  description = "ARN of the access key rotator Lambda function"
  value       = module.access_key_rotator.lambda_function_arn
}

output "lambda_function_name" {
  description = "Name of the access key rotator Lambda function"
  value       = module.access_key_rotator.lambda_function_name
}

output "cloudwatch_event_rule_arn" {
  description = "ARN of the CloudWatch Event Rule"
  value       = module.access_key_rotator.cloudwatch_event_rule_arn
}

output "iam_role_arn" {
  description = "ARN of the IAM role used by the Lambda function"
  value       = module.access_key_rotator.iam_role_arn
}

output "iam_role_name" {
  description = "Name of the IAM role used by the Lambda function"
  value       = module.access_key_rotator.iam_role_name
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = module.access_key_rotator.cloudwatch_log_group_name
}
