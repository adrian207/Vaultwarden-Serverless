/**
 * GCP Infrastructure Variables
 * Author: Adrian Johnson <adrian207@gmail.com>
 */

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "vaultwarden"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "subnet_cidr" {
  description = "Subnet CIDR"
  type        = string
  default     = "10.0.0.0/24"
}

variable "vpc_connector_cidr" {
  description = "VPC connector CIDR"
  type        = string
  default     = "10.8.0.0/28"
}

variable "domain_name" {
  description = "Domain name for Vaultwarden"
  type        = string
}

variable "container_image" {
  description = "Container image"
  type        = string
  default     = "vaultwarden/server:latest"
}

variable "container_cpu" {
  description = "CPU limit"
  type        = string
  default     = "1"
}

variable "container_memory" {
  description = "Memory limit"
  type        = string
  default     = "512Mi"
}

variable "min_instances" {
  description = "Minimum instances"
  type        = number
  default     = 0
}

variable "max_instances" {
  description = "Maximum instances"
  type        = number
  default     = 10
}

variable "database_name" {
  description = "Database name"
  type        = string
  default     = "vaultwarden"
}

variable "database_username" {
  description = "Database username"
  type        = string
  default     = "vaultwarden_admin"
}

variable "db_tier" {
  description = "Cloud SQL tier"
  type        = string
  default     = "db-f1-micro"
}

variable "db_high_availability" {
  description = "Enable HA for database"
  type        = bool
  default     = false
}

variable "backup_retention_days" {
  description = "Backup retention days"
  type        = number
  default     = 30
}

variable "signups_allowed" {
  description = "Allow signups"
  type        = string
  default     = "false"
}

variable "invitations_allowed" {
  description = "Allow invitations"
  type        = string
  default     = "true"
}

variable "enable_public_access" {
  description = "Enable public access to Cloud Run"
  type        = bool
  default     = true
}

variable "enable_cloud_armor" {
  description = "Enable Cloud Armor"
  type        = bool
  default     = true
}

variable "deletion_protection" {
  description = "Enable deletion protection"
  type        = bool
  default     = true
}

