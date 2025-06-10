output "lambda_function_arn" {
  description = "ARN of the access key rotator Lambda function"
  value       = aws_lambda_function.access_key_rotator.arn
}

output "lambda_function_name" {
  description = "Name of the access key rotator Lambda function"
  value       = aws_lambda_function.access_key_rotator.function_name
}

output "cloudwatch_event_rule_arn" {
  description = "ARN of the CloudWatch Event Rule"
  value       = aws_cloudwatch_event_rule.access_key_rotator_schedule.arn
}

output "iam_role_arn" {
  description = "ARN of the IAM role used by the Lambda function"
  value       = aws_iam_role.lambda_role.arn
}

output "iam_role_name" {
  description = "Name of the IAM role used by the Lambda function"
  value       = aws_iam_role.lambda_role.name
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}
