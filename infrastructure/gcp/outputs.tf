/**
 * GCP Infrastructure Outputs
 * Author: Adrian Johnson <adrian207@gmail.com>
 */

output "vaultwarden_url" {
  description = "Vaultwarden URL"
  value       = google_cloud_run_v2_service.vaultwarden.uri
}

output "cloud_run_service_name" {
  description = "Cloud Run service name"
  value       = google_cloud_run_v2_service.vaultwarden.name
}

output "database_connection_name" {
  description = "Cloud SQL connection name"
  value       = google_sql_database_instance.main.connection_name
  sensitive   = true
}

output "database_private_ip" {
  description = "Database private IP"
  value       = google_sql_database_instance.main.private_ip_address
  sensitive   = true
}

output "storage_bucket_name" {
  description = "Storage bucket name"
  value       = google_storage_bucket.attachments.name
}

output "admin_token" {
  description = "Admin token"
  value       = random_password.admin_token.result
  sensitive   = true
}

output "post_deployment_steps" {
  description = "Post-deployment instructions"
  value = <<-EOT
    ╔══════════════════════════════════════════════════════════════════╗
    ║          Vaultwarden GCP Deployment Complete!                    ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    🌐 Access URL: ${google_cloud_run_v2_service.vaultwarden.uri}
    
    📋 Next Steps:
    
    1. Map Custom Domain:
       gcloud run services update ${google_cloud_run_v2_service.vaultwarden.name} \
         --region ${var.region} \
         --platform managed \
         --domain ${var.domain_name}
    
    2. Get Admin Token:
       gcloud secrets versions access latest --secret="${google_secret_manager_secret.admin_token.secret_id}"
    
    3. Access Admin Panel:
       URL: ${google_cloud_run_v2_service.vaultwarden.uri}/admin
       
    4. Create Account and Configure:
       - Visit ${google_cloud_run_v2_service.vaultwarden.uri}
       - Create your admin account
       - Disable signups in admin panel
    
    5. Install Bitwarden Clients:
       - Set custom server URL to: ${google_cloud_run_v2_service.vaultwarden.uri}
    
    💰 Cost Estimate: $25-45/month for < 100 users
       - Scales to zero when idle
       - Pay only for actual usage
    
    🔒 Security:
       ✓ Private database access
       ✓ HTTPS enforced
       ✓ Cloud Armor enabled: ${var.enable_cloud_armor}
       ✓ Secrets encrypted
       ✓ Automated backups
  EOT
}

