#!/bin/bash
##
## GCP Vaultwarden Deployment Script
## Author: Adrian Johnson <adrian207@gmail.com>
##

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform not found. Install from https://terraform.io"
        exit 1
    fi
    
    if ! command -v gcloud &> /dev/null; then
        print_error "gcloud CLI not found. Install from https://cloud.google.com/sdk"
        exit 1
    fi
    
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
        print_error "Not authenticated to GCP. Run: gcloud auth login"
        exit 1
    fi
    
    print_info "Prerequisites met ✓"
}

init_terraform() {
    print_info "Initializing Terraform..."
    cd infrastructure/gcp
    terraform init
    print_info "Terraform initialized ✓"
}

validate_config() {
    print_info "Validating configuration..."
    
    if [ ! -f "terraform.tfvars" ]; then
        print_error "terraform.tfvars not found!"
        print_info "Copy terraform.tfvars.example and configure it"
        exit 1
    fi
    
    terraform validate
    print_info "Configuration valid ✓"
}

enable_apis() {
    print_info "Enabling required GCP APIs..."
    
    PROJECT_ID=$(grep "project_id" terraform.tfvars | cut -d '"' -f 2)
    
    gcloud services enable \
        run.googleapis.com \
        sqladmin.googleapis.com \
        compute.googleapis.com \
        servicenetworking.googleapis.com \
        secretmanager.googleapis.com \
        --project=$PROJECT_ID
    
    print_info "APIs enabled ✓"
}

run_plan() {
    print_info "Running Terraform plan..."
    terraform plan -out=tfplan
    
    echo ""
    read -p "Continue with deployment? (yes/no): " CONFIRM
    
    if [ "$CONFIRM" != "yes" ]; then
        print_warn "Deployment cancelled"
        exit 0
    fi
}

run_apply() {
    print_info "Deploying infrastructure..."
    terraform apply tfplan
    print_info "Deployment complete ✓"
}

show_outputs() {
    echo ""
    print_info "============================================"
    print_info "         DEPLOYMENT COMPLETE!"
    print_info "============================================"
    echo ""
    
    terraform output -raw post_deployment_steps
    
    echo ""
    print_info "Admin token:"
    terraform output -raw admin_token
    echo ""
}

main() {
    echo ""
    echo "╔══════════════════════════════════════════════════╗"
    echo "║   Vaultwarden GCP Serverless Deployment         ║"
    echo "║   Author: Adrian Johnson <adrian207@gmail.com>  ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""
    
    check_prerequisites
    init_terraform
    validate_config
    enable_apis
    run_plan
    run_apply
    show_outputs
    
    print_info "Deployment successful! 🎉"
}

main

