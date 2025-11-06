# Contributing to Vaultwarden Serverless Deployment

**Author:** Adrian Johnson <adrian207@gmail.com>

Thank you for considering contributing to this project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues

1. **Search existing issues** to avoid duplicates
2. **Use issue templates** when available
3. **Provide details:**
   - Cloud provider (AWS/GCP/Azure)
   - Terraform version
   - Error messages and logs
   - Steps to reproduce

### Suggesting Enhancements

1. **Check existing feature requests** first
2. **Describe the use case** clearly
3. **Explain the expected behavior**
4. **Consider backwards compatibility**

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly** on at least one cloud provider
5. **Update documentation** if needed
6. **Commit with clear messages:**
   ```
   feat: Add Azure Container Instances support
   
   - Implement Terraform modules for ACI
   - Add deployment documentation
   - Include cost estimation
   ```
7. **Push to your fork:** `git push origin feature/your-feature-name`
8. **Open a Pull Request** with description

## Development Guidelines

### Terraform Code Standards

1. **Use consistent naming:**
   ```hcl
   resource "aws_s3_bucket" "attachments" {
     bucket_prefix = "${local.name_prefix}-attachments-"
     # ...
   }
   ```

2. **Add comments for complex logic:**
   ```hcl
   # Calculate the number of NAT gateways based on availability zones
   # One NAT gateway per AZ for high availability
   resource "aws_nat_gateway" "main" {
     count = length(var.availability_zones)
     # ...
   }
   ```

3. **Use variables for configurability:**
   ```hcl
   variable "enable_waf" {
     description = "Enable AWS WAF for DDoS protection"
     type        = bool
     default     = true
   }
   ```

4. **Include outputs for important values:**
   ```hcl
   output "vaultwarden_url" {
     description = "Vaultwarden application URL"
     value       = module.compute.alb_dns_name
   }
   ```

5. **Format code:** `terraform fmt -recursive`

### Documentation Standards

1. **Use Minto Pyramid Principle:**
   - Start with the conclusion/summary
   - Support with key arguments
   - Provide detailed evidence

2. **Include code examples:**
   ```bash
   # Good: Specific, actionable command
   terraform apply -var="environment=prod"
   
   # Bad: Vague instruction
   # Deploy the infrastructure
   ```

3. **Add author attribution:**
   ```markdown
   **Author:** Adrian Johnson <adrian207@gmail.com>
   ```

4. **Label unverified claims:**
   ```markdown
   [Inference] Cold start times are approximately 2-3 seconds based on observed patterns.
   ```

### Security Guidelines

1. **Never commit secrets** to git
2. **Use secrets management** services
3. **Enable encryption** by default
4. **Follow least privilege** principle
5. **Document security implications**

### Testing Checklist

Before submitting a PR, verify:

- [ ] Terraform code passes `terraform validate`
- [ ] Code is formatted with `terraform fmt`
- [ ] Documentation is updated
- [ ] Tested on at least one cloud provider
- [ ] No secrets or credentials committed
- [ ] Variables have descriptions
- [ ] Outputs are documented
- [ ] Security scan passes (tfsec)

## Project Structure

```
vaultwarden-serverless/
├── infrastructure/
│   ├── aws/              # AWS-specific Terraform
│   ├── azure/            # Azure-specific Terraform
│   ├── gcp/              # GCP-specific Terraform
│   └── modules/          # Reusable Terraform modules
├── docs/
│   ├── deployment/       # Cloud-specific deployment guides
│   ├── configuration/    # Configuration documentation
│   └── operations/       # Operational procedures
├── scripts/              # Deployment automation scripts
├── .github/workflows/    # CI/CD pipelines
└── docker/               # Custom Docker configurations
```

## Code of Conduct

1. **Be respectful** and inclusive
2. **Provide constructive feedback**
3. **Focus on the issue**, not the person
4. **Help others learn** and grow
5. **Credit contributors** appropriately

## Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open a GitHub Issue
- **Security:** Email adrian207@gmail.com directly
- **Urgent:** Tag @adrian207 in issue

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README (for significant contributions)

Thank you for making this project better! 🙏

