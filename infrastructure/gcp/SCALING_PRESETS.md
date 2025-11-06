# GCP Scaling Tier Presets

**Author:** Adrian Johnson <adrian207@gmail.com>

Quick reference configurations for each scaling tier. Copy the appropriate settings to your `terraform.tfvars` file.

## Tier 0: Personal (1-10 users) - $15-25/month

```hcl
# Compute (scales to zero!)
container_cpu           = "1"
container_memory        = "512Mi"
min_instances          = 0      # Scale to zero
max_instances          = 2

# Database
db_tier                = "db-f1-micro"
db_high_availability   = false
```

**Cost breakdown:**
- Cloud Run: $0-5 (idle most of time)
- Cloud SQL: $7-10
- Storage: $1-2
- Networking: $3-5

## Tier 1: Small Team (10-100 users) - $35-60/month

```hcl
# Compute
container_cpu           = "2"
container_memory        = "1Gi"
min_instances          = 1      # Keep warm
max_instances          = 5

# Database
db_tier                = "db-g1-small"
db_high_availability   = false
```

**Cost breakdown:**
- Cloud Run: $15-25 (1-2 instances avg)
- Cloud SQL: $15-20
- Storage: $2-3
- VPC Connector: $7-10
- Networking: $3-5

## Tier 2: Medium Organization (100-1K users) - $120-180/month

```hcl
# Compute
container_cpu           = "2"
container_memory        = "2Gi"
min_instances          = 2      # Always 2+ running
max_instances          = 15

# Database
db_tier                = "db-n1-standard-1"  # 1 vCPU, 3.75 GB
db_high_availability   = true               # Enable HA
```

**Cost breakdown:**
- Cloud Run: $60-90 (3-5 instances avg)
- Cloud SQL: $50-70 (HA enabled)
- Storage: $5-10
- Networking: $5-10

## Tier 3: Large Enterprise (1K-10K users) - $400-600/month

```hcl
# Compute
container_cpu           = "4"
container_memory        = "4Gi"
min_instances          = 5
max_instances          = 30

# Database
db_tier                = "db-n1-standard-2"  # 2 vCPU, 7.5 GB
db_high_availability   = true

# Add to main.tf:
# Read replicas: 2
# Memorystore Redis
# Cloud CDN
```

**Cost breakdown:**
- Cloud Run: $250-350 (10-15 instances)
- Cloud SQL: $120-180 (HA + replicas)
- Memorystore: $50-80
- Storage: $20-30
- CDN: $10-20

## Tier 4: Very Large (10K-50K users) - $1,500-2,500/month

```hcl
# Compute
container_cpu           = "4"
container_memory        = "8Gi"
min_instances          = 10
max_instances          = 60

# Database
db_tier                = "db-n1-standard-4"  # 4 vCPU, 15 GB
db_high_availability   = true

# Required additions:
# - Multi-region deployment (3 regions)
# - Memorystore HA (10 GB)
# - Cloud CDN globally
# - Cloud Armor advanced
```

**Cost breakdown:**
- Cloud Run: $800-1,200 (multi-region)
- Cloud SQL: $400-600 (HA + replicas)
- Memorystore: $100-150
- Storage: $50-100
- CDN: $50-100
- Networking: $100-200

## Tier 5: Massive Scale (50K-100K+ users) - $5,000-8,000/month

```hcl
# Compute
container_cpu           = "8"
container_memory        = "16Gi"
min_instances          = 20
max_instances          = 100

# Database
db_tier                = "db-n1-standard-8"  # 8 vCPU, 30 GB
db_high_availability   = true

# Required infrastructure:
# - 4+ region deployment
# - Cloud SQL replicas (3 per region)
# - Memorystore HA (50 GB, 5 replicas)
# - Global load balancing
# - Cloud Armor Premium
# - Optional: Cloud Spanner for global consistency
```

**Cost breakdown:**
- Cloud Run: $2,500-4,000 (multi-region)
- Cloud SQL: $1,500-2,000 (global)
- Memorystore: $500-700
- Global LB: $200-300
- Storage: $200-300
- CDN: $200-400
- Cloud Armor: $100-200
- Networking: $300-500

## Quick Migration Between Tiers

1. Update `terraform.tfvars` with new tier settings
2. Run `terraform plan` to preview changes
3. Run `terraform apply`
4. Cloud Run performs zero-downtime rolling update

**Example:** Tier 1 → Tier 2
```bash
# Edit terraform.tfvars
terraform plan -out=upgrade.tfplan
terraform apply upgrade.tfplan
```

Deployment time: 3-5 minutes  
Downtime: None (automatic)

## Cost Optimization Tips

### Tier 0-1
- Set `min_instances = 0` to scale to zero
- Use smallest DB tier that handles load
- Monitor and adjust based on actual usage

### Tier 2-3
- Enable committed use discounts (30-70% off)
- Use Cloud SQL automatic storage increase
- Implement Cloud CDN for static assets

### Tier 4-5
- Use enterprise discounts (contact sales)
- Optimize database queries and indexes
- Implement aggressive caching strategy
- Use committed use for predictable workloads

