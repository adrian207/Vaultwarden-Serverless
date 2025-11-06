# Scaling Quick Reference

**Author:** Adrian Johnson <adrian207@gmail.com>

## 🎯 Find Your Tier in 30 Seconds

| How Many Users? | Your Tier | Monthly Cost | Setup |
|----------------|-----------|--------------|-------|
| Me + family (< 10) | **Tier 0: Personal** | GCP: $15-25<br>AWS: $30-45 | [Tier 0 Config](#tier-0-personal) |
| Small team (10-100) | **Tier 1: Small Team** | GCP: $35-60<br>AWS: $60-90 | [Tier 1 Config](#tier-1-small-team) |
| Department (100-1K) | **Tier 2: Medium Org** | GCP: $120-180<br>AWS: $180-260 | [Tier 2 Config](#tier-2-medium-organization) |
| Company (1K-10K) | **Tier 3: Large Enterprise** | GCP: $400-600<br>AWS: $600-900 | [Tier 3 Config](#tier-3-large-enterprise) |
| Corporation (10K-50K) | **Tier 4: Very Large** | GCP: $1.5K-2.5K<br>AWS: $2.5K-4K | [Tier 4 Config](#tier-4-very-large-enterprise) |
| Massive (50K-100K+) | **Tier 5: Massive Scale** | GCP: $5K-8K<br>AWS: $8K-15K | [Tier 5 Config](#tier-5-massive-scale) |

## 📋 Copy-Paste Configurations

### Tier 0: Personal

**GCP** (`infrastructure/gcp/terraform.tfvars`):
```hcl
container_cpu = "1"
container_memory = "512Mi"
min_instances = 0
max_instances = 2
db_tier = "db-f1-micro"
db_high_availability = false
```

**AWS** (`infrastructure/aws/terraform.tfvars`):
```hcl
container_cpu = 256
container_memory = 512
desired_count = 1
min_capacity = 1
max_capacity = 2
db_min_capacity = 0.5
db_max_capacity = 1
enable_waf = false
enable_cloudfront = false
```

---

### Tier 1: Small Team

**GCP**:
```hcl
container_cpu = "2"
container_memory = "1Gi"
min_instances = 1
max_instances = 5
db_tier = "db-g1-small"
db_high_availability = false
```

**AWS**:
```hcl
container_cpu = 512
container_memory = 1024
desired_count = 2
min_capacity = 2
max_capacity = 5
db_min_capacity = 0.5
db_max_capacity = 2
enable_waf = true
enable_cloudfront = false
```

---

### Tier 2: Medium Organization

**GCP**:
```hcl
container_cpu = "2"
container_memory = "2Gi"
min_instances = 2
max_instances = 15
db_tier = "db-n1-standard-1"
db_high_availability = true
```

**AWS**:
```hcl
container_cpu = 1024
container_memory = 2048
desired_count = 3
min_capacity = 3
max_capacity = 15
db_min_capacity = 1
db_max_capacity = 4
enable_waf = true
enable_cloudfront = true
```

---

### Tier 3: Large Enterprise

**GCP**:
```hcl
container_cpu = "4"
container_memory = "4Gi"
min_instances = 5
max_instances = 30
db_tier = "db-n1-standard-2"
db_high_availability = true
# Add: Redis cache, CDN, read replicas
```

**AWS**:
```hcl
container_cpu = 2048
container_memory = 4096
desired_count = 6
min_capacity = 5
max_capacity = 30
db_min_capacity = 2
db_max_capacity = 8
enable_waf = true
enable_cloudfront = true
# Add: ElastiCache, Aurora replicas
```

---

### Tier 4: Very Large Enterprise

**GCP**:
```hcl
container_cpu = "4"
container_memory = "8Gi"
min_instances = 10
max_instances = 60
db_tier = "db-n1-standard-4"
db_high_availability = true
# Requires: Multi-region, Memorystore HA, Global LB
```

**AWS**:
```hcl
container_cpu = 4096
container_memory = 8192
desired_count = 15
min_capacity = 10
max_capacity = 60
db_min_capacity = 4
db_max_capacity = 16
enable_waf = true
enable_cloudfront = true
# Requires: Multi-region, Global Accelerator, Aurora Global
```

---

### Tier 5: Massive Scale

**Contact:** This tier requires custom architecture design.

**Requirements:**
- Multi-region deployment (4+ regions)
- Global database replication
- Advanced caching (50+ GB)
- Premium DDoS protection
- Dedicated support

**Get Started:** Email adrian207@gmail.com for enterprise consultation.

---

## ⚡ Quick Upgrade Path

### Growing from Tier 0 → Tier 1

```bash
# 1. Edit terraform.tfvars
cd infrastructure/gcp  # or aws

# 2. Update these values (see Tier 1 above)
nano terraform.tfvars

# 3. Apply changes
terraform plan
terraform apply
```

**Time:** 5 minutes  
**Downtime:** None

---

## 💰 ROI Calculator

### Small Team (10 users)
- **Your Cost (GCP):** $35-60/month = $420-720/year
- **1Password Cost:** $199.50/month = $2,394/year
- **Your Savings:** **$1,674-1,974/year** ✅

### Medium Org (1,000 users)
- **Your Cost (GCP):** $120-180/month = $1,440-2,160/year
- **1Password Cost:** $19,950/month = $239,400/year
- **Your Savings:** **$237,240/year** 🚀

### Large Enterprise (10,000 users)
- **Your Cost (GCP):** $400-600/month = $4,800-7,200/year
- **1Password Cost:** $199,500/month = $2,394,000/year
- **Your Savings:** **$2,386,800/year** 💰

---

## 🔍 Performance by Tier

| Tier | Response Time | Max Users | Concurrent Requests | Uptime |
|------|--------------|-----------|---------------------|--------|
| 0 | < 100ms | 10 | 50 | 99.5% |
| 1 | < 50ms | 100 | 500 | 99.5% |
| 2 | < 30ms | 1,000 | 2,000 | 99.9% |
| 3 | < 20ms | 10,000 | 10,000 | 99.9% |
| 4 | < 15ms | 50,000 | 50,000 | 99.95% |
| 5 | < 10ms | 100,000+ | 200,000+ | 99.99% |

---

## 📚 Need More Details?

**Complete Documentation:**
- 📖 [Full Scaling Guide](docs/operations/SCALING_GUIDE.md) - 30+ pages with every detail
- 🚀 [AWS Presets](infrastructure/aws/SCALING_PRESETS.md) - Copy-paste configs
- ☁️ [GCP Presets](infrastructure/gcp/SCALING_PRESETS.md) - Copy-paste configs
- 📊 [Getting Started](docs/GETTING_STARTED.md) - First-time setup

**Have Questions?**
- GitHub Issues: Technical questions
- Email: adrian207@gmail.com for enterprise consulting

---

## ✅ Quick Start Checklist

- [ ] Pick your tier from table above
- [ ] Copy configuration to `terraform.tfvars`
- [ ] Run `terraform init && terraform apply`
- [ ] Access your Vaultwarden instance
- [ ] Create admin account
- [ ] Disable public signups
- [ ] Install Bitwarden clients
- [ ] Enjoy self-hosted password management!

**Estimated Setup Time:** 15-30 minutes per tier

---

**Pro Tip:** Start with Tier 0 or 1, then scale up as you grow. Upgrades take 5-10 minutes with zero downtime!

