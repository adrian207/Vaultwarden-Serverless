# AWS Deployment Guide

**Author:** Adrian Johnson <adrian207@gmail.com>

## Summary

Deploy Vaultwarden on AWS using ECS Fargate (serverless containers) and Aurora Serverless v2 (auto-scaling database). This configuration provides automatic scaling from 0 to 100,000+ users with ~$30-50/month starting cost.

## Architecture Components

- **Compute:** ECS Fargate (serverless containers)
- **Database:** Aurora Serverless v2 PostgreSQL
- **Storage:** S3 (attachments)
- **CDN:** CloudFront (optional)
- **Security:** WAF, SSL/TLS, Secrets Manager
- **Networking:** VPC, ALB, NAT Gateway

## Prerequisites

### Required

1. **AWS Account** with admin access
2. **AWS CLI** v2+ installed and configured
   ```bash
   aws configure
   ```
3. **Terraform** 1.5+ installed
4. **Domain name** (or use ALB DNS name)

### Optional

5. **ACM Certificate** for custom domain
   ```bash
   aws acm request-certificate \
     --domain-name vault.example.com \
     --validation-method DNS \
     --region us-east-1
   ```

## Deployment Steps

### 1. Clone and Configure

```bash
cd infrastructure/aws
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
domain_name     = "vault.example.com"
certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/your-cert-id"
aws_region      = "us-east-1"

# Adjust capacity as needed
container_cpu    = 512   # 0.5 vCPU
container_memory = 1024  # 1 GB
db_min_capacity  = 0.5   # Aurora ACUs
db_max_capacity  = 4

# Disable signups after initial setup
signups_allowed = "false"
```

### 2. Initialize Terraform

```bash
terraform init
```

### 3. Plan Deployment

```bash
terraform plan
```

Review the resources that will be created:
- VPC with public and private subnets across 3 AZs
- ECS Fargate cluster and service
- Aurora Serverless v2 cluster (2 instances)
- Application Load Balancer
- S3 bucket for attachments
- Secrets Manager for sensitive data
- CloudWatch logs and alarms
- AWS Backup vault and plan

### 4. Deploy

```bash
terraform apply
```

Type `yes` to confirm. Deployment takes ~15-20 minutes.

### 5. Configure DNS

Get the ALB DNS name:
```bash
terraform output alb_dns_name
```

Create DNS record:

**Option A: Route53 (recommended)**
```bash
aws route53 change-resource-record-sets \
  --hosted-zone-id YOUR_ZONE_ID \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "vault.example.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "'$(terraform output -raw alb_zone_id)'",
          "DNSName": "'$(terraform output -raw alb_dns_name)'",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'
```

**Option B: Other DNS providers**
- Create CNAME record pointing to ALB DNS name

### 6. Access Vaultwarden

Wait 2-3 minutes for DNS propagation, then access:
```
https://vault.example.com
```

### 7. Initial Configuration

1. **Create Admin Account**
   - Visit your domain
   - Click "Create Account"
   - Create your master password (NEVER forgotten - cannot be recovered!)

2. **Get Admin Token**
   ```bash
   terraform output -raw admin_token
   ```

3. **Access Admin Panel**
   - Go to: `https://vault.example.com/admin`
   - Enter admin token
   - **Disable public signups**
   - Configure SMTP (optional)
   - Enable 2FA for your account

4. **Install Clients**
   - Download official Bitwarden clients
   - Configure server URL: `https://vault.example.com`
   - Login with your credentials

## Post-Deployment

### Monitoring

**CloudWatch Dashboard**
```bash
aws cloudwatch get-dashboard --dashboard-name vaultwarden-prod
```

**View Logs**
```bash
aws logs tail /aws/ecs/vaultwarden-prod --follow
```

**ECS Service Status**
```bash
aws ecs describe-services \
  --cluster vaultwarden-prod-cluster \
  --services vaultwarden-prod-service
```

### Backups

Automated backups are configured via AWS Backup:

**List Backups**
```bash
aws backup list-recovery-points-by-backup-vault \
  --backup-vault-name vaultwarden-prod-backup-vault
```

**Manual Backup**
```bash
aws backup start-backup-job \
  --backup-vault-name vaultwarden-prod-backup-vault \
  --resource-arn $(terraform output -raw database_endpoint) \
  --iam-role-arn BACKUP_ROLE_ARN
```

### Scaling

**Manual Scale**
```bash
aws ecs update-service \
  --cluster vaultwarden-prod-cluster \
  --service vaultwarden-prod-service \
  --desired-count 3
```

Auto-scaling is enabled by default:
- CPU threshold: 70%
- Memory threshold: 80%
- Min instances: 1
- Max instances: 10

### Cost Optimization

**Current Costs (approximate)**
- ECS Fargate (2 tasks): $15-20/month
- Aurora Serverless v2 (0.5-4 ACUs): $10-25/month
- S3: $1-5/month
- Data transfer: $1-5/month
- **Total: $30-50/month**

**Optimization Tips**
1. Use Aurora Serverless v2 pause/resume
2. Enable S3 Intelligent Tiering
3. Reduce backup retention if acceptable
4. Use single-AZ for non-production
5. Skip CloudFront if not needed globally

## Troubleshooting

### Issue: ECS tasks failing health checks

```bash
# Check task logs
aws logs tail /aws/ecs/vaultwarden-prod --follow

# Check task definition
aws ecs describe-task-definition \
  --task-definition vaultwarden-prod-task
```

### Issue: Database connection errors

```bash
# Verify security groups
aws ec2 describe-security-groups \
  --filters "Name=tag:Name,Values=vaultwarden-prod-*"

# Check database status
aws rds describe-db-clusters \
  --db-cluster-identifier vaultwarden-prod-cluster
```

### Issue: SSL certificate errors

```bash
# Verify certificate
aws acm describe-certificate \
  --certificate-arn YOUR_CERT_ARN
```

## Maintenance

### Update Vaultwarden Version

```bash
# Update container image in terraform.tfvars
vaultwarden_image = "vaultwarden/server:1.30.0"

# Apply changes
terraform apply

# ECS will perform rolling update with zero downtime
```

### Backup Database Manually

```bash
aws rds create-db-cluster-snapshot \
  --db-cluster-identifier vaultwarden-prod-cluster \
  --db-cluster-snapshot-identifier manual-backup-$(date +%Y%m%d)
```

### Restore from Backup

```bash
# List available snapshots
aws rds describe-db-cluster-snapshots \
  --db-cluster-identifier vaultwarden-prod-cluster

# Restore (creates new cluster)
aws rds restore-db-cluster-from-snapshot \
  --db-cluster-identifier vaultwarden-prod-cluster-restored \
  --snapshot-identifier SNAPSHOT_ID \
  --engine aurora-postgresql
```

## Cleanup

To destroy all resources:

```bash
cd infrastructure/aws
terraform destroy
```

⚠️ **Warning:** This deletes all data. Ensure backups are secure before destroying.

## Support

- **Issues:** GitHub Issues
- **Documentation:** [Main README](../../README.md)
- **Security:** security@example.com

