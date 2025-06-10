
# AWS Access Key Rotator

This Terraform project creates an automated AWS Access Key rotator that disables access keys older than 90 days (configurable).

## Features

- **Automated Rotation**: Runs on a configurable schedule (daily by default)
- **Configurable Age Threshold**: Set the maximum age for access keys before they're disabled
- **Comprehensive Logging**: CloudWatch logs for monitoring and troubleshooting
- **Safe Operation**: Only disables keys, doesn't delete them
- **Detailed Reporting**: Logs information about disabled keys including last usage
- **Modular Design**: Reusable Terraform module for easy deployment across environments

## Architecture

- **Lambda Function**: Python function that checks and disables old access keys
- **CloudWatch Events**: Triggers the Lambda function on a schedule
- **IAM Role & Policy**: Minimal permissions for the Lambda to perform its tasks
- **CloudWatch Logs**: Stores execution logs for monitoring

## Project Structure

```
.
├── backend.tf                           # Terraform backend configuration
├── provider.tf                          # AWS provider configuration
├── variables.tf                         # Root-level variables
├── main.tf                              # Module instantiation
├── outputs.tf                           # Root-level outputs
├── terraform.tfvars.example             # Example configuration
├── README.md                            # This file
└── modules/
    └── access-key-rotator/
        ├── main.tf                      # Module resources
        ├── variables.tf                 # Module variables
        ├── outputs.tf                   # Module outputs
        └── lambda_function.py           # Lambda function code
```

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Terraform Cloud/S3 backend (update `backend.tf`)

## Deployment

1. **Configure Backend**: Update `backend.tf` with your S3/Terraform Cloud details
2. **Set Variables**: Copy `terraform.tfvars.example` to `terraform.tfvars` and customize
3. **Deploy**:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

## Configuration

### Root Variables

- `aws_region`: AWS region to deploy resources (default: eu-west-1)
- `max_key_age_days`: Maximum age of access keys before disabling (default: 90)
- `schedule_expression`: CloudWatch Events schedule (default: "rate(1 day)")
- `tags`: Tags to apply to all resources

### Module Variables

The module accepts additional configuration options:
- `function_name`: Name of the Lambda function
- `lambda_timeout`: Function timeout in seconds
- `log_retention_days`: CloudWatch log retention period

### Schedule Examples

- `"rate(1 day)"` - Run daily
- `"rate(12 hours)"` - Run every 12 hours  
- `"cron(0 9 * * ? *)"` - Run daily at 9 AM UTC
- `"cron(0 9 ? * MON *)"` - Run every Monday at 9 AM UTC

## Using the Module

You can use this module in other Terraform configurations:

```hcl
module "access_key_rotator" {
  source = "./modules/access-key-rotator"

  function_name        = "my-key-rotator"
  max_key_age_days     = 60
  schedule_expression  = "rate(12 hours)"
  lambda_timeout       = 600
  log_retention_days   = 30

  tags = {
    Environment = "production"
    Team        = "security"
  }
}
```

## Monitoring

- Check CloudWatch Logs: `/aws/lambda/access-key-rotator`
- Lambda function returns detailed information about processed keys
- Logs include:
  - Total keys checked
  - Keys disabled
  - User information
  - Key age and last usage

## Security Considerations

- The Lambda function has minimal IAM permissions
- Keys are disabled, not deleted (can be re-enabled if needed)
- All actions are logged for audit purposes
- Consider setting up CloudWatch alarms for failures

## Manual Testing

You can manually invoke the Lambda function to test:

```bash
aws lambda invoke \
  --function-name access-key-rotator \
  --payload '{}' \
  response.json
```

## Cleanup

To remove all resources:

```bash
terraform destroy
```

## Troubleshooting

1. **Permission Errors**: Ensure the Lambda execution role has the required IAM permissions
2. **No Keys Disabled**: Check the `max_key_age_days` setting and key creation dates
3. **Function Timeout**: Increase the Lambda timeout if you have many users/keys

## Cost Estimation
This solution is very cost-effective:
- Lambda: ~$0.20/month (assuming daily execution)
- CloudWatch Logs: ~$0.50/month (with 14-day retention)
- CloudWatch Events: Free tier covers typical usage

Total estimated cost: < $1/month
