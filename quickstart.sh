#!/bin/bash
##
## Vaultwarden Serverless Quick Start
## Author: Adrian Johnson <adrian207@gmail.com>
##
## This script helps you choose and deploy Vaultwarden to your preferred cloud provider
##

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║        Vaultwarden Serverless Deployment                     ║"
echo "║        Self-Hosted Password Manager                          ║"
echo "║                                                               ║"
echo "║        Author: Adrian Johnson <adrian207@gmail.com>          ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${BLUE}Welcome to the Vaultwarden Serverless deployment wizard!${NC}"
echo ""
echo "This script will help you deploy a production-ready password manager"
echo "on AWS or GCP with automatic scaling to 100,000+ users."
echo ""

# Function to print info
print_info() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print section header
print_header() {
    echo ""
    echo -e "${BLUE}═══ $1 ═══${NC}"
    echo ""
}

# Check prerequisites
check_prereqs() {
    print_header "Checking Prerequisites"
    
    local missing=0
    
    if command -v terraform &> /dev/null; then
        print_info "Terraform found: $(terraform version | head -n1)"
    else
        echo "✗ Terraform not found - Install from: https://terraform.io/downloads"
        missing=1
    fi
    
    if command -v git &> /dev/null; then
        print_info "Git found: $(git --version)"
    else
        echo "✗ Git not found - Install from: https://git-scm.com/downloads"
        missing=1
    fi
    
    if [ $missing -eq 1 ]; then
        echo ""
        echo "Please install missing prerequisites and run this script again."
        exit 1
    fi
    
    echo ""
    print_info "All prerequisites met!"
}

# Choose cloud provider
choose_provider() {
    print_header "Choose Cloud Provider"
    
    echo "Which cloud provider would you like to use?"
    echo ""
    echo "  1) GCP (Google Cloud Platform)"
    echo "     • Lowest cost: \$15-45/month"
    echo "     • Scales to zero when idle"
    echo "     • Fastest deployment: 15 minutes"
    echo "     • Best for: Personal use, small teams"
    echo ""
    echo "  2) AWS (Amazon Web Services)"
    echo "     • Enterprise-grade: \$30-60/month"
    echo "     • Maximum control and features"
    echo "     • Deployment time: 20 minutes"
    echo "     • Best for: Enterprises, teams"
    echo ""
    echo "  3) Exit"
    echo ""
    
    while true; do
        read -p "Enter your choice (1-3): " choice
        case $choice in
            1)
                PROVIDER="gcp"
                PROVIDER_NAME="Google Cloud Platform"
                break
                ;;
            2)
                PROVIDER="aws"
                PROVIDER_NAME="Amazon Web Services"
                break
                ;;
            3)
                echo "Goodbye!"
                exit 0
                ;;
            *)
                echo "Invalid choice. Please enter 1, 2, or 3."
                ;;
        esac
    done
    
    echo ""
    print_info "Selected: $PROVIDER_NAME"
}

# Check cloud CLI
check_cloud_cli() {
    print_header "Checking Cloud CLI"
    
    if [ "$PROVIDER" == "gcp" ]; then
        if command -v gcloud &> /dev/null; then
            print_info "gcloud CLI found"
            
            if gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
                ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1)
                print_info "Authenticated as: $ACCOUNT"
            else
                echo ""
                echo "You need to authenticate with GCP."
                read -p "Run 'gcloud auth login' now? (y/n): " auth_choice
                if [ "$auth_choice" == "y" ]; then
                    gcloud auth login
                else
                    echo "Please run 'gcloud auth login' manually and restart this script."
                    exit 1
                fi
            fi
        else
            echo "✗ gcloud CLI not found"
            echo "Install from: https://cloud.google.com/sdk/docs/install"
            exit 1
        fi
    elif [ "$PROVIDER" == "aws" ]; then
        if command -v aws &> /dev/null; then
            print_info "AWS CLI found"
            
            if aws sts get-caller-identity &> /dev/null; then
                ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
                print_info "Authenticated - Account: $ACCOUNT"
            else
                echo ""
                echo "You need to configure AWS credentials."
                read -p "Run 'aws configure' now? (y/n): " aws_choice
                if [ "$aws_choice" == "y" ]; then
                    aws configure
                else
                    echo "Please run 'aws configure' manually and restart this script."
                    exit 1
                fi
            fi
        else
            echo "✗ AWS CLI not found"
            echo "Install from: https://aws.amazon.com/cli/"
            exit 1
        fi
    fi
}

# Show next steps
show_next_steps() {
    print_header "Next Steps"
    
    echo "Great! You're ready to deploy Vaultwarden."
    echo ""
    echo "Follow these steps:"
    echo ""
    echo "1. Navigate to the infrastructure directory:"
    echo "   ${GREEN}cd infrastructure/$PROVIDER${NC}"
    echo ""
    echo "2. Copy and configure the example settings:"
    echo "   ${GREEN}cp terraform.tfvars.example terraform.tfvars${NC}"
    echo "   ${GREEN}nano terraform.tfvars${NC}  # or use your preferred editor"
    echo ""
    
    if [ "$PROVIDER" == "gcp" ]; then
        echo "3. Required configuration:"
        echo "   - project_id: Your GCP project ID"
        echo "   - domain_name: Your domain (optional, can use Cloud Run URL)"
        echo ""
    elif [ "$PROVIDER" == "aws" ]; then
        echo "3. Required configuration:"
        echo "   - domain_name: Your domain"
        echo "   - certificate_arn: ACM certificate ARN (create first)"
        echo ""
        echo "   To create certificate:"
        echo "   ${GREEN}aws acm request-certificate --domain-name vault.example.com --validation-method DNS${NC}"
        echo ""
    fi
    
    echo "4. Deploy using the automated script:"
    echo "   ${GREEN}cd ../..${NC}  # Return to project root"
    echo "   ${GREEN}./scripts/deploy-$PROVIDER.sh${NC}"
    echo ""
    echo "   OR deploy manually:"
    echo "   ${GREEN}cd infrastructure/$PROVIDER${NC}"
    echo "   ${GREEN}terraform init${NC}"
    echo "   ${GREEN}terraform plan${NC}"
    echo "   ${GREEN}terraform apply${NC}"
    echo ""
    echo "5. After deployment:"
    echo "   • Access the URL shown in output"
    echo "   • Create your admin account"
    echo "   • Retrieve admin token: ${GREEN}terraform output -raw admin_token${NC}"
    echo "   • Access admin panel: https://your-url/admin"
    echo "   • Disable public signups"
    echo "   • Install Bitwarden clients"
    echo ""
    
    print_header "Documentation"
    echo ""
    echo "📖 Complete Guides:"
    echo "   • Getting Started: docs/GETTING_STARTED.md"
    echo "   • $PROVIDER_NAME Guide: docs/deployment/$(echo $PROVIDER | tr '[:lower:]' '[:upper:]').md"
    echo "   • Project Summary: PROJECT_SUMMARY.md"
    echo ""
    
    print_header "Estimated Costs (Scales 1 to 100,000+ Users)"
    echo ""
    if [ "$PROVIDER" == "gcp" ]; then
        echo "  📊 GCP Scaling Tiers:"
        echo "     1-10 users:        \$15-25/month"
        echo "     10-100 users:      \$35-60/month"
        echo "     100-1K users:      \$120-180/month"
        echo "     1K-10K users:      \$400-600/month"
        echo "     10K-50K users:     \$1,500-2,500/month"
        echo "     50K-100K+ users:   \$5,000-8,000/month"
        echo ""
        echo "  💰 Scales to \$0 when completely idle!"
    elif [ "$PROVIDER" == "aws" ]; then
        echo "  📊 AWS Scaling Tiers:"
        echo "     1-10 users:        \$30-45/month"
        echo "     10-100 users:      \$60-90/month"
        echo "     100-1K users:      \$180-260/month"
        echo "     1K-10K users:      \$600-900/month"
        echo "     10K-50K users:     \$2,500-4,000/month"
        echo "     50K-100K+ users:   \$8,000-15,000/month"
    fi
    echo ""
    echo "  Compare to 1Password Teams: \$19.95/user/month"
    echo "     10 users = \$199.50/month (\$2,394/year)"
    echo "     1,000 users = \$19,950/month (\$239,400/year)"
    echo "     10,000 users = \$199,500/month (\$2,394,000/year)"
    echo ""
    echo "  💰 At 1,000 users, save \$237,240/year vs 1Password!"
    echo "  💰 At 10,000 users, save \$2.38M/year vs 1Password!"
    echo ""
    echo "  📖 Full scaling details: SCALING_QUICK_REFERENCE.md"
    echo ""
    
    print_header "Support"
    echo ""
    echo "Need help?"
    echo "  • Documentation: All guides in docs/ folder"
    echo "  • Issues: https://github.com/your-repo/issues"
    echo "  • Email: adrian207@gmail.com"
    echo ""
    
    read -p "Press Enter to open the deployment guide..."
    
    if [ "$PROVIDER" == "gcp" ]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open docs/deployment/GCP.md
        elif command -v open &> /dev/null; then
            open docs/deployment/GCP.md
        else
            echo "Please open: docs/deployment/GCP.md"
        fi
    elif [ "$PROVIDER" == "aws" ]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open docs/deployment/AWS.md
        elif command -v open &> /dev/null; then
            open docs/deployment/AWS.md
        else
            echo "Please open: docs/deployment/AWS.md"
        fi
    fi
    
    echo ""
    echo -e "${GREEN}Good luck with your deployment! 🚀${NC}"
    echo ""
}

# Main flow
main() {
    check_prereqs
    choose_provider
    check_cloud_cli
    show_next_steps
}

main

