/**
 * AWS Infrastructure Variables
 * Author: Adrian Johnson <adrian207@gmail.com>
 */

# General Configuration
variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "vaultwarden"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "availability_zones" {
  description = "Availability zones for multi-AZ deployment"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

# Networking
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# Domain and SSL
variable "domain_name" {
  description = "Domain name for Vaultwarden (e.g., vault.example.com)"
  type        = string
}

variable "certificate_arn" {
  description = "ACM certificate ARN for HTTPS. Create in AWS Certificate Manager first."
  type        = string
}

# Container Configuration
variable "vaultwarden_image" {
  description = "Docker image for Vaultwarden"
  type        = string
  default     = "vaultwarden/server:latest"
}

variable "container_cpu" {
  description = "CPU units for container (1024 = 1 vCPU)"
  type        = number
  default     = 512
}

variable "container_memory" {
  description = "Memory for container in MB"
  type        = number
  default     = 1024
}

variable "desired_count" {
  description = "Desired number of container instances"
  type        = number
  default     = 2
}

variable "min_capacity" {
  description = "Minimum number of container instances for auto-scaling"
  type        = number
  default     = 1
}

variable "max_capacity" {
  description = "Maximum number of container instances for auto-scaling"
  type        = number
  default     = 10
}

# Database Configuration
variable "database_name" {
  description = "Database name"
  type        = string
  default     = "vaultwarden"
}

variable "database_username" {
  description = "Database master username"
  type        = string
  default     = "vaultwarden_admin"
  sensitive   = true
}

variable "db_min_capacity" {
  description = "Minimum Aurora Serverless v2 capacity units (0.5-128)"
  type        = number
  default     = 0.5
}

variable "db_max_capacity" {
  description = "Maximum Aurora Serverless v2 capacity units (0.5-128)"
  type        = number
  default     = 4
}

# Vaultwarden Configuration
variable "signups_allowed" {
  description = "Allow new user registrations"
  type        = string
  default     = "false"  # Disable after initial setup
}

variable "invitations_allowed" {
  description = "Allow user invitations"
  type        = string
  default     = "true"
}

# SMTP Configuration (for email notifications)
variable "smtp_host" {
  description = "SMTP server host"
  type        = string
  default     = ""
}

variable "smtp_port" {
  description = "SMTP server port"
  type        = number
  default     = 587
}

variable "smtp_from" {
  description = "From email address"
  type        = string
  default     = "vaultwarden@example.com"
}

variable "smtp_security" {
  description = "SMTP security (starttls, force_tls, off)"
  type        = string
  default     = "starttls"
}

variable "smtp_password" {
  description = "SMTP password"
  type        = string
  default     = ""
  sensitive   = true
}

# S3 Configuration
variable "s3_lifecycle_rules" {
  description = "S3 lifecycle rules for attachment storage"
  type = list(object({
    enabled = bool
    id      = string
    transition_days = number
    storage_class   = string
  }))
  default = [
    {
      enabled         = true
      id              = "intelligent_tiering"
      transition_days = 90
      storage_class   = "INTELLIGENT_TIERING"
    }
  ]
}

# Backup Configuration
variable "backup_retention_days" {
  description = "Number of days to retain backups"
  type        = number
  default     = 30
}

# Monitoring
variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}

variable "alarm_sns_topic_arn" {
  description = "SNS topic ARN for CloudWatch alarms"
  type        = string
  default     = ""
}

# Security Features
variable "enable_waf" {
  description = "Enable AWS WAF for DDoS protection"
  type        = bool
  default     = true
}

variable "enable_cloudfront" {
  description = "Enable CloudFront CDN for global distribution"
  type        = bool
  default     = false
}

# Tags
variable "additional_tags" {
  description = "Additional tags for all resources"
  type        = map(string)
  default     = {}
}

