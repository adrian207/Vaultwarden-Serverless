# SSO Setup Guide: Azure Active Directory

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Estimated Time:** 60-90 minutes  
**Difficulty:** Medium

## Overview

This guide walks you through integrating your Vaultwarden deployment with Azure Active Directory (Azure AD / Microsoft Entra ID) for Single Sign-On.

**What you'll build:**
```
User → Azure AD SSO → OAuth2 Proxy → Vaultwarden → Master Password → Vault Unlocked
```

---

## Prerequisites

- ✅ Vaultwarden deployed on GCP or AWS
- ✅ Azure AD tenant (P1/P2 for conditional access, Free for basic SSO)
- ✅ Azure AD admin access
- ✅ Domain verified in Azure AD
- ✅ GCP or AWS CLI configured

**Estimated Cost:**
- Azure AD Free: $0
- Azure AD Premium P1: $6/user/month
- OAuth2 Proxy infrastructure: $40-90/month

---

## Part 1: Azure AD Configuration (30 minutes)

### Step 1: Register Application

1. **Navigate to Azure Portal**
   - Go to [portal.azure.com](https://portal.azure.com)
   - Sign in with admin account

2. **Open Azure Active Directory**
   - Search "Azure Active Directory"
   - Click to open

3. **Register New Application**
   - Left menu → App registrations
   - Click "New registration"
   
4. **Configure Registration**
   - Name: `Vaultwarden SSO`
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI:
     - Platform: Web
     - URI: `https://vault.yourcompany.com/oauth2/callback`
   - Click "Register"

5. **Note Application Details**
   - **Application (client) ID:** Copy and save
   - **Directory (tenant) ID:** Copy and save (from Overview page)

✅ **Application registered!**

---

### Step 2: Create Client Secret

1. **Navigate to Certificates & secrets**
   - Your app → Certificates & secrets (left menu)

2. **Create New Client Secret**
   - Click "New client secret"
   - Description: `OAuth2 Proxy Secret`
   - Expires: 24 months (or custom)
   - Click "Add"

3. **Copy Secret Value**
   - ⚠️ **IMPORTANT:** Copy secret value NOW (shows once only)
   - Store securely (will use in next section)

✅ **Client secret created!**

---

### Step 3: Configure API Permissions

1. **Navigate to API permissions**
   - Your app → API permissions (left menu)

2. **Add Permission**
   - Click "Add a permission"
   - Select "Microsoft Graph"
   - Select "Delegated permissions"
   - Check: `User.Read` (basic profile)
   - Check: `email` (user email address)
   - Check: `openid` (OpenID Connect)
   - Check: `profile` (basic profile)
   - Click "Add permissions"

3. **Grant Admin Consent**
   - Click "Grant admin consent for [Your Organization]"
   - Confirm: Yes
   - Wait for green checkmarks

✅ **Permissions configured!**

---

### Step 4: Configure Token Settings (Optional but Recommended)

1. **Navigate to Token configuration**
   - Your app → Token configuration (left menu)

2. **Add Optional Claims**
   - Click "Add optional claim"
   - Token type: ID
   - Claims: Select `email`, `preferred_username`
   - Click "Add"

3. **Add Groups Claim (if using group restrictions)**
   - Click "Add groups claim"
   - Select: Security groups
   - ID token: Check
   - Access token: Check
   - Click "Add"

✅ **Token configuration complete!**

---

### Step 5: Configure Conditional Access (Optional - Premium P1/P2)

**Skip this if using Azure AD Free.**

1. **Navigate to Conditional Access**
   - Azure AD → Security → Conditional Access

2. **Create New Policy**
   - Click "New policy"
   - Name: `Vaultwarden MFA Required`

3. **Assign Users**
   - Users and groups → Include → All users
   - (Or select specific group: "Vaultwarden Users")

4. **Cloud Apps**
   - Cloud apps or actions → Include → Select apps
   - Search and select: "Vaultwarden SSO"

5. **Conditions (Examples)**
   - Locations: Any location OR specific countries
   - Device platforms: Any device
   - Client apps: Browser

6. **Grant**
   - Select "Grant access"
   - Check "Require multi-factor authentication"
   - Check "Require device to be marked as compliant" (optional)
   - For multiple controls: Require all selected controls
   - Click "Select"

7. **Enable Policy**
   - Enable policy: On
   - Click "Create"

✅ **Conditional access configured!**

---

## Part 2: Deploy OAuth2 Proxy (30 minutes)

### Option A: Deploy on GCP Cloud Run

**Step 1: Prepare Configuration**

```bash
# Set your variables
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
export SERVICE_NAME="vaultwarden-oauth2-proxy"

# Azure AD details (from Part 1)
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"

# Your Vaultwarden URL
export VAULTWARDEN_BACKEND_URL="https://vaultwarden-internal-xxxxx.run.app"

# Generate cookie secret
export COOKIE_SECRET=$(openssl rand -base64 32 | tr -d '\n')

# Your public domain
export PUBLIC_DOMAIN="vault.yourcompany.com"
```

**Step 2: Store Secrets in Secret Manager**

```bash
# Store client secret
echo -n "$AZURE_CLIENT_SECRET" | gcloud secrets create oauth2-client-secret \
  --data-file=- \
  --replication-policy=automatic

# Store cookie secret
echo -n "$COOKIE_SECRET" | gcloud secrets create oauth2-cookie-secret \
  --data-file=- \
  --replication-policy=automatic

# Create service account
gcloud iam service-accounts create oauth2-proxy-sa \
  --display-name="OAuth2 Proxy Service Account"

# Grant secret access
gcloud secrets add-iam-policy-binding oauth2-client-secret \
  --member="serviceAccount:oauth2-proxy-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding oauth2-cookie-secret \
  --member="serviceAccount:oauth2-proxy-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

**Step 3: Deploy to Cloud Run**

```bash
gcloud run deploy $SERVICE_NAME \
  --image quay.io/oauth2-proxy/oauth2-proxy:v7.5.1 \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --service-account="oauth2-proxy-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --cpu=1 \
  --memory=512Mi \
  --min-instances=1 \
  --max-instances=10 \
  --port=4180 \
  --set-env-vars="OAUTH2_PROXY_PROVIDER=oidc" \
  --set-env-vars="OAUTH2_PROXY_OIDC_ISSUER_URL=https://login.microsoftonline.com/${AZURE_TENANT_ID}/v2.0" \
  --set-env-vars="OAUTH2_PROXY_CLIENT_ID=${AZURE_CLIENT_ID}" \
  --set-env-vars="OAUTH2_PROXY_REDIRECT_URL=https://${PUBLIC_DOMAIN}/oauth2/callback" \
  --set-env-vars="OAUTH2_PROXY_UPSTREAMS=${VAULTWARDEN_BACKEND_URL}" \
  --set-env-vars="OAUTH2_PROXY_EMAIL_DOMAINS=*" \
  --set-env-vars="OAUTH2_PROXY_COOKIE_SECURE=true" \
  --set-env-vars="OAUTH2_PROXY_COOKIE_HTTPONLY=true" \
  --set-env-vars="OAUTH2_PROXY_COOKIE_SAMESITE=lax" \
  --set-env-vars="OAUTH2_PROXY_COOKIE_EXPIRE=24h" \
  --set-env-vars="OAUTH2_PROXY_COOKIE_REFRESH=1h" \
  --set-env-vars="OAUTH2_PROXY_SKIP_PROVIDER_BUTTON=true" \
  --set-env-vars="OAUTH2_PROXY_PASS_BASIC_AUTH=false" \
  --set-env-vars="OAUTH2_PROXY_PASS_ACCESS_TOKEN=true" \
  --set-env-vars="OAUTH2_PROXY_SET_XAUTHREQUEST=true" \
  --set-secrets="OAUTH2_PROXY_CLIENT_SECRET=oauth2-client-secret:latest" \
  --set-secrets="OAUTH2_PROXY_COOKIE_SECRET=oauth2-cookie-secret:latest"
```

✅ **OAuth2 Proxy deployed!**

---

### Option B: Deploy on AWS ECS Fargate

**Step 1: Store Secrets in AWS Secrets Manager**

```bash
# Set your region
export AWS_REGION="us-east-1"

# Store client secret
aws secretsmanager create-secret \
  --name oauth2-proxy/azure-client-secret \
  --secret-string "$AZURE_CLIENT_SECRET" \
  --region $AWS_REGION

# Store cookie secret
export COOKIE_SECRET=$(openssl rand -base64 32 | tr -d '\n')
aws secretsmanager create-secret \
  --name oauth2-proxy/cookie-secret \
  --secret-string "$COOKIE_SECRET" \
  --region $AWS_REGION

# Note the ARNs for use in task definition
```

**Step 2: Create Task Definition**

Create file: `oauth2-proxy-task.json`

```json
{
  "family": "vaultwarden-oauth2-proxy",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "oauth2-proxy",
      "image": "quay.io/oauth2-proxy/oauth2-proxy:v7.5.1",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 4180,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OAUTH2_PROXY_PROVIDER",
          "value": "oidc"
        },
        {
          "name": "OAUTH2_PROXY_OIDC_ISSUER_URL",
          "value": "https://login.microsoftonline.com/YOUR_TENANT_ID/v2.0"
        },
        {
          "name": "OAUTH2_PROXY_CLIENT_ID",
          "value": "YOUR_CLIENT_ID"
        },
        {
          "name": "OAUTH2_PROXY_REDIRECT_URL",
          "value": "https://vault.yourcompany.com/oauth2/callback"
        },
        {
          "name": "OAUTH2_PROXY_UPSTREAMS",
          "value": "http://vaultwarden-internal.local:8080"
        },
        {
          "name": "OAUTH2_PROXY_EMAIL_DOMAINS",
          "value": "*"
        },
        {
          "name": "OAUTH2_PROXY_COOKIE_SECURE",
          "value": "true"
        },
        {
          "name": "OAUTH2_PROXY_COOKIE_HTTPONLY",
          "value": "true"
        },
        {
          "name": "OAUTH2_PROXY_COOKIE_SAMESITE",
          "value": "lax"
        },
        {
          "name": "OAUTH2_PROXY_COOKIE_EXPIRE",
          "value": "24h"
        },
        {
          "name": "OAUTH2_PROXY_SKIP_PROVIDER_BUTTON",
          "value": "true"
        }
      ],
      "secrets": [
        {
          "name": "OAUTH2_PROXY_CLIENT_SECRET",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT:secret:oauth2-proxy/azure-client-secret"
        },
        {
          "name": "OAUTH2_PROXY_COOKIE_SECRET",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT:secret:oauth2-proxy/cookie-secret"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/oauth2-proxy",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Step 3: Register Task Definition**

```bash
aws ecs register-task-definition \
  --cli-input-json file://oauth2-proxy-task.json
```

**Step 4: Create ECS Service**

```bash
aws ecs create-service \
  --cluster vaultwarden-cluster \
  --service-name oauth2-proxy \
  --task-definition vaultwarden-oauth2-proxy \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=DISABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=oauth2-proxy,containerPort=4180"
```

✅ **OAuth2 Proxy deployed!**

---

## Part 3: Update Load Balancer (20 minutes)

### GCP: Update Cloud Load Balancing

**Step 1: Create Backend Service**

```bash
# Create backend service for oauth2-proxy
gcloud compute backend-services create oauth2-proxy-backend \
  --protocol=HTTPS \
  --port-name=http \
  --health-checks=default-health-check \
  --global

# Add Cloud Run NEG
gcloud compute network-endpoint-groups create oauth2-proxy-neg \
  --region=$REGION \
  --network-endpoint-type=SERVERLESS \
  --cloud-run-service=$SERVICE_NAME

# Add NEG to backend service
gcloud compute backend-services add-backend oauth2-proxy-backend \
  --global \
  --network-endpoint-group=oauth2-proxy-neg \
  --network-endpoint-group-region=$REGION
```

**Step 2: Update URL Map**

```bash
# Update default service to oauth2-proxy
gcloud compute url-maps edit vaultwarden-url-map
# Change defaultService to oauth2-proxy-backend
```

---

### AWS: Update ALB

**Step 1: Create Target Group**

```bash
aws elbv2 create-target-group \
  --name oauth2-proxy-tg \
  --protocol HTTP \
  --port 4180 \
  --vpc-id vpc-xxx \
  --target-type ip \
  --health-check-path /ping \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3
```

**Step 2: Update ALB Listener**

```bash
# Modify HTTPS listener (port 443) to use new target group
aws elbv2 modify-listener \
  --listener-arn arn:aws:elasticloadbalancing:REGION:ACCOUNT:listener/app/vaultwarden-alb/xxx/xxx \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:REGION:ACCOUNT:targetgroup/oauth2-proxy-tg/xxx
```

✅ **Load balancer updated!**

---

## Part 4: Test SSO Integration (15 minutes)

### Test Flow

**Step 1: Open Incognito/Private Browser**
- Chrome: Ctrl+Shift+N
- Firefox: Ctrl+Shift+P
- Edge: Ctrl+Shift+N

**Step 2: Navigate to Vault**
- Go to: `https://vault.yourcompany.com`

**Expected:** Redirect to Microsoft login

**Step 3: Login with Microsoft**
- Enter: `yourname@yourcompany.com`
- Enter: Your Microsoft password
- Complete MFA (if configured)

**Expected:** Redirect back to Vaultwarden

**Step 4: Enter Master Password**
- Prompt: "Enter your master password"
- Enter: Your Vaultwarden master password

**Expected:** Vault unlocks, passwords visible

**Step 5: Verify Session**
- Close tab
- Open new tab
- Go to: `https://vault.yourcompany.com`

**Expected:** No Microsoft login (session active), master password prompt only

**Step 6: Test Logout**
- Click "Logout" in Vaultwarden
- Go to: `https://vault.yourcompany.com`

**Expected:** Redirect to Microsoft login again

✅ **SSO working correctly!**

---

### Troubleshooting

**Issue: "redirect_uri_mismatch" error**

**Solution:**
1. Check Azure AD app redirect URI exactly matches: `https://vault.yourcompany.com/oauth2/callback`
2. No trailing slash
3. Correct domain

**Issue: "invalid_client" error**

**Solution:**
1. Verify client ID in oauth2-proxy matches Azure AD
2. Verify client secret is correct
3. Check secret hasn't expired

**Issue: "access_denied" error**

**Solution:**
1. Check user's email domain allowed (EMAIL_DOMAINS setting)
2. Verify user has permission in Azure AD
3. Check conditional access policies aren't blocking

**Issue: Redirects to Microsoft but then "404 Not Found"**

**Solution:**
1. Verify load balancer routes to oauth2-proxy
2. Check oauth2-proxy is running: `gcloud run services list` or check ECS service
3. Check oauth2-proxy logs for errors

---

## Part 5: User Provisioning (Optional)

### Manual Provisioning

**For each user:**
1. Go to `https://vault.yourcompany.com/admin`
2. Click "Invite User"
3. Enter user email (must match Azure AD email)
4. User receives invitation email
5. User creates master password
6. User can now login with SSO

---

### Bulk Provisioning Script

**Export users from Azure AD:**

```bash
# Install Azure CLI
# az login

# Export users
az ad user list --query "[].userPrincipalName" -o tsv > users.txt
```

**Invite users to Vaultwarden:**

```bash
#!/bin/bash

ADMIN_TOKEN="your-admin-token"
VAULT_URL="https://vault.yourcompany.com"

while IFS= read -r email; do
  echo "Inviting: $email"
  curl -X POST "${VAULT_URL}/admin/invite" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$email\"}"
  sleep 1
done < users.txt
```

✅ **Users provisioned!**

---

## Part 6: Configure User Groups (Optional)

### Restrict Access to Specific Azure AD Group

**Step 1: Get Group ID**

```bash
# Find your group
az ad group list --query "[?displayName=='Vaultwarden Users'].objectId" -o tsv
```

**Step 2: Update OAuth2 Proxy**

Add environment variable to oauth2-proxy:

```bash
OAUTH2_PROXY_OIDC_GROUPS_CLAIM=groups
OAUTH2_PROXY_ALLOWED_GROUPS=GROUP_OBJECT_ID_HERE
```

**Step 3: Configure Azure AD App**

1. Azure AD → Your app → Token configuration
2. Add groups claim
3. ID and Access tokens: Security groups

**Step 4: Add Users to Group**

1. Azure AD → Groups → "Vaultwarden Users"
2. Members → Add members
3. Select users
4. Add

✅ **Group restriction configured!**

---

## Monitoring & Maintenance

### Monitor OAuth2 Proxy

**GCP Cloud Run:**
```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=vaultwarden-oauth2-proxy" --limit 50

# Monitor metrics
gcloud monitoring dashboards describe oauth2-proxy-dashboard
```

**AWS ECS:**
```bash
# View logs
aws logs tail /ecs/oauth2-proxy --follow

# Check service status
aws ecs describe-services --cluster vaultwarden-cluster --services oauth2-proxy
```

---

### Health Checks

**OAuth2 Proxy Health Endpoint:**
```bash
curl https://vault.yourcompany.com/ping
# Expected: 200 OK
```

**Full Flow Test:**
```bash
# Should redirect to Microsoft login
curl -I https://vault.yourcompany.com
# Expected: 302 redirect to login.microsoftonline.com
```

---

### Rotate Client Secret

**Every 12-24 months:**

1. Azure AD → Your app → Certificates & secrets
2. Create new client secret
3. Update oauth2-proxy configuration (Secret Manager / Secrets Manager)
4. Test SSO login
5. Delete old secret

---

## Cost Summary

**Monthly Costs (1,000 users):**
- Azure AD Free: $0
- OAuth2 Proxy (GCP Cloud Run): $10-20
- OAuth2 Proxy (AWS Fargate): $15-30
- **Total:** $10-30/month

**With Conditional Access (Premium P1):**
- Azure AD Premium P1: $6,000/month (1,000 users)
- OAuth2 Proxy: $10-30/month
- **Total:** $6,010-6,030/month

**Still cheaper than commercial password managers!**

---

## Next Steps

1. ✅ Azure AD configured
2. ✅ OAuth2 Proxy deployed
3. ✅ Load balancer updated
4. ✅ SSO tested
5. [ ] Provision users
6. [ ] Document for end users
7. [ ] Announce to organization
8. [ ] Monitor adoption

---

## Support

**Azure AD Issues:**
- Azure Support Portal
- Azure AD documentation

**OAuth2 Proxy Issues:**
- GitHub: [oauth2-proxy/oauth2-proxy](https://github.com/oauth2-proxy/oauth2-proxy)
- Logs: Check Cloud Run or ECS logs

**Vaultwarden Issues:**
- Your deployment documentation
- Email: adrian207@gmail.com

---

**Setup Complete!** Your users can now login with Microsoft Azure AD SSO. 🎉

