# Access Key Rotator Module
module "access_key_rotator" {
  source = "./modules/access-key-rotator"

  function_name        = "access-key-rotator"
  max_key_age_days     = var.max_key_age_days
  schedule_expression  = var.schedule_expression
  lambda_timeout       = 300
  log_retention_days   = 14

  tags = var.tags
}
