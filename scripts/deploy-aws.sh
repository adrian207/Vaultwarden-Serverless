#!/bin/bash
##
## AWS Vaultwarden Deployment Script
## Author: Adrian Johnson <adrian207@gmail.com>
##
## This script automates the deployment of Vaultwarden on AWS using Terraform.
##

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform not found. Please install Terraform 1.5+"
        exit 1
    fi
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI not found. Please install AWS CLI"
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials not configured. Run 'aws configure'"
        exit 1
    fi
    
    print_info "All prerequisites met ✓"
}

# Initialize Terraform
init_terraform() {
    print_info "Initializing Terraform..."
    cd infrastructure/aws
    terraform init
    print_info "Terraform initialized ✓"
}

# Validate configuration
validate_config() {
    print_info "Validating Terraform configuration..."
    
    if [ ! -f "terraform.tfvars" ]; then
        print_error "terraform.tfvars not found!"
        print_info "Copy terraform.tfvars.example to terraform.tfvars and configure it"
        exit 1
    fi
    
    terraform validate
    print_info "Configuration valid ✓"
}

# Create SSL certificate (if needed)
create_certificate() {
    print_info "Checking SSL certificate..."
    
    # Extract domain from tfvars
    DOMAIN=$(grep "domain_name" terraform.tfvars | cut -d '"' -f 2)
    
    if [ -z "$DOMAIN" ]; then
        print_warn "Domain not configured in terraform.tfvars"
        return
    fi
    
    print_info "Domain: $DOMAIN"
    print_warn "Ensure you have a valid ACM certificate for this domain"
    print_warn "Create one with: aws acm request-certificate --domain-name $DOMAIN --validation-method DNS"
}

# Run Terraform plan
run_plan() {
    print_info "Running Terraform plan..."
    terraform plan -out=tfplan
    
    echo ""
    read -p "Review the plan above. Continue with deployment? (yes/no): " CONFIRM
    
    if [ "$CONFIRM" != "yes" ]; then
        print_warn "Deployment cancelled"
        exit 0
    fi
}

# Apply Terraform
run_apply() {
    print_info "Deploying infrastructure..."
    terraform apply tfplan
    print_info "Deployment complete ✓"
}

# Display outputs
show_outputs() {
    echo ""
    print_info "============================================"
    print_info "         DEPLOYMENT COMPLETE!"
    print_info "============================================"
    echo ""
    
    terraform output -raw post_deployment_steps
    
    echo ""
    print_info "To retrieve the admin token:"
    echo "terraform output -raw admin_token"
    echo ""
}

# Main deployment flow
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════╗"
    echo "║   Vaultwarden AWS Serverless Deployment         ║"
    echo "║   Author: Adrian Johnson <adrian207@gmail.com>  ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""
    
    check_prerequisites
    init_terraform
    validate_config
    create_certificate
    run_plan
    run_apply
    show_outputs
    
    print_info "Deployment successful! 🎉"
}

# Run main function
main

