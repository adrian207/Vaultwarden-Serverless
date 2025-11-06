/**
 * AWS Infrastructure Outputs
 * Author: Adrian Johnson <adrian207@gmail.com>
 */

output "vaultwarden_url" {
  description = "Vaultwarden application URL"
  value       = var.enable_cloudfront && length(aws_cloudfront_distribution.vaultwarden) > 0 ? "https://${var.domain_name}" : "https://${module.compute.alb_dns_name}"
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = module.compute.alb_dns_name
}

output "alb_zone_id" {
  description = "Application Load Balancer Zone ID (for Route53 alias)"
  value       = module.compute.alb_zone_id
}

output "database_endpoint" {
  description = "Aurora Serverless cluster endpoint"
  value       = module.database.cluster_endpoint
  sensitive   = true
}

output "database_reader_endpoint" {
  description = "Aurora Serverless cluster reader endpoint"
  value       = module.database.reader_endpoint
  sensitive   = true
}

output "s3_bucket_name" {
  description = "S3 bucket name for attachments"
  value       = module.storage.bucket_name
}

output "s3_bucket_arn" {
  description = "S3 bucket ARN"
  value       = module.storage.bucket_arn
}

output "secrets_manager_arn" {
  description = "Secrets Manager secret ARN"
  value       = aws_secretsmanager_secret.vaultwarden_config.arn
  sensitive   = true
}

output "admin_token" {
  description = "Admin token for accessing /admin panel"
  value       = random_password.admin_token.result
  sensitive   = true
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = module.compute.cluster_name
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = module.compute.service_name
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name"
  value       = aws_cloudwatch_log_group.vaultwarden.name
}

output "backup_vault_name" {
  description = "AWS Backup vault name"
  value       = aws_backup_vault.vaultwarden.name
}

output "waf_web_acl_arn" {
  description = "WAF Web ACL ARN"
  value       = var.enable_waf ? aws_wafv2_web_acl.vaultwarden[0].arn : null
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = var.enable_cloudfront ? aws_cloudfront_distribution.vaultwarden[0].id : null
}

output "cloudfront_domain_name" {
  description = "CloudFront distribution domain name"
  value       = var.enable_cloudfront ? aws_cloudfront_distribution.vaultwarden[0].domain_name : null
}

# DNS Configuration Instructions
output "dns_configuration" {
  description = "DNS configuration instructions"
  value = var.enable_cloudfront ? {
    type   = "CNAME or ALIAS"
    name   = var.domain_name
    value  = aws_cloudfront_distribution.vaultwarden[0].domain_name
    note   = "Point your domain to the CloudFront distribution"
  } : {
    type   = "ALIAS (Route53) or CNAME"
    name   = var.domain_name
    value  = module.compute.alb_dns_name
    zone_id = module.compute.alb_zone_id
    note   = "For Route53, create ALIAS record. Otherwise use CNAME."
  }
}

# Post-Deployment Instructions
output "post_deployment_steps" {
  description = "Steps to complete after deployment"
  value = <<-EOT
    ╔══════════════════════════════════════════════════════════════════╗
    ║          Vaultwarden Deployment Complete!                        ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    🌐 Access URL: ${var.enable_cloudfront && length(aws_cloudfront_distribution.vaultwarden) > 0 ? "https://${var.domain_name}" : "https://${module.compute.alb_dns_name}"}
    
    📋 Next Steps:
    
    1. Configure DNS:
       ${var.enable_cloudfront ? "Create CNAME: ${var.domain_name} → ${try(aws_cloudfront_distribution.vaultwarden[0].domain_name, "pending")}" : "Create ALIAS: ${var.domain_name} → ${module.compute.alb_dns_name}"}
    
    2. Access Admin Panel:
       URL: https://${var.domain_name}/admin
       Token: (stored in AWS Secrets Manager - retrieve with:)
       aws secretsmanager get-secret-value --secret-id ${aws_secretsmanager_secret.vaultwarden_config.id} --query SecretString --output text | jq -r .ADMIN_TOKEN
    
    3. Create Your Account:
       - Go to: https://${var.domain_name}
       - Click "Create Account"
       - After creating admin account, disable signups in admin panel
    
    4. Configure Vaultwarden:
       - Enable 2FA for your account
       - Review admin settings
       - Setup SMTP for email notifications (if not done)
    
    5. Install Clients:
       - Browser Extension: https://bitwarden.com/download/
       - Mobile Apps: iOS/Android App Stores
       - Desktop: https://bitwarden.com/download/
       - Configure custom server: https://${var.domain_name}
    
    6. Monitor:
       - CloudWatch Dashboard: https://console.aws.amazon.com/cloudwatch/
       - ECS Service: https://console.aws.amazon.com/ecs/
       - RDS Cluster: https://console.aws.amazon.com/rds/
    
    7. Backups:
       - Automatic daily backups configured via AWS Backup
       - Retention: ${var.backup_retention_days} days
       - Vault: ${aws_backup_vault.vaultwarden.name}
    
    🔒 Security:
       ✓ WAF enabled: ${var.enable_waf}
       ✓ SSL/TLS configured
       ✓ Secrets encrypted in Secrets Manager
       ✓ Multi-AZ deployment
       ✓ Automated backups
    
    📊 Cost Estimate:
       ~$30-50/month for < 100 users
       Scales automatically based on usage
    
    ⚠️  Important:
       - Store admin token securely
       - Disable public signups after creating accounts
       - Enable 2FA for all users
       - Review security settings in admin panel
  EOT
}

