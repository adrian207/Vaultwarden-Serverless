# GCP Deployment Guide

**Author:** Adrian Johnson <adrian207@gmail.com>

## Summary

Deploy Vaultwarden on GCP using Cloud Run (fully serverless) and Cloud SQL (managed PostgreSQL). This is the most cost-effective option, with automatic scaling to zero when idle. Starting cost: ~$25-45/month.

## Architecture Components

- **Compute:** Cloud Run (serverless containers)
- **Database:** Cloud SQL PostgreSQL
- **Storage:** Cloud Storage (attachments)
- **Security:** Cloud Armor, Secret Manager, IAM
- **Networking:** VPC, Serverless VPC Access

## Prerequisites

1. **GCP Project** with billing enabled
2. **gcloud CLI** installed and authenticated
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```
3. **Terraform** 1.5+ installed
4. **(Optional) Domain name**

## Deployment Steps

### 1. Enable Required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  compute.googleapis.com \
  servicenetworking.googleapis.com \
  secretmanager.googleapis.com
```

### 2. Configure Terraform

```bash
cd infrastructure/gcp
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
project_id   = "your-gcp-project-id"
region       = "us-central1"
domain_name  = "vault.example.com"

# Cost optimization
container_cpu       = "1"      # 1 vCPU
container_memory    = "512Mi"  # 512 MB
min_instances       = 0        # Scale to zero
max_instances       = 10
db_tier             = "db-f1-micro"  # Smallest: ~$7/month
db_high_availability = false         # Single-zone for dev/test
```

### 3. Initialize and Deploy

```bash
terraform init
terraform plan
terraform apply
```

Deployment takes ~10-15 minutes.

### 4. Get Service URL

```bash
terraform output vaultwarden_url
```

Example output: `https://vaultwarden-prod-service-abc123-uc.a.run.app`

### 5. Map Custom Domain (Optional)

```bash
# Map domain to Cloud Run
gcloud run services update vaultwarden-prod-service \
  --region us-central1 \
  --platform managed \
  --add-custom-domain vault.example.com

# Follow instructions to verify domain ownership and update DNS
```

Alternatively, create DNS CNAME:
```
vault.example.com -> ghs.googlehosted.com
```

### 6. Initial Setup

1. **Access Vaultwarden**
   ```
   https://your-cloud-run-url.run.app
   ```

2. **Create Admin Account**
   - Click "Create Account"
   - Set strong master password
   - Enable 2FA immediately

3. **Get Admin Token**
   ```bash
   gcloud secrets versions access latest \
     --secret="vaultwarden-prod-admin-token"
   ```

4. **Access Admin Panel**
   - URL: `https://your-url/admin`
   - Enter admin token
   - Disable public signups
   - Configure settings

## Post-Deployment

### Monitoring

**View Logs**
```bash
gcloud run services logs read vaultwarden-prod-service \
  --region us-central1 \
  --limit 50
```

**Real-time Logs**
```bash
gcloud run services logs tail vaultwarden-prod-service \
  --region us-central1
```

**Service Details**
```bash
gcloud run services describe vaultwarden-prod-service \
  --region us-central1
```

**Metrics**
- Go to: Cloud Console > Cloud Run > vaultwarden-prod-service
- View: Request count, latency, instance count, CPU/memory usage

### Backups

**Automated Backups**
- Cloud SQL automatically backs up daily at 3:00 AM UTC
- Retention: 30 days (configurable)
- Point-in-time recovery enabled

**View Backups**
```bash
gcloud sql backups list --instance=vaultwarden-prod-db
```

**Create Manual Backup**
```bash
gcloud sql backups create \
  --instance=vaultwarden-prod-db \
  --description="Manual backup $(date +%Y-%m-%d)"
```

**Restore from Backup**
```bash
# List backups
gcloud sql backups list --instance=vaultwarden-prod-db

# Restore specific backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=vaultwarden-prod-db \
  --backup-id=BACKUP_ID
```

### Scaling

**Scale to Zero** (default)
- Cloud Run automatically scales to 0 when idle
- Cold start: ~2-3 seconds
- Cost when idle: $0

**Adjust Scaling**
```bash
gcloud run services update vaultwarden-prod-service \
  --region us-central1 \
  --min-instances 1 \  # Keep 1 instance always running
  --max-instances 20
```

**Database Scaling**
- db-f1-micro: 0.6 GB RAM, shared CPU (~$7/month)
- db-g1-small: 1.7 GB RAM, shared CPU (~$25/month)
- db-n1-standard-1: 3.75 GB RAM, 1 vCPU (~$50/month)

```bash
gcloud sql instances patch vaultwarden-prod-db \
  --tier=db-g1-small
```

### Cost Optimization

**Current Costs (approximate)**
| Component | Cost/Month |
|-----------|------------|
| Cloud Run (scaled to zero) | $0-10 |
| Cloud SQL (db-f1-micro) | $7-15 |
| Cloud Storage | $1-3 |
| VPC Connector | $7-10 |
| Networking | $1-5 |
| **Total** | **$15-45** |

**Optimization Tips**
1. **Scale to Zero:** Set `min_instances = 0`
2. **Smallest DB Tier:** Use `db-f1-micro` for < 50 users
3. **Single-Zone:** Disable HA for non-production
4. **Storage Lifecycle:** Enable Nearline/Coldline after 90 days
5. **Delete Old Logs:** Reduce log retention period

## Troubleshooting

### Issue: Service won't start

```bash
# Check recent logs
gcloud run services logs read vaultwarden-prod-service \
  --region us-central1 \
  --limit 100

# Check service configuration
gcloud run services describe vaultwarden-prod-service \
  --region us-central1 \
  --format=yaml
```

### Issue: Database connection errors

```bash
# Verify Cloud SQL instance
gcloud sql instances describe vaultwarden-prod-db

# Check VPC connector
gcloud compute networks vpc-access connectors describe \
  vaultwarden-prod-connector \
  --region us-central1

# Test database connectivity
gcloud sql connect vaultwarden-prod-db --user=vaultwarden_admin
```

### Issue: Out of memory errors

```bash
# Increase memory allocation
gcloud run services update vaultwarden-prod-service \
  --region us-central1 \
  --memory 1Gi
```

### Issue: Slow cold starts

```bash
# Keep 1 instance always warm
gcloud run services update vaultwarden-prod-service \
  --region us-central1 \
  --min-instances 1

# Enable CPU boost for faster startups
# (Already enabled in Terraform config)
```

## Maintenance

### Update Vaultwarden

```bash
# Update image in terraform.tfvars
container_image = "vaultwarden/server:1.30.0"

# Apply changes
terraform apply

# Cloud Run performs zero-downtime rolling update
```

### Backup Before Major Changes

```bash
# Backup database
gcloud sql backups create --instance=vaultwarden-prod-db

# Export to Cloud Storage (optional)
gcloud sql export sql vaultwarden-prod-db \
  gs://your-backup-bucket/vaultwarden-backup-$(date +%Y%m%d).sql \
  --database=vaultwarden
```

## Security Best Practices

1. **Enable Binary Authorization**
   ```bash
   gcloud run services update vaultwarden-prod-service \
     --region us-central1 \
     --binary-authorization=default
   ```

2. **Restrict Service Account Permissions**
   - Use least privilege principle
   - Separate service accounts for different services

3. **Enable Cloud Armor**
   - DDoS protection
   - Rate limiting
   - Bot detection

4. **Audit Logs**
   ```bash
   gcloud logging read "resource.type=cloud_run_revision AND \
     resource.labels.service_name=vaultwarden-prod-service" \
     --limit 50
   ```

5. **Security Scanning**
   - Enable Container Analysis API
   - Scan images for vulnerabilities

## Cleanup

To destroy all resources:

```bash
cd infrastructure/gcp
terraform destroy
```

⚠️ **Warning:** This permanently deletes all data. Ensure backups are secure.

## Comparison with AWS/Azure

| Feature | GCP Cloud Run | AWS Fargate | Azure Container Instances |
|---------|---------------|-------------|---------------------------|
| Scale to Zero | ✅ Yes | ❌ No | ⚠️ Limited |
| Cold Start | ~2-3s | N/A | ~10-15s |
| Min Cost/Month | $15-25 | $30-50 | $35-60 |
| Setup Complexity | Low | Medium | Medium |
| Global CDN | Cloud CDN | CloudFront | Azure CDN |

**GCP Advantages:**
- Lowest cost with scale-to-zero
- Simplest deployment
- Fastest cold starts
- No minimum charges

**GCP Disadvantages:**
- Cold starts (2-3 seconds)
- Less control over networking
- Limited Windows container support

## Support

- **Issues:** GitHub Issues
- **Documentation:** [Main README](../../README.md)
- **GCP Support:** https://cloud.google.com/support

