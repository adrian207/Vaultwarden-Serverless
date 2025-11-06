# SSO Integration Implementation Plan

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Date:** November 5, 2025  
**Status:** Planning Phase

## Executive Summary

**Current State:** Vaultwarden uses email/password authentication with optional 2FA.

**Goal:** Enable Single Sign-On (SSO) for enterprise users using existing identity providers (Azure AD, Google Workspace, Okta, etc.).

**Challenge:** Vaultwarden does not natively support SAML/OAuth SSO for vault unlock due to zero-knowledge encryption architecture.

**Solution Approach:** Implement SSO for **login/authentication** while maintaining zero-knowledge encryption for **vault unlock**.

---

## Understanding the Challenge

### Zero-Knowledge Encryption Architecture

**How Vaultwarden Works:**
1. User enters master password
2. Master password derives encryption key (client-side)
3. Encryption key decrypts vault (client-side)
4. Server never sees encryption key
5. Server never sees unencrypted vault data

**Why This Matters:**
- Master password ≠ login password (in SSO context)
- SSO can authenticate user identity
- SSO cannot decrypt vault (no access to encryption key)
- Must maintain both: SSO login + master password/key

---

## SSO Implementation Options

### Option 1: Hybrid SSO + Master Password ⭐ **RECOMMENDED**

**How It Works:**
1. User logs in via SSO (Azure AD, Google, etc.)
2. SSO validates user identity
3. User then enters master password
4. Master password unlocks vault

**Pros:**
- ✅ Best security (zero-knowledge maintained)
- ✅ Centralized user management
- ✅ SSO benefits (audit, MFA, conditional access)
- ✅ No vault access if SSO account compromised alone

**Cons:**
- ❌ Two-step login (SSO + master password)
- ❌ Requires custom implementation or proxy

**Best For:** Enterprises with 100+ users, high security requirements

**Implementation:** Requires authentication proxy or custom integration

---

### Option 2: Directory Sync (LDAP/SCIM)

**How It Works:**
1. Sync users from directory (AD, LDAP, etc.)
2. Auto-create Vaultwarden accounts
3. Users login with email/password
4. Optionally: Use same password as directory

**Pros:**
- ✅ Centralized user provisioning
- ✅ Automatic account creation
- ✅ Deprovisioning support
- ✅ Works with Vaultwarden natively (LDAP support available)

**Cons:**
- ❌ Not true SSO (separate passwords)
- ❌ Users must remember separate password (unless synced)

**Best For:** Organizations wanting centralized user management without full SSO

**Implementation:** Configure LDAP/directory sync in Vaultwarden

---

### Option 3: Authentication Proxy (OAuth/OIDC)

**How It Works:**
1. Deploy authentication proxy (oauth2-proxy, Authelia, etc.)
2. Proxy sits in front of Vaultwarden
3. User authenticates via OAuth/OIDC
4. Proxy forwards authenticated requests to Vaultwarden
5. User still enters master password for vault

**Pros:**
- ✅ True SSO experience
- ✅ Works with any OAuth/OIDC provider
- ✅ No Vaultwarden modifications needed
- ✅ Maintains zero-knowledge encryption

**Cons:**
- ❌ Additional infrastructure component
- ❌ Complexity in setup
- ❌ Still requires master password for vault

**Best For:** Enterprises with existing OAuth/OIDC infrastructure

**Implementation:** Deploy proxy with serverless (Cloud Run, Fargate, etc.)

---

### Option 4: Bitwarden Official (Commercial Alternative)

**How It Works:**
1. Upgrade to commercial Bitwarden
2. Enable enterprise SSO feature
3. Users login via SAML/SSO
4. Master password optional or org-managed

**Pros:**
- ✅ Native SAML/SSO support
- ✅ Fully supported solution
- ✅ Advanced admin features
- ✅ Customer support

**Cons:**
- ❌ Costs $6-10/user/month
- ❌ Must migrate from Vaultwarden
- ❌ Loses cost savings

**Best For:** Organizations requiring official support and willing to pay

**Cost:** $72,000-$120,000/year for 1,000 users

---

## Recommended Architecture

### Hybrid SSO with Authentication Proxy ⭐

```
User
  ↓ (1) Navigate to vault.company.com
OAuth2 Proxy (Cloud Run / Fargate)
  ↓ (2) Redirect to IdP (Azure AD, Google, Okta)
Identity Provider
  ↓ (3) User authenticates with SSO
OAuth2 Proxy
  ↓ (4) Verify token, forward to Vaultwarden
Vaultwarden
  ↓ (5) User enters master password
Vault Unlocked ✅
```

**Components:**
1. **Identity Provider** - Azure AD, Google Workspace, Okta, Keycloak
2. **OAuth2 Proxy** - Serverless container (Cloud Run, Fargate)
3. **Vaultwarden** - Existing deployment (unchanged)
4. **Load Balancer** - Routes through proxy

**User Experience:**
1. User goes to vault URL
2. Redirected to company SSO
3. Logs in with SSO (Microsoft, Google, etc.)
4. Redirected back to Vaultwarden
5. Enters master password
6. Vault unlocked

**Security:**
- ✅ Centralized authentication
- ✅ Zero-knowledge encryption maintained
- ✅ MFA enforced at IdP
- ✅ Conditional access policies apply
- ✅ Audit logs in IdP

---

## Identity Provider Options

### Azure Active Directory (Azure AD / Entra ID)

**Best For:** Microsoft 365 organizations, Azure cloud users

**Features:**
- ✅ SAML 2.0 and OAuth 2.0/OIDC support
- ✅ Conditional access policies
- ✅ Multi-factor authentication
- ✅ Rich audit logs
- ✅ Device compliance checks
- ✅ Integration with Microsoft ecosystem

**Pricing:**
- Azure AD Free: Basic SSO
- Azure AD Premium P1: $6/user/month (conditional access)
- Azure AD Premium P2: $9/user/month (advanced features)

**Setup Complexity:** Medium  
**Documentation:** Excellent

---

### Google Workspace

**Best For:** Google Workspace organizations, GCP users

**Features:**
- ✅ OAuth 2.0/OIDC support
- ✅ 2-Step Verification
- ✅ Security keys support
- ✅ Admin audit logs
- ✅ Context-aware access
- ✅ Integration with Google ecosystem

**Pricing:**
- Business Starter: $6/user/month
- Business Standard: $12/user/month
- Business Plus: $18/user/month

**Setup Complexity:** Easy  
**Documentation:** Excellent

---

### Okta

**Best For:** Enterprises with diverse app ecosystem

**Features:**
- ✅ SAML 2.0 and OIDC support
- ✅ Universal Directory
- ✅ Lifecycle Management
- ✅ Adaptive MFA
- ✅ API Access Management
- ✅ Extensive integrations (7,000+ apps)

**Pricing:**
- Workforce Identity: $2-5/user/month
- Customer Identity: Usage-based

**Setup Complexity:** Medium  
**Documentation:** Excellent

---

### Keycloak (Open Source)

**Best For:** Self-hosted, cost-conscious organizations

**Features:**
- ✅ Free and open source
- ✅ SAML 2.0 and OIDC support
- ✅ User federation (LDAP, AD)
- ✅ Social login (Google, Facebook, etc.)
- ✅ Custom themes and branding
- ✅ Self-hosted or managed

**Pricing:**
- Self-hosted: $0 (infrastructure costs only)
- Managed (Red Hat SSO): Enterprise pricing

**Setup Complexity:** High  
**Documentation:** Good

---

### Auth0 (by Okta)

**Best For:** Developers, modern applications

**Features:**
- ✅ OAuth 2.0/OIDC support
- ✅ Social and enterprise connections
- ✅ Passwordless authentication
- ✅ Extensive SDKs
- ✅ Rules and Actions (customization)
- ✅ Developer-friendly

**Pricing:**
- Free: 7,500 active users
- Essentials: $35/month (500 users)
- Professional: $240/month (1,000 users)
- Enterprise: Custom pricing

**Setup Complexity:** Easy  
**Documentation:** Excellent

---

## Implementation: OAuth2 Proxy + Azure AD

### Architecture

```
Internet
  ↓
CloudFront / Cloud CDN
  ↓
Application Load Balancer / Cloud Load Balancing
  ↓
┌─────────────────────────────────┐
│     OAuth2 Proxy Container      │  ← New Component
│  (Cloud Run / ECS Fargate)      │
│                                 │
│  - Validate Azure AD tokens     │
│  - Session management           │
│  - Forward authenticated users  │
└─────────────────────────────────┘
  ↓
┌─────────────────────────────────┐
│        Vaultwarden              │  ← Existing
│     (Cloud Run / ECS)           │
└─────────────────────────────────┘
  ↓
Aurora Serverless / Cloud SQL
```

---

### Components

**1. OAuth2 Proxy**
- **Purpose:** SSO gateway
- **Technology:** oauth2-proxy (open source)
- **Deployment:** Serverless container
- **Configuration:** Azure AD client ID/secret
- **Resources:** 
  - CPU: 0.5-1 vCPU
  - Memory: 512MB-1GB
  - Auto-scaling: 1-10 instances

**2. Azure AD Application**
- **Type:** Enterprise application
- **Protocol:** OAuth 2.0 / OIDC
- **Redirect URI:** `https://vault.company.com/oauth2/callback`
- **Permissions:** User.Read (basic profile)

**3. Session Store**
- **Purpose:** Store OAuth sessions
- **Options:**
  - Redis (serverless, Elasticache/Memorystore)
  - Encrypted cookies (simpler)
- **TTL:** 24 hours (configurable)

---

### Step-by-Step Setup

#### Phase 1: Azure AD Configuration (30 minutes)

**Step 1: Register Application**
1. Go to Azure Portal → Azure Active Directory
2. App registrations → New registration
3. Name: "Vaultwarden SSO"
4. Redirect URI: `https://vault.company.com/oauth2/callback`
5. Register

**Step 2: Configure Application**
1. Note Application (client) ID
2. Note Directory (tenant) ID
3. Certificates & secrets → New client secret
4. Note secret value (save securely)
5. API permissions → Add Microsoft Graph → User.Read
6. Grant admin consent

**Step 3: Configure Conditional Access (Optional)**
1. Azure AD → Security → Conditional Access
2. New policy:
   - Users: All users or specific group
   - Cloud apps: Vaultwarden SSO app
   - Conditions: MFA required, device compliance, etc.
   - Grant: Require MFA, compliant device, etc.

---

#### Phase 2: Deploy OAuth2 Proxy (60 minutes)

**Option A: GCP Cloud Run**

**Dockerfile:**
```dockerfile
FROM quay.io/oauth2-proxy/oauth2-proxy:v7.5.1

# Use unprivileged user
USER 2000:2000
```

**Deploy:**
```bash
# Set variables
PROJECT_ID="your-gcp-project"
REGION="us-central1"
SERVICE_NAME="vaultwarden-oauth2-proxy"

# Azure AD config
AZURE_TENANT="your-tenant-id"
AZURE_CLIENT_ID="your-client-id"
AZURE_CLIENT_SECRET="your-client-secret"

# Vaultwarden backend
VAULTWARDEN_URL="https://vaultwarden-internal.run.app"

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image quay.io/oauth2-proxy/oauth2-proxy:v7.5.1 \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="OAUTH2_PROXY_PROVIDER=oidc" \
  --set-env-vars="OAUTH2_PROXY_OIDC_ISSUER_URL=https://login.microsoftonline.com/${AZURE_TENANT}/v2.0" \
  --set-env-vars="OAUTH2_PROXY_CLIENT_ID=${AZURE_CLIENT_ID}" \
  --set-env-vars="OAUTH2_PROXY_CLIENT_SECRET=${AZURE_CLIENT_SECRET}" \
  --set-env-vars="OAUTH2_PROXY_REDIRECT_URL=https://vault.company.com/oauth2/callback" \
  --set-env-vars="OAUTH2_PROXY_UPSTREAMS=${VAULTWARDEN_URL}" \
  --set-env-vars="OAUTH2_PROXY_EMAIL_DOMAINS=*" \
  --set-env-vars="OAUTH2_PROXY_COOKIE_SECRET=$(openssl rand -base64 32)" \
  --set-env-vars="OAUTH2_PROXY_COOKIE_SECURE=true" \
  --set-env-vars="OAUTH2_PROXY_SKIP_PROVIDER_BUTTON=true" \
  --cpu=1 \
  --memory=512Mi \
  --min-instances=1 \
  --max-instances=10
```

**Option B: AWS ECS Fargate**

**Task Definition:**
```json
{
  "family": "vaultwarden-oauth2-proxy",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "oauth2-proxy",
      "image": "quay.io/oauth2-proxy/oauth2-proxy:v7.5.1",
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
          "value": "https://vault.company.com/oauth2/callback"
        },
        {
          "name": "OAUTH2_PROXY_UPSTREAMS",
          "value": "http://vaultwarden.internal:8080"
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
          "name": "OAUTH2_PROXY_SKIP_PROVIDER_BUTTON",
          "value": "true"
        }
      ],
      "secrets": [
        {
          "name": "OAUTH2_PROXY_CLIENT_SECRET",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:oauth2-proxy-secret"
        },
        {
          "name": "OAUTH2_PROXY_COOKIE_SECRET",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:oauth2-proxy-cookie"
        }
      ]
    }
  ]
}
```

---

#### Phase 3: Update Load Balancer (30 minutes)

**GCP: Update Cloud Load Balancing**
```bash
# Backend service for oauth2-proxy
gcloud compute backend-services create oauth2-proxy-backend \
  --protocol=HTTPS \
  --global \
  --health-checks=oauth2-proxy-health

# Add Cloud Run backend
gcloud compute backend-services add-backend oauth2-proxy-backend \
  --global \
  --serverless-region=$REGION \
  --serverless-deployment=oauth2-proxy

# Update URL map to route through proxy
gcloud compute url-maps edit vaultwarden-url-map
```

**AWS: Update ALB Target Group**
```bash
# Create target group for oauth2-proxy
aws elbv2 create-target-group \
  --name vaultwarden-oauth2-proxy \
  --protocol HTTPS \
  --port 4180 \
  --vpc-id vpc-xxx \
  --target-type ip \
  --health-check-path /ping

# Update listener rule
aws elbv2 modify-listener \
  --listener-arn arn:aws:elasticloadbalancing:... \
  --default-actions Type=forward,TargetGroupArn=arn:aws:...
```

---

#### Phase 4: Test SSO (15 minutes)

**Test Flow:**
1. Open incognito browser
2. Navigate to `https://vault.company.com`
3. Redirected to Microsoft login
4. Enter Microsoft credentials
5. Complete MFA (if configured)
6. Redirected back to Vaultwarden
7. Enter master password
8. Vault unlocks

**Verify:**
- ✅ SSO login works
- ✅ Master password still required
- ✅ Vault decrypts successfully
- ✅ Session persists (24 hours default)
- ✅ Logout clears session

---

## Configuration Options

### Session Duration

**oauth2-proxy config:**
```bash
OAUTH2_PROXY_COOKIE_EXPIRE=24h  # SSO session duration
OAUTH2_PROXY_COOKIE_REFRESH=1h   # Token refresh interval
```

**Recommended:** 24 hours (users login once per day)

---

### User Restrictions

**Option 1: Email Domain**
```bash
OAUTH2_PROXY_EMAIL_DOMAINS=company.com,company.co.uk
```

**Option 2: Specific Users**
```bash
OAUTH2_PROXY_AUTHENTICATED_EMAILS_FILE=/config/emails.txt
```

**Option 3: Azure AD Group**
```bash
OAUTH2_PROXY_OIDC_GROUPS_CLAIM=groups
OAUTH2_PROXY_ALLOWED_GROUPS=vaultwarden-users
```

---

### Conditional Access

**Azure AD Policies:**
- Require MFA for all users
- Require compliant device
- Require managed device
- Block legacy authentication
- Require approved client app
- Geographic restrictions
- Risk-based policies

**Configured in Azure AD, enforced automatically**

---

## Security Considerations

### Defense in Depth

**Layer 1: Identity Provider**
- SSO authentication
- MFA enforcement
- Conditional access policies
- Device compliance checks

**Layer 2: OAuth2 Proxy**
- Token validation
- Session management
- HTTPS enforcement
- CORS protection

**Layer 3: Vaultwarden**
- Master password (zero-knowledge)
- Vault encryption
- 2FA (optional, additional)
- Rate limiting

**Layer 4: Infrastructure**
- WAF rules
- DDoS protection
- Network isolation
- Encrypted transit/rest

---

### Session Security

**Cookie Settings:**
```bash
OAUTH2_PROXY_COOKIE_SECURE=true      # HTTPS only
OAUTH2_PROXY_COOKIE_HTTPONLY=true    # No JavaScript access
OAUTH2_PROXY_COOKIE_SAMESITE=lax     # CSRF protection
```

**Session Storage:**
- Option 1: Encrypted cookies (simple)
- Option 2: Redis (scalable, can revoke)

---

### Account Provisioning

**Challenge:** User must exist in Vaultwarden before SSO login

**Solutions:**

**Option 1: Pre-provision via API**
```bash
# Script to create users from directory
for user in $(get_users_from_ad); do
  curl -X POST https://vault.company.com/admin/invite \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d "email=$user"
done
```

**Option 2: Just-in-Time Provisioning**
- Modify oauth2-proxy to auto-create users
- Requires custom logic or script

**Option 3: Self-service Registration**
- Users register once manually
- SSO takes over after registration

**Recommended:** Option 1 (automated provisioning)

---

## Cost Analysis

### Infrastructure Costs (SSO Components)

**GCP (1,000 users):**
- OAuth2 Proxy (Cloud Run): $10-20/month
- Session storage (Redis, if used): $30-50/month
- Load Balancing (existing): $0 additional
- **Total:** $40-70/month

**AWS (1,000 users):**
- OAuth2 Proxy (Fargate): $15-30/month
- Session storage (Elasticache, if used): $40-60/month
- ALB (existing): $0 additional
- **Total:** $55-90/month

---

### Identity Provider Costs

**Azure AD:**
- Free tier: $0 (basic SSO)
- Premium P1: $6/user/month ($6,000/month for 1,000 users)
- Premium P2: $9/user/month ($9,000/month for 1,000 users)

**Google Workspace:**
- Included with Workspace subscriptions
- Business Starter: $6/user/month
- Business Standard: $12/user/month

**Okta:**
- Workforce Identity: $2-5/user/month ($2,000-5,000/month for 1,000 users)

**Keycloak:**
- Self-hosted: $50-100/month (infrastructure)
- Managed (Red Hat SSO): Enterprise pricing

**Auth0:**
- Free: 7,500 users ($0)
- Essentials: $35/month base + per-user
- Professional: $240/month + per-user

---

### Total Cost Comparison (1,000 users)

**Option 1: OAuth2 Proxy + Azure AD Free**
- Infrastructure: $40-90/month
- Identity Provider: $0
- **Total:** $40-90/month ($480-1,080/year)

**Option 2: OAuth2 Proxy + Azure AD Premium P1**
- Infrastructure: $40-90/month
- Identity Provider: $6,000/month
- **Total:** $6,040-6,090/month ($72,480-73,080/year)

**Option 3: OAuth2 Proxy + Okta**
- Infrastructure: $40-90/month
- Identity Provider: $2,000-5,000/month
- **Total:** $2,040-5,090/month ($24,480-61,080/year)

**Option 4: OAuth2 Proxy + Keycloak (self-hosted)**
- Infrastructure: $40-90/month (proxy)
- Infrastructure: $50-100/month (Keycloak)
- Identity Provider: $0
- **Total:** $90-190/month ($1,080-2,280/year)

**Option 5: Bitwarden Official SSO**
- Infrastructure: Bitwarden-managed
- Bitwarden license: $6-10/user/month ($6,000-10,000/month)
- **Total:** $6,000-10,000/month ($72,000-120,000/year)

**Recommended for Cost:** If you already have Azure AD/Google Workspace, use that. Otherwise, self-hosted Keycloak.

---

## Implementation Timeline

### Phase 1: Planning & Design (Week 1)

**Action Items:**
- [ ] Choose identity provider (Azure AD, Google, Okta, Keycloak)
- [ ] Review security requirements
- [ ] Architect SSO flow
- [ ] Document user experience
- [ ] Get stakeholder approval

**Deliverable:** SSO design document

---

### Phase 2: Identity Provider Setup (Week 2)

**Action Items:**
- [ ] Register OAuth application in IdP
- [ ] Configure redirect URIs
- [ ] Set up conditional access policies (if applicable)
- [ ] Configure user groups/permissions
- [ ] Test IdP configuration

**Deliverable:** Configured identity provider

---

### Phase 3: OAuth2 Proxy Deployment (Week 3)

**Action Items:**
- [ ] Create Dockerfile/container image
- [ ] Configure oauth2-proxy settings
- [ ] Store secrets securely (Secrets Manager)
- [ ] Deploy to serverless (Cloud Run / Fargate)
- [ ] Configure health checks
- [ ] Set up auto-scaling

**Deliverable:** Deployed oauth2-proxy

---

### Phase 4: Integration & Testing (Week 4)

**Action Items:**
- [ ] Update load balancer routing
- [ ] Configure DNS (if needed)
- [ ] Test SSO login flow
- [ ] Test master password unlock
- [ ] Test all client apps (web, browser, mobile)
- [ ] Test session timeout
- [ ] Test logout

**Deliverable:** Working SSO integration

---

### Phase 5: User Provisioning (Week 5)

**Action Items:**
- [ ] Export users from identity provider
- [ ] Create provisioning script
- [ ] Pre-provision user accounts in Vaultwarden
- [ ] Send invitations to users
- [ ] Document user onboarding

**Deliverable:** Provisioned user accounts

---

### Phase 6: Documentation & Training (Week 6)

**Action Items:**
- [ ] Create user guides
- [ ] Document SSO login process
- [ ] Create troubleshooting guide
- [ ] Train support team
- [ ] Prepare announcement

**Deliverable:** Complete documentation

---

### Phase 7: Pilot Rollout (Week 7)

**Action Items:**
- [ ] Select pilot group (10-20 users)
- [ ] Distribute documentation
- [ ] Monitor pilot users
- [ ] Gather feedback
- [ ] Refine documentation

**Deliverable:** Validated SSO implementation

---

### Phase 8: Full Rollout (Week 8)

**Action Items:**
- [ ] Announce to all users
- [ ] Monitor adoption
- [ ] Address support tickets
- [ ] Measure success metrics
- [ ] Optimize performance

**Deliverable:** SSO in production

---

## User Experience

### First Login (with SSO)

**Step 1: Navigate to Vault**
- User goes to `https://vault.company.com`

**Step 2: SSO Redirect**
- Automatically redirected to company SSO
- (Microsoft login / Google login / Okta)

**Step 3: Authenticate**
- Enter company email/password
- Complete MFA (if required)
- Device compliance check (if configured)

**Step 4: Redirect to Vaultwarden**
- Redirected back to vault
- SSO session established (24 hours)

**Step 5: Enter Master Password**
- Prompt: "Enter your master password"
- User enters master password
- Vault unlocks

**Step 6: Access Granted**
- Full access to password vault
- All features available

**Total Time:** 30-60 seconds (first login)

---

### Subsequent Logins (same day)

**Step 1: Navigate to Vault**
- User goes to `https://vault.company.com`

**Step 2: SSO Session Valid**
- No redirect (session still active)
- Directly to Vaultwarden

**Step 3: Enter Master Password**
- User enters master password
- Vault unlocks

**Total Time:** 10 seconds

---

### Logout

**User clicks "Logout":**
1. Vaultwarden locks vault
2. OAuth2 proxy clears session
3. (Optional) IdP logout redirect

**Effect:**
- Vault locked
- SSO session cleared
- Must re-authenticate on next login

---

## Monitoring & Logging

### Metrics to Track

**Authentication:**
- SSO login attempts (success/failure)
- SSO session duration
- Master password unlock attempts
- Failed authentication rates

**Performance:**
- OAuth2 proxy latency
- Token validation time
- Session lookup time
- End-to-end login time

**Security:**
- Failed login attempts by user
- Failed login attempts by IP
- Suspicious geographic logins
- Conditional access blocks

---

### Logging Strategy

**OAuth2 Proxy Logs:**
```json
{
  "timestamp": "2025-11-05T10:30:45Z",
  "level": "info",
  "event": "authentication_success",
  "user": "user@company.com",
  "ip": "203.0.113.1",
  "user_agent": "Mozilla/5.0...",
  "session_id": "abc123..."
}
```

**Azure AD Audit Logs:**
- Sign-in logs
- Conditional access decisions
- MFA events
- Risk detections

**Vaultwarden Logs:**
- Master password attempts
- Vault access
- Item modifications
- API calls

---

### Alerting

**Critical Alerts:**
- SSO service down (5xx errors)
- Token validation failures (> 5% rate)
- Unusual login patterns

**Warning Alerts:**
- Session store latency (> 500ms)
- OAuth2 proxy high memory
- Failed login rate increase (> 10%)

**Send to:**
- PagerDuty / Opsgenie
- Slack / Teams
- Email (security team)

---

## Troubleshooting

### Issue: "OAuth callback error"

**Causes:**
1. Incorrect redirect URI in IdP
2. Client secret mismatch
3. Token validation failure

**Solutions:**
1. Verify redirect URI: `https://vault.company.com/oauth2/callback`
2. Check client secret in oauth2-proxy config
3. Review oauth2-proxy logs for specific error
4. Verify IdP application permissions

---

### Issue: "Access denied after SSO login"

**Causes:**
1. User not provisioned in Vaultwarden
2. Email domain not allowed
3. User not in allowed Azure AD group

**Solutions:**
1. Pre-provision user account
2. Check `OAUTH2_PROXY_EMAIL_DOMAINS` setting
3. Verify Azure AD group membership

---

### Issue: "Session expired too quickly"

**Causes:**
1. Cookie expiration too short
2. Token refresh not configured
3. Session store issues

**Solutions:**
1. Increase `OAUTH2_PROXY_COOKIE_EXPIRE` (default: 24h)
2. Enable `OAUTH2_PROXY_COOKIE_REFRESH`
3. Check Redis/session store connectivity

---

### Issue: "Master password not prompted"

**This should not happen!**

**Verification:**
1. Navigate to vault after SSO
2. Should always prompt for master password
3. If not, vault cannot decrypt (security issue)

**If master password skipped:**
- Zero-knowledge encryption is bypassed (BAD!)
- Review oauth2-proxy config
- Ensure not bypassing Vaultwarden auth

---

## Limitations & Trade-offs

### Known Limitations

**1. Two-Step Login**
- Users must: SSO + master password
- Cannot be single step (zero-knowledge requirement)
- Trade-off: Security vs convenience

**2. Client App Compatibility**
- Browser extensions: SSO works
- Mobile apps: Must use email/password (no SSO)
- Desktop apps: Must use email/password (no SSO)
- CLI: Must use API token

**Why:** Client apps connect directly to Vaultwarden API, bypass proxy

**Workaround:** Users can use same email/password as SSO (if directory-synced)

**3. Account Provisioning**
- Users must be pre-provisioned
- No automatic just-in-time provisioning (requires custom dev)

**4. Session Management**
- SSO session separate from vault lock
- SSO session ≠ vault unlock
- Users can be SSO-authenticated but vault locked

---

### Trade-offs

**Security vs Convenience:**
- More secure: SSO + master password
- Less convenient: Two authentication steps

**Simplicity vs Features:**
- Simpler: No SSO, just email/password
- More features: SSO with centralized management

**Cost vs Control:**
- Cheaper: Self-hosted Keycloak
- Easier: Managed Azure AD / Okta

---

## Alternative: Directory Sync (LDAP)

### Vaultwarden LDAP Support

**Built-in feature!** Vaultwarden supports LDAP authentication.

**How It Works:**
1. User enters email and password
2. Vaultwarden validates against LDAP/AD
3. Password also derives vault encryption key
4. Vault unlocks

**Pros:**
- ✅ Centralized authentication
- ✅ Single password for user
- ✅ Simpler than OAuth proxy
- ✅ Works with all client apps

**Cons:**
- ❌ Not true SSO (still enter password)
- ❌ LDAP must be accessible from Vaultwarden
- ❌ No conditional access policies

**Configuration:**
```bash
# Vaultwarden environment variables
LDAP_ENABLED=true
LDAP_URL=ldaps://ldap.company.com:636
LDAP_BIND_DN=cn=admin,dc=company,dc=com
LDAP_BIND_PASSWORD=secure_password
LDAP_USER_BASE_DN=ou=users,dc=company,dc=com
LDAP_USER_SEARCH_FILTER=(&(objectClass=person)(mail=%s))
LDAP_USER_EMAIL_ATTRIBUTE=mail
```

**Use Case:** Organizations wanting centralized auth without full SSO complexity

---

## Recommendations

### For Small Teams (1-100 users)

**Recommendation:** Skip SSO, use email/password + 2FA

**Reasoning:**
- SSO setup overhead not justified
- Email/password simpler
- 2FA provides good security
- Cost: $0

---

### For Medium Organizations (100-1,000 users)

**Recommendation:** LDAP sync (if existing directory) OR OAuth2 proxy + Azure AD Free

**Reasoning:**
- Centralized user management beneficial
- LDAP simpler if already using AD
- OAuth2 proxy provides SSO experience
- Cost: $0-50/month

---

### For Large Enterprises (1,000-10,000+ users)

**Recommendation:** OAuth2 proxy + Azure AD Premium / Okta

**Reasoning:**
- SSO expected in enterprise
- Conditional access policies critical
- Compliance requirements
- Centralized audit logs
- Worth the cost ($2k-9k/month)

---

### For Maximum Security

**Recommendation:** OAuth2 proxy + Azure AD Premium P2 + Conditional Access

**Features:**
- Risk-based access
- Device compliance
- Geographic restrictions
- MFA enforcement
- Advanced threat protection

**Cost:** $9/user/month for Azure AD P2

---

## Next Steps

### Immediate (This Week)

1. **Decide:** Do you need SSO?
2. **Choose:** Which identity provider?
3. **Budget:** Approve costs (IdP + infrastructure)
4. **Review:** This implementation plan
5. **Approve:** Move forward or defer

---

### If Proceeding (Weeks 2-8)

6. **Week 2:** Set up identity provider
7. **Week 3:** Deploy oauth2-proxy
8. **Week 4:** Integration testing
9. **Week 5:** User provisioning
10. **Week 6:** Documentation
11. **Week 7:** Pilot rollout
12. **Week 8:** Full deployment

---

## Conclusion

**SSO with Vaultwarden is possible but requires careful architecture due to zero-knowledge encryption.**

**Key Points:**
- ✅ SSO handles **authentication** (who you are)
- ✅ Master password handles **vault unlock** (decrypt data)
- ✅ Cannot skip master password (security requirement)
- ✅ OAuth2 proxy recommended approach
- ✅ LDAP sync simpler alternative
- ✅ Cost: $40-90/month (infrastructure) + IdP costs

**Recommendation:** Evaluate based on organization size and existing infrastructure. For most deployments under 1,000 users, LDAP sync or email/password + 2FA is sufficient. For enterprises 1,000+ users, invest in OAuth2 proxy + managed IdP.

---

**Document Version:** 1.0  
**Last Updated:** November 5, 2025  
**Next Review:** February 2026

**Questions?** adrian207@gmail.com

