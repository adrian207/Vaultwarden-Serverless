/**
 * AWS Serverless Infrastructure for Vaultwarden
 * Author: Adrian Johnson <adrian207@gmail.com>
 * 
 * Architecture:
 * - ECS Fargate for serverless container orchestration
 * - Aurora Serverless v2 for auto-scaling PostgreSQL database
 * - S3 for attachment storage
 * - CloudFront for CDN
 * - Application Load Balancer for HTTPS termination
 * - WAF for DDoS and bot protection
 */

terraform {
  required_version = ">= 1.5"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    # Configure this for your environment
    # bucket = "your-terraform-state-bucket"
    # key    = "vaultwarden/terraform.tfstate"
    # region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "Vaultwarden"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Author      = "Adrian Johnson"
    }
  }
}

# Local variables for resource naming
locals {
  name_prefix = "${var.project_name}-${var.environment}"
  
  common_tags = {
    Application = "Vaultwarden"
    Environment = var.environment
  }
}

# VPC and Networking
module "networking" {
  source = "./modules/networking"
  
  name_prefix        = local.name_prefix
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  
  tags = local.common_tags
}

# RDS Aurora Serverless v2 (PostgreSQL)
module "database" {
  source = "./modules/database"
  
  name_prefix           = local.name_prefix
  vpc_id                = module.networking.vpc_id
  private_subnet_ids    = module.networking.private_subnet_ids
  allowed_security_groups = [module.compute.ecs_security_group_id]
  
  database_name         = var.database_name
  master_username       = var.database_username
  min_capacity          = var.db_min_capacity
  max_capacity          = var.db_max_capacity
  backup_retention_days = var.backup_retention_days
  
  tags = local.common_tags
}

# S3 Bucket for Attachments
module "storage" {
  source = "./modules/storage"
  
  name_prefix        = local.name_prefix
  enable_versioning  = true
  enable_encryption  = true
  lifecycle_rules    = var.s3_lifecycle_rules
  
  tags = local.common_tags
}

# Secrets Manager for sensitive configuration
resource "aws_secretsmanager_secret" "vaultwarden_config" {
  name_prefix = "${local.name_prefix}-config-"
  description = "Vaultwarden configuration secrets"
  
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret_version" "vaultwarden_config" {
  secret_id = aws_secretsmanager_secret.vaultwarden_config.id
  
  secret_string = jsonencode({
    DATABASE_URL        = "postgresql://${var.database_username}:${module.database.master_password}@${module.database.cluster_endpoint}:5432/${var.database_name}"
    ADMIN_TOKEN         = random_password.admin_token.result
    SMTP_PASSWORD       = var.smtp_password
  })
}

resource "random_password" "admin_token" {
  length  = 48
  special = true
}

# ECS Fargate Cluster and Service
module "compute" {
  source = "./modules/compute"
  
  name_prefix          = local.name_prefix
  vpc_id               = module.networking.vpc_id
  private_subnet_ids   = module.networking.private_subnet_ids
  public_subnet_ids    = module.networking.public_subnet_ids
  
  # Container configuration
  container_image      = var.vaultwarden_image
  container_port       = 80
  container_cpu        = var.container_cpu
  container_memory     = var.container_memory
  desired_count        = var.desired_count
  min_capacity         = var.min_capacity
  max_capacity         = var.max_capacity
  
  # Environment variables
  environment_variables = {
    DOMAIN              = "https://${var.domain_name}"
    SIGNUPS_ALLOWED     = var.signups_allowed
    INVITATIONS_ALLOWED = var.invitations_allowed
    SHOW_PASSWORD_HINT  = "false"
    WEB_VAULT_ENABLED   = "true"
    WEBSOCKET_ENABLED   = "true"
    SENDS_ALLOWED       = "true"
    EMERGENCY_ACCESS_ALLOWED = "true"
    
    # S3 Attachments
    ATTACHMENTS_S3_BUCKET = module.storage.bucket_name
    ATTACHMENTS_S3_REGION = var.aws_region
    
    # SMTP Configuration
    SMTP_HOST     = var.smtp_host
    SMTP_PORT     = var.smtp_port
    SMTP_FROM     = var.smtp_from
    SMTP_SECURITY = var.smtp_security
    
    # Performance tuning
    ROCKET_WORKERS = "10"
    DATABASE_MAX_CONNS = "10"
  }
  
  # Secret environment variables from Secrets Manager
  secrets = [
    {
      name      = "DATABASE_URL"
      valueFrom = "${aws_secretsmanager_secret.vaultwarden_config.arn}:DATABASE_URL::"
    },
    {
      name      = "ADMIN_TOKEN"
      valueFrom = "${aws_secretsmanager_secret.vaultwarden_config.arn}:ADMIN_TOKEN::"
    },
    {
      name      = "SMTP_PASSWORD"
      valueFrom = "${aws_secretsmanager_secret.vaultwarden_config.arn}:SMTP_PASSWORD::"
    }
  ]
  
  # Health check
  health_check_path     = "/alive"
  health_check_interval = 30
  
  # SSL Certificate ARN (create in ACM first)
  certificate_arn = var.certificate_arn
  domain_name     = var.domain_name
  
  # Enable auto-scaling
  enable_autoscaling = true
  cpu_threshold      = 70
  memory_threshold   = 80
  
  # Grant S3 access
  s3_bucket_arn = module.storage.bucket_arn
  
  tags = local.common_tags
}

# WAF for DDoS and bot protection
resource "aws_wafv2_web_acl" "vaultwarden" {
  count = var.enable_waf ? 1 : 0
  
  name  = "${local.name_prefix}-waf"
  scope = "REGIONAL"
  
  default_action {
    allow {}
  }
  
  # Rate limiting rule
  rule {
    name     = "RateLimit"
    priority = 1
    
    action {
      block {}
    }
    
    statement {
      rate_based_statement {
        limit              = 2000
        aggregate_key_type = "IP"
      }
    }
    
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimit"
      sampled_requests_enabled   = true
    }
  }
  
  # AWS Managed Rules - Core Rule Set
  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 2
    
    override_action {
      none {}
    }
    
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }
    
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesCommonRuleSet"
      sampled_requests_enabled   = true
    }
  }
  
  # AWS Managed Rules - Known Bad Inputs
  rule {
    name     = "AWSManagedRulesKnownBadInputsRuleSet"
    priority = 3
    
    override_action {
      none {}
    }
    
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }
    
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWSManagedRulesKnownBadInputsRuleSet"
      sampled_requests_enabled   = true
    }
  }
  
  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "VaultwardenWAF"
    sampled_requests_enabled   = true
  }
  
  tags = local.common_tags
}

# Associate WAF with ALB
resource "aws_wafv2_web_acl_association" "vaultwarden" {
  count = var.enable_waf ? 1 : 0
  
  resource_arn = module.compute.alb_arn
  web_acl_arn  = aws_wafv2_web_acl.vaultwarden[0].arn
}

# CloudFront Distribution (optional, for global CDN)
resource "aws_cloudfront_distribution" "vaultwarden" {
  count = var.enable_cloudfront ? 1 : 0
  
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Vaultwarden CDN"
  aliases             = [var.domain_name]
  price_class         = "PriceClass_100"  # Use only North America and Europe
  
  origin {
    domain_name = module.compute.alb_dns_name
    origin_id   = "ALB"
    
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }
  
  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "ALB"
    
    forwarded_values {
      query_string = true
      headers      = ["Host", "Authorization", "CloudFront-Forwarded-Proto"]
      
      cookies {
        forward = "all"
      }
    }
    
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0
    compress               = true
  }
  
  # Cache static assets
  ordered_cache_behavior {
    path_pattern     = "/app/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "ALB"
    
    forwarded_values {
      query_string = false
      
      cookies {
        forward = "none"
      }
    }
    
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 3600
    default_ttl            = 86400
    max_ttl                = 31536000
    compress               = true
  }
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    acm_certificate_arn      = var.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
  
  tags = local.common_tags
}

# CloudWatch Log Group for monitoring
resource "aws_cloudwatch_log_group" "vaultwarden" {
  name              = "/aws/ecs/${local.name_prefix}"
  retention_in_days = var.log_retention_days
  
  tags = local.common_tags
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${local.name_prefix}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ECS CPU utilization"
  
  dimensions = {
    ClusterName = module.compute.cluster_name
    ServiceName = module.compute.service_name
  }
  
  alarm_actions = var.alarm_sns_topic_arn != "" ? [var.alarm_sns_topic_arn] : []
  
  tags = local.common_tags
}

resource "aws_cloudwatch_metric_alarm" "database_cpu" {
  alarm_name          = "${local.name_prefix}-db-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors RDS CPU utilization"
  
  dimensions = {
    DBClusterIdentifier = module.database.cluster_identifier
  }
  
  alarm_actions = var.alarm_sns_topic_arn != "" ? [var.alarm_sns_topic_arn] : []
  
  tags = local.common_tags
}

# Backup plan using AWS Backup
resource "aws_backup_vault" "vaultwarden" {
  name = "${local.name_prefix}-backup-vault"
  
  tags = local.common_tags
}

resource "aws_backup_plan" "vaultwarden" {
  name = "${local.name_prefix}-backup-plan"
  
  rule {
    rule_name         = "daily_backup"
    target_vault_name = aws_backup_vault.vaultwarden.name
    schedule          = "cron(0 2 * * ? *)"  # Daily at 2 AM UTC
    
    lifecycle {
      delete_after = var.backup_retention_days
    }
  }
  
  tags = local.common_tags
}

resource "aws_backup_selection" "vaultwarden" {
  name         = "${local.name_prefix}-backup-selection"
  plan_id      = aws_backup_plan.vaultwarden.id
  iam_role_arn = aws_iam_role.backup.arn
  
  resources = [
    module.database.cluster_arn
  ]
}

resource "aws_iam_role" "backup" {
  name = "${local.name_prefix}-backup-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "backup.amazonaws.com"
      }
    }]
  })
  
  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "backup" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

resource "aws_iam_role_policy_attachment" "restore" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForRestores"
}

