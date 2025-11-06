/**
 * GCP Serverless Infrastructure for Vaultwarden
 * Author: Adrian Johnson <adrian207@gmail.com>
 * 
 * Architecture:
 * - Cloud Run for serverless container deployment
 * - Cloud SQL (PostgreSQL) with automatic scaling
 * - Cloud Storage for attachments
 * - Cloud CDN for global distribution
 * - Cloud Armor for DDoS protection
 */

terraform {
  required_version = ">= 1.5"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
  
  backend "gcs" {
    # Configure for your environment
    # bucket = "your-terraform-state-bucket"
    # prefix = "vaultwarden"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  name_prefix = "${var.project_name}-${var.environment}"
  
  common_labels = {
    application = "vaultwarden"
    environment = var.environment
    managed_by  = "terraform"
  }
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "compute.googleapis.com",
    "servicenetworking.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudscheduler.googleapis.com",
  ])
  
  service = each.key
  disable_on_destroy = false
}

# VPC Network
resource "google_compute_network" "main" {
  name                    = "${local.name_prefix}-network"
  auto_create_subnetworks = false
  
  depends_on = [google_project_service.required_apis]
}

# Subnet
resource "google_compute_subnetwork" "main" {
  name          = "${local.name_prefix}-subnet"
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.main.id
  
  private_ip_google_access = true
}

# VPC Peering for Cloud SQL
resource "google_compute_global_address" "private_ip_address" {
  name          = "${local.name_prefix}-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.main.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.main.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
  
  depends_on = [google_project_service.required_apis]
}

# Random password for database
resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Cloud SQL Instance (PostgreSQL)
resource "google_sql_database_instance" "main" {
  name             = "${local.name_prefix}-db"
  database_version = "POSTGRES_15"
  region           = var.region
  
  settings {
    tier              = var.db_tier
    availability_type = var.db_high_availability ? "REGIONAL" : "ZONAL"
    disk_autoresize   = true
    disk_size         = 10
    
    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "03:00"
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = var.backup_retention_days
      }
    }
    
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
    }
    
    database_flags {
      name  = "max_connections"
      value = "100"
    }
  }
  
  deletion_protection = var.deletion_protection
  
  depends_on = [google_service_networking_connection.private_vpc_connection]
}

# Database
resource "google_sql_database" "vaultwarden" {
  name     = var.database_name
  instance = google_sql_database_instance.main.name
}

# Database User
resource "google_sql_user" "vaultwarden" {
  name     = var.database_username
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}

# Cloud Storage Bucket for attachments
resource "google_storage_bucket" "attachments" {
  name          = "${local.name_prefix}-attachments-${random_id.bucket_suffix.hex}"
  location      = var.region
  force_destroy = false
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
  
  labels = local.common_labels
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Service Account for Cloud Run
resource "google_service_account" "vaultwarden" {
  account_id   = "${local.name_prefix}-sa"
  display_name = "Vaultwarden Service Account"
}

# Grant Cloud SQL Client role
resource "google_project_iam_member" "cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.vaultwarden.email}"
}

# Grant Storage Object Admin role
resource "google_storage_bucket_iam_member" "vaultwarden_storage" {
  bucket = google_storage_bucket.attachments.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.vaultwarden.email}"
}

# Secret Manager for sensitive data
resource "google_secret_manager_secret" "admin_token" {
  secret_id = "${local.name_prefix}-admin-token"
  
  replication {
    auto {}
  }
  
  labels = local.common_labels
}

resource "random_password" "admin_token" {
  length  = 48
  special = true
}

resource "google_secret_manager_secret_version" "admin_token" {
  secret      = google_secret_manager_secret.admin_token.id
  secret_data = random_password.admin_token.result
}

resource "google_secret_manager_secret_iam_member" "admin_token_access" {
  secret_id = google_secret_manager_secret.admin_token.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.vaultwarden.email}"
}

# Cloud Run Service
resource "google_cloud_run_v2_service" "vaultwarden" {
  name     = "${local.name_prefix}-service"
  location = var.region
  
  template {
    service_account = google_service_account.vaultwarden.email
    
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }
    
    containers {
      image = var.container_image
      
      resources {
        limits = {
          cpu    = var.container_cpu
          memory = var.container_memory
        }
        cpu_idle          = true
        startup_cpu_boost = true
      }
      
      ports {
        container_port = 80
      }
      
      env {
        name  = "DOMAIN"
        value = "https://${var.domain_name}"
      }
      
      env {
        name  = "SIGNUPS_ALLOWED"
        value = var.signups_allowed
      }
      
      env {
        name  = "INVITATIONS_ALLOWED"
        value = var.invitations_allowed
      }
      
      env {
        name  = "WEB_VAULT_ENABLED"
        value = "true"
      }
      
      env {
        name  = "WEBSOCKET_ENABLED"
        value = "true"
      }
      
      env {
        name  = "DATABASE_URL"
        value = "postgresql://${google_sql_user.vaultwarden.name}:${google_sql_user.vaultwarden.password}@localhost/${google_sql_database.vaultwarden.name}?host=/cloudsql/${google_sql_database_instance.main.connection_name}"
      }
      
      env {
        name = "ADMIN_TOKEN"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.admin_token.secret_id
            version = "latest"
          }
        }
      }
      
      env {
        name  = "GCS_BUCKET"
        value = google_storage_bucket.attachments.name
      }
      
      env {
        name  = "ROCKET_WORKERS"
        value = "10"
      }
    }
    
    vpc_access {
      connector = google_vpc_access_connector.main.id
      egress    = "PRIVATE_RANGES_ONLY"
    }
  }
  
  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
  
  depends_on = [
    google_project_service.required_apis,
    google_sql_database_instance.main
  ]
}

# VPC Access Connector
resource "google_vpc_access_connector" "main" {
  name          = "${local.name_prefix}-connector"
  region        = var.region
  network       = google_compute_network.main.name
  ip_cidr_range = var.vpc_connector_cidr
  
  min_instances = 2
  max_instances = 10
}

# IAM for public access (or use Cloud Armor + Load Balancer for more control)
resource "google_cloud_run_service_iam_member" "public_access" {
  count    = var.enable_public_access ? 1 : 0
  location = google_cloud_run_v2_service.vaultwarden.location
  service  = google_cloud_run_v2_service.vaultwarden.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Cloud Armor Security Policy (for DDoS protection)
resource "google_compute_security_policy" "vaultwarden" {
  count = var.enable_cloud_armor ? 1 : 0
  name  = "${local.name_prefix}-security-policy"
  
  rule {
    action   = "rate_based_ban"
    priority = "1000"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    rate_limit_options {
      conform_action = "allow"
      exceed_action  = "deny(429)"
      enforce_on_key = "IP"
      ban_duration_sec = 600
      rate_limit_threshold {
        count        = 100
        interval_sec = 60
      }
    }
  }
  
  rule {
    action   = "allow"
    priority = "2147483647"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
  }
}

