# AWS Scaling Tier Presets

**Author:** Adrian Johnson <adrian207@gmail.com>

Quick reference configurations for each scaling tier. Copy the appropriate settings to your `terraform.tfvars` file.

## Tier 0: Personal (1-10 users) - $30-45/month

```hcl
# Basic configuration
container_cpu     = 256    # 0.25 vCPU
container_memory  = 512    # 512 MB
desired_count     = 1
min_capacity      = 1
max_capacity      = 2

# Database
db_min_capacity   = 0.5    # ACUs
db_max_capacity   = 1

# Features
enable_waf        = false  # Optional for personal use
enable_cloudfront = false
```

## Tier 1: Small Team (10-100 users) - $60-90/month

```hcl
# Compute
container_cpu     = 512    # 0.5 vCPU
container_memory  = 1024   # 1 GB
desired_count     = 2
min_capacity      = 2
max_capacity      = 5

# Database
db_min_capacity   = 0.5
db_max_capacity   = 2

# Features
enable_waf        = true
enable_cloudfront = false
```

## Tier 2: Medium Organization (100-1K users) - $180-260/month

```hcl
# Compute
container_cpu     = 1024   # 1 vCPU
container_memory  = 2048   # 2 GB
desired_count     = 3
min_capacity      = 3
max_capacity      = 15

# Database
db_min_capacity   = 1
db_max_capacity   = 4

# Features
enable_waf        = true
enable_cloudfront = true   # Enable CDN
```

## Tier 3: Large Enterprise (1K-10K users) - $600-900/month

```hcl
# Compute
container_cpu     = 2048   # 2 vCPU
container_memory  = 4096   # 4 GB
desired_count     = 6
min_capacity      = 5
max_capacity      = 30

# Database
db_min_capacity   = 2
db_max_capacity   = 8

# Features
enable_waf        = true
enable_cloudfront = true

# Add to main.tf:
# ElastiCache for session caching
# Aurora read replicas (2)
```

## Tier 4: Very Large (10K-50K users) - $2,500-4,000/month

```hcl
# Compute
container_cpu     = 4096   # 4 vCPU
container_memory  = 8192   # 8 GB
desired_count     = 15
min_capacity      = 10
max_capacity      = 60

# Database
db_min_capacity   = 4
db_max_capacity   = 16

# Features
enable_waf        = true
enable_cloudfront = true

# Required additions:
# - Multi-region deployment
# - Global Accelerator
# - ElastiCache cluster
# - Aurora Global Database
```

## Tier 5: Massive Scale (50K-100K+ users) - $8,000-15,000/month

```hcl
# Compute
container_cpu     = 8192   # 8 vCPU
container_memory  = 16384  # 16 GB
desired_count     = 30
min_capacity      = 20
max_capacity      = 100

# Database
db_min_capacity   = 8
db_max_capacity   = 32

# Required infrastructure:
# - 4+ region deployment
# - Aurora Global Database
# - ElastiCache Global Datastore
# - Route 53 health checks
# - AWS WAF with custom rules
# - Lambda@Edge for routing
```

## Quick Migration Between Tiers

1. Update `terraform.tfvars` with new tier settings
2. Run `terraform plan` to preview changes
3. Run `terraform apply` during low-traffic period
4. Monitor deployment (zero downtime)

**Example:** Tier 1 → Tier 2
```bash
# Edit terraform.tfvars (increase resources)
terraform plan -out=upgrade.tfplan
terraform apply upgrade.tfplan
```

Deployment time: 5-10 minutes  
Downtime: None (rolling update)

