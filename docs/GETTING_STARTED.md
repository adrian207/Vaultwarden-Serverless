# Getting Started with Vaultwarden Serverless Deployment

**Author:** Adrian Johnson <adrian207@gmail.com>

## What You're Deploying

This repository deploys **Vaultwarden**, a lightweight, open-source Bitwarden-compatible password manager server, using serverless infrastructure on AWS, Azure, or GCP. It provides enterprise-grade password management with automatic scaling to 100,000+ users while keeping costs low.

## Quick Decision Guide

### Which Cloud Provider Should I Choose?

| Cloud | Best For | Starting Cost/Month | Scale to Zero | Setup Time |
|-------|----------|---------------------|---------------|------------|
| **GCP** | Cost optimization, simple setup | $15-25 | ✅ Yes | 15 min |
| **AWS** | Enterprise, maximum control | $30-50 | ❌ No | 20 min |
| **Azure** | Microsoft ecosystem | $35-60 | ⚠️ Limited | 25 min |

**Recommendation:**
- **For personal/small team:** GCP Cloud Run
- **For enterprise:** AWS ECS Fargate
- **For Microsoft shops:** Azure Container Instances

## Prerequisites Checklist

### All Deployments
- [ ] Cloud account with admin access
- [ ] Credit card (for cloud provider billing)
- [ ] Basic command line knowledge
- [ ] 30-60 minutes of time

### Software Requirements
- [ ] [Terraform](https://www.terraform.io/downloads) 1.5+
- [ ] [Git](https://git-scm.com/downloads)
- [ ] Cloud CLI:
  - AWS: [AWS CLI](https://aws.amazon.com/cli/)
  - GCP: [gcloud CLI](https://cloud.google.com/sdk/docs/install)
  - Azure: [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

### Optional (But Recommended)
- [ ] Domain name ($10-15/year)
- [ ] Email provider for SMTP (Gmail, SendGrid, etc.)

## Step-by-Step Deployment

### Phase 1: Preparation (10 minutes)

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/vaultwarden-serverless.git
   cd vaultwarden-serverless
   ```

2. **Choose Cloud Provider**
   ```bash
   # Navigate to your chosen provider
   cd infrastructure/gcp    # For GCP
   # OR
   cd infrastructure/aws    # For AWS
   # OR
   cd infrastructure/azure  # For Azure
   ```

3. **Install Cloud CLI and Login**
   
   **GCP:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```
   
   **AWS:**
   ```bash
   aws configure
   # Enter your AWS Access Key ID and Secret
   ```
   
   **Azure:**
   ```bash
   az login
   az account set --subscription YOUR_SUBSCRIPTION_ID
   ```

### Phase 2: Configuration (5 minutes)

1. **Copy Example Configuration**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Edit Configuration**
   ```bash
   # Use your preferred editor
   nano terraform.tfvars
   # OR
   code terraform.tfvars
   ```

3. **Minimum Required Settings**
   
   **GCP:**
   ```hcl
   project_id  = "your-project-id"    # Required
   domain_name = "vault.example.com"   # Optional
   ```
   
   **AWS:**
   ```hcl
   aws_region      = "us-east-1"
   domain_name     = "vault.example.com"
   certificate_arn = "arn:aws:acm:..."  # Create first
   ```

### Phase 3: Deployment (15-20 minutes)

1. **Initialize Terraform**
   ```bash
   terraform init
   ```

2. **Preview Changes**
   ```bash
   terraform plan
   ```
   
   Review the resources that will be created. Look for:
   - ✅ Compute resources (ECS/Cloud Run)
   - ✅ Database (Aurora/Cloud SQL)
   - ✅ Storage (S3/Cloud Storage)
   - ✅ Networking (VPC/Subnets)

3. **Deploy**
   ```bash
   terraform apply
   ```
   
   Type `yes` when prompted. Get coffee ☕ - this takes 15-20 minutes.

4. **Save Outputs**
   ```bash
   # Save important information
   terraform output -raw vaultwarden_url > url.txt
   terraform output -raw admin_token > admin_token.txt
   chmod 600 admin_token.txt  # Protect admin token
   ```

### Phase 4: Initial Setup (10 minutes)

1. **Access Vaultwarden**
   ```bash
   # Get your URL
   cat url.txt
   ```
   
   Open the URL in your browser.

2. **Create Master Account**
   - Click "Create Account"
   - Enter email: `your-email@example.com`
   - Create **strong** master password
   - ⚠️ **CRITICAL:** Write down your master password. It CANNOT be recovered!

3. **Access Admin Panel**
   ```bash
   # Get admin token
   cat admin_token.txt
   ```
   
   - Go to: `https://your-url/admin`
   - Enter admin token
   - **Immediately disable public signups**
   - Enable 2FA for your account

4. **Configure SMTP (Optional)**
   - In admin panel: Settings > SMTP
   - Enter your email provider details
   - Test email configuration

### Phase 5: Install Clients (5 minutes)

1. **Download Bitwarden Clients**
   - Browser: [Chrome](https://chrome.google.com/webstore/detail/bitwarden/nngceckbapebfimnlniiiahkandclblb) / [Firefox](https://addons.mozilla.org/en-US/firefox/addon/bitwarden-password-manager/)
   - Desktop: [Download](https://bitwarden.com/download/)
   - Mobile: [iOS](https://apps.apple.com/app/bitwarden-password-manager/id1137397744) / [Android](https://play.google.com/store/apps/details?id=com.x8bit.bitwarden)

2. **Configure Custom Server**
   - Open Bitwarden client
   - Click settings ⚙️
   - Server URL: `https://your-url`
   - Login with your credentials

3. **Enable 2FA**
   - In web vault: Settings > Two-step Login
   - Choose method (Authenticator app recommended)
   - Save backup codes securely

## What's Next?

### Immediate Actions
- [ ] Test password saving/retrieval
- [ ] Backup master password offline
- [ ] Save admin token securely
- [ ] Enable 2FA on all accounts
- [ ] Disable public signups (if not done)

### Within First Week
- [ ] Import passwords from other managers
- [ ] Invite team members (if using Organizations)
- [ ] Setup custom domain (if using ALB DNS)
- [ ] Configure backup notifications
- [ ] Test password health reports

### Ongoing Maintenance
- [ ] Monitor costs (monthly)
- [ ] Update Vaultwarden version (quarterly)
- [ ] Review access logs (monthly)
- [ ] Test backup restoration (quarterly)
- [ ] Review security settings (monthly)

## Cost Expectations

### Quick Reference

| Users | GCP Cost | AWS Cost | Recommended Tier |
|-------|----------|----------|------------------|
| 1-10 | $15-25 | $30-45 | Personal |
| 10-100 | $35-60 | $60-90 | Small Team |
| 100-1K | $120-180 | $180-260 | Medium Org |
| 1K-10K | $400-600 | $600-900 | Large Enterprise |
| 10K-50K | $1,500-2,500 | $2,500-4,000 | Very Large |
| 50K-100K+ | $5,000-8,000 | $8,000-15,000 | Massive Scale |

📊 **See [Scaling Guide](operations/SCALING_GUIDE.md) for complete configurations and benchmarks at each tier**

### Key Features by Scale
- **Tier 0-1 (< 100 users):** Single region, basic configuration, scales to zero (GCP)
- **Tier 2-3 (100-10K users):** High availability, auto-scaling, CDN support
- **Tier 4-5 (10K-100K+ users):** Multi-region, global CDN, advanced caching, 99.99% uptime

## Common Issues & Solutions

### Issue: "Access Denied" or Permissions Error
**Solution:**
- Verify cloud CLI is authenticated: `gcloud auth list` / `aws sts get-caller-identity`
- Ensure you have admin/owner permissions on the project/account

### Issue: Domain/SSL Certificate Errors
**Solution:**
- AWS: Create ACM certificate BEFORE deployment
- GCP: Map domain AFTER deployment via Cloud Run console
- Verify DNS propagation: `nslookup your-domain.com`

### Issue: High Costs
**Solution:**
- GCP: Ensure `min_instances = 0` for scale-to-zero
- AWS: Reduce `desired_count` and `db_max_capacity`
- All: Enable database auto-pause, reduce log retention

### Issue: Slow Response Times
**Solution:**
- GCP: Set `min_instances = 1` to keep warm instance
- AWS: Increase ECS task count
- All: Enable CDN (CloudFront/Cloud CDN)

## Getting Help

### Documentation
- [AWS Deployment Guide](docs/deployment/AWS.md)
- [GCP Deployment Guide](docs/deployment/GCP.md)
- [Azure Deployment Guide](docs/deployment/AZURE.md)
- [Troubleshooting Guide](docs/deployment/TROUBLESHOOTING.md)

### Community
- **GitHub Issues:** Report bugs and request features
- **Vaultwarden Forum:** https://github.com/dani-garcia/vaultwarden/discussions
- **Bitwarden Community:** https://community.bitwarden.com/

### Commercial Support
- For enterprise support, contact: adrian207@gmail.com

## Success Checklist

Before considering your deployment complete:

- [ ] ✅ Vaultwarden accessible via HTTPS
- [ ] ✅ Master account created with strong password
- [ ] ✅ Admin token saved securely
- [ ] ✅ Public signups disabled
- [ ] ✅ 2FA enabled on admin account
- [ ] ✅ At least one client installed and working
- [ ] ✅ SMTP configured (optional but recommended)
- [ ] ✅ Backup verified
- [ ] ✅ Cost monitoring setup
- [ ] ✅ DNS configured (if using custom domain)

## Security Best Practices

1. **Master Password:** Use 16+ characters, unique, never reused
2. **Admin Token:** Store in password manager, rotate quarterly
3. **2FA:** Enable on all accounts
4. **Backups:** Verify monthly, test restoration quarterly
5. **Updates:** Apply Vaultwarden updates within 30 days
6. **Monitoring:** Review access logs monthly
7. **Signups:** Keep disabled, use invitations only
8. **SMTP:** Use dedicated email account
9. **Domain:** Use HTTPS only, never HTTP
10. **Secrets:** Never commit to git

---

**🎉 Congratulations!** You now have a production-ready, self-hosted password manager that scales automatically and costs a fraction of commercial alternatives.

**Next Steps:** Start migrating your passwords and enjoy the freedom of self-hosting!

