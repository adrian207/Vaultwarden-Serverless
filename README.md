# Vaultwarden-Serverless

Terraform for running [Vaultwarden](https://github.com/dani-garcia/vaultwarden), the open-source Bitwarden-compatible password server, on managed, autoscaling cloud services: ECS Fargate with Aurora Serverless v2 on AWS, or Cloud Run with Cloud SQL on Google Cloud. The official Bitwarden apps and browser extensions connect to it as they would to Bitwarden.

## What it builds

| | AWS (`infrastructure/aws`) | Google Cloud (`infrastructure/gcp`) |
|---|---|---|
| Application | ECS Fargate service behind an Application Load Balancer, 2 tasks by default, autoscaling 1–10 | Cloud Run (v2), scales 0–10 instances |
| Database | Aurora PostgreSQL Serverless v2 (0.5–4 ACU) | Cloud SQL PostgreSQL 15 (`db-f1-micro`), private IP |
| Attachments | S3 bucket (versioned, encrypted, private) | Cloud Storage bucket |
| Secrets | Secrets Manager (database connection and a generated admin token) | Secret Manager (generated admin token) |
| Edge | CloudFront and AWS WAF | Cloud Armor security policy |
| Network | VPC with public and private subnets, NAT gateway, flow logs | VPC, subnet and Serverless VPC Access connector |
| Operations | CloudWatch logs and alarms, AWS Backup plan | Cloud Run logging |

Both use the upstream `vaultwarden/server` image by default (`vaultwarden_image` / `container_image`). `docker/Dockerfile` adds a health check on top of it if you want to build your own.

## Requirements

- Terraform 1.5 or later
- **AWS:** the AWS CLI configured for an account where you can create VPC, ECS, RDS, CloudFront and WAF resources
- **Google Cloud:** the gcloud CLI, signed in, with a project and billing enabled
- A domain name if you want your own hostname and certificate

## Quick start

`./quickstart.sh` checks the tools, lets you pick AWS or Google Cloud, offers to sign in, and prints the next steps. Or deploy directly:

```bash
git clone https://github.com/adrian207/Vaultwarden-Serverless.git
cd Vaultwarden-Serverless/infrastructure/aws        # or infrastructure/gcp

cp terraform.tfvars.example terraform.tfvars        # set region, domain and sizes
terraform init
terraform plan
terraform apply
terraform output
```

`scripts/deploy-aws.sh` and `scripts/deploy-gcp.sh` run the same steps and ask for confirmation before applying. After deployment, create your account, then set `signups_allowed = false` and apply again. The `/admin` page uses the generated admin token stored in Secrets Manager or Secret Manager.

Sizing presets are in [infrastructure/aws/SCALING_PRESETS.md](infrastructure/aws/SCALING_PRESETS.md) and [infrastructure/gcp/SCALING_PRESETS.md](infrastructure/gcp/SCALING_PRESETS.md); deployment guides in [docs/deployment/AWS.md](docs/deployment/AWS.md) and [docs/deployment/GCP.md](docs/deployment/GCP.md).

### Continuous deployment

`.github/workflows/deploy-gcp.yml` runs `terraform apply` for Google Cloud when `infrastructure/gcp/` changes on `main`, using repository secrets for credentials. `security-scan.yml` runs tfsec and a dependency scan on pushes and pull requests to `main` and weekly.

## Repository layout

```
infrastructure/aws/          Root module and networking, compute, database and storage modules
infrastructure/gcp/          Single-file Cloud Run configuration
docker/                      Optional custom image with a health check
scripts/                     deploy-aws.sh, deploy-gcp.sh
quickstart.sh                Interactive setup helper
backend/secrets-management/  Separate prototype API (see below)
docs/                        Deployment, scaling and compliance guides, and plans for future features
```

## Status and limitations

- **No Azure version.** Earlier documentation described one; only AWS and Google Cloud are implemented.
- **Secrets-management prototype.** `backend/secrets-management/` is a FastAPI service for storing application secrets with service-account API keys, written as phase 1 of a DevOps secrets feature. It is not part of the Vaultwarden deployment and the Terraform does not deploy it. See its [README](backend/secrets-management/README.md).
- **Plans, not features.** The documents under `docs/extensions`, `docs/mobile`, `docs/sso`, `docs/organizations`, `docs/reporting` and `docs/features` describe planned additions. They are not implemented in this repository; Vaultwarden itself provides organizations, Send and the standard Bitwarden apps.
- The configurations pass `terraform validate`; they have not been applied end to end from this repository. Costs depend on traffic and region; check current pricing.

## License

MIT. See [LICENSE](LICENSE). Vaultwarden is a separate project under the AGPL-3.0 license.

## Author

Adrian Johnson · [github.com/adrian207](https://github.com/adrian207)
