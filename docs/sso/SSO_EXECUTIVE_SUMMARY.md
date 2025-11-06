# SSO Integration - Executive Summary

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Date:** November 5, 2025  
**Status:** Planning & Documentation Complete

## TL;DR (30 seconds)

**Can Vaultwarden do SSO?** Yes, but with an important caveat due to zero-knowledge encryption.

**Solution:** SSO handles login authentication → User still enters master password to unlock vault

**Recommended Approach:** OAuth2 Proxy + Your existing identity provider (Azure AD, Google Workspace, Okta)

**Cost:** $40-90/month (infrastructure) + Identity provider costs (possibly $0 if you already have one)

**Implementation Time:** 6-8 weeks

**Complexity:** Medium-High

---

## Key Decision: Do You Need SSO?

### ✅ You SHOULD implement SSO if:

- You have 100+ users
- You already use Azure AD, Google Workspace, or Okta
- Centralized user management is critical
- Compliance requires MFA and audit logs
- You want conditional access policies
- Budget allows ($40-6,000+/month depending on IdP)

### ❌ You DON'T need SSO if:

- You have < 100 users
- Email/password + 2FA provides sufficient security
- Budget is extremely tight ($0)
- Team comfortable with separate credentials
- Implementation complexity not justified

**Alternative for < 100 users:** Use email/password authentication with strong 2FA. It's simpler, costs $0, and provides good security.

---

## Understanding the Architecture

### The Zero-Knowledge Challenge

**Vaultwarden uses zero-knowledge encryption:**
1. Master password derives encryption key (client-side)
2. Encryption key decrypts vault (client-side)
3. Server never has encryption key
4. Server never has unencrypted data

**This means:**
- SSO can authenticate WHO you are (identity)
- SSO cannot decrypt vault (no encryption key)
- Master password ALWAYS required for vault unlock
- Two-step process: SSO login + Master password

**Trade-off:** More steps, but maximum security

---

## Recommended Solution

### Hybrid SSO with OAuth2 Proxy ⭐

**Architecture:**
```
User → Identity Provider (Azure AD/Google/Okta)
     → OAuth2 Proxy (authenticates)
     → Vaultwarden (master password prompt)
     → Vault Unlocked
```

**User Experience:**
1. Navigate to vault.company.com
2. Redirect to company SSO (Microsoft/Google)
3. Login with SSO credentials + MFA
4. Redirect back to vault
5. Enter master password
6. Vault unlocked

**First login:** ~60 seconds  
**Subsequent logins (same day):** ~10 seconds (SSO session cached)

---

## Implementation Options

### Option 1: OAuth2 Proxy (Recommended)

**Best For:** Enterprises, 100-10,000+ users

**Pros:**
- ✅ True SSO experience
- ✅ Works with any OAuth/OIDC provider
- ✅ Maintains zero-knowledge encryption
- ✅ Centralized authentication
- ✅ MFA enforcement at IdP
- ✅ Audit logs at IdP
- ✅ Conditional access policies

**Cons:**
- ❌ Additional infrastructure component
- ❌ Medium-high setup complexity
- ❌ Still requires master password

**Cost:** $40-90/month (infrastructure) + IdP costs  
**Time:** 6-8 weeks implementation

---

### Option 2: LDAP Directory Sync

**Best For:** Organizations with existing AD/LDAP, want simplicity

**Pros:**
- ✅ Centralized user management
- ✅ Automatic account provisioning
- ✅ Works with all client apps
- ✅ Simpler than OAuth proxy
- ✅ Built into Vaultwarden

**Cons:**
- ❌ Not true SSO (users still enter password)
- ❌ LDAP server must be accessible
- ❌ No conditional access policies

**Cost:** $0 (uses existing LDAP)  
**Time:** 2-3 weeks implementation

---

### Option 3: Email/Password + 2FA (Baseline)

**Best For:** Small teams (< 100 users), budget-conscious

**Pros:**
- ✅ Simplest approach
- ✅ $0 cost
- ✅ Works with all clients
- ✅ No additional infrastructure
- ✅ Strong security with 2FA

**Cons:**
- ❌ Separate credentials to remember
- ❌ Manual user management
- ❌ No centralized audit logs

**Cost:** $0  
**Time:** 0 (already implemented)

---

## Identity Provider Options

### Azure Active Directory / Microsoft Entra ID

**Best For:** Microsoft 365 organizations

**Pricing:**
- Free: Basic SSO ($0)
- Premium P1: Conditional access ($6/user/month)
- Premium P2: Advanced features ($9/user/month)

**Features:** SAML, OIDC, conditional access, MFA, rich audit logs

**Setup Guide:** [SSO Setup - Azure AD](SSO_SETUP_AZURE_AD.md)

---

### Google Workspace

**Best For:** Google-centric organizations

**Pricing:**
- Included with Workspace ($6-18/user/month)

**Features:** OAuth 2.0, OIDC, 2-Step Verification, context-aware access

**Setup Guide:** Coming soon

---

### Okta

**Best For:** Enterprises with diverse app ecosystem

**Pricing:**
- Workforce Identity: $2-5/user/month

**Features:** SAML, OIDC, Universal Directory, adaptive MFA, 7,000+ integrations

**Setup Guide:** Coming soon

---

### Keycloak (Open Source)

**Best For:** Self-hosted, cost-conscious

**Pricing:**
- Self-hosted: $0 (infrastructure only: $50-100/month)

**Features:** SAML, OIDC, user federation, social login, custom branding

**Setup Guide:** Coming soon

---

## Cost Analysis

### Small Organization (100 users)

**Option 1: OAuth2 Proxy + Azure AD Free**
- Infrastructure: $40-90/month
- IdP: $0
- **Total:** $40-90/month ($480-1,080/year)

**Option 2: LDAP Sync (existing AD)**
- Infrastructure: $0 additional
- **Total:** $0/year

**Option 3: Email/Password + 2FA**
- **Total:** $0/year

**Recommendation:** LDAP sync or email/password

---

### Medium Organization (1,000 users)

**Option 1: OAuth2 Proxy + Azure AD Premium P1**
- Infrastructure: $40-90/month
- IdP: $6,000/month
- **Total:** $6,040-6,090/month ($72,480-73,080/year)

**Option 2: OAuth2 Proxy + Keycloak**
- Infrastructure: $40-90/month (proxy)
- Infrastructure: $50-100/month (Keycloak)
- **Total:** $90-190/month ($1,080-2,280/year)

**Option 3: LDAP Sync**
- **Total:** $0/year

**Recommendation:** Depends on existing infrastructure  
- Have Azure AD Premium? Use it
- Need conditional access but no IdP? Invest in managed IdP
- Budget tight? LDAP sync or email/password

---

### Large Enterprise (10,000 users)

**Option 1: OAuth2 Proxy + Azure AD Premium P1**
- Infrastructure: $100-200/month
- IdP: $60,000/month
- **Total:** $60,100-60,200/month ($721,200-722,400/year)

**Option 2: OAuth2 Proxy + Okta**
- Infrastructure: $100-200/month
- IdP: $20,000-50,000/month
- **Total:** $20,100-50,200/month ($241,200-602,400/year)

**Recommendation:** Use existing enterprise IdP  
Most enterprises already have Azure AD or Okta

---

## Implementation Timeline

### 8-Week Implementation Plan

**Week 1:** Planning & Design
- Choose identity provider
- Review security requirements
- Architect SSO flow
- Get stakeholder approval

**Week 2:** Identity Provider Setup
- Register OAuth application
- Configure redirect URIs
- Set up conditional access
- Test IdP configuration

**Week 3:** OAuth2 Proxy Deployment
- Deploy proxy container (Cloud Run / Fargate)
- Configure environment variables
- Store secrets securely
- Set up health checks

**Week 4:** Integration & Testing
- Update load balancer
- Test SSO login flow
- Test all client apps
- Verify security settings

**Week 5:** User Provisioning
- Export users from IdP
- Create provisioning script
- Invite users to Vaultwarden
- Verify accounts

**Week 6:** Documentation & Training
- Create user guides
- Document troubleshooting
- Train support team
- Prepare announcement

**Week 7:** Pilot Rollout
- Deploy to 10-20 pilot users
- Monitor and gather feedback
- Refine documentation

**Week 8:** Full Rollout
- Announce to all users
- Monitor adoption
- Address support tickets

**Total:** 8 weeks from planning to production

---

## Security Benefits

### With SSO:

✅ **Centralized Authentication**
- Single identity source
- Easier to audit
- Consistent policies

✅ **MFA Enforcement**
- Enforced at IdP level
- Cannot be bypassed
- Multiple factor options

✅ **Conditional Access**
- Device compliance checks
- Geographic restrictions
- Risk-based access
- Time-based policies

✅ **Automated Provisioning/Deprovisioning**
- New hires get access automatically
- Departures lose access immediately
- Reduces security risk

✅ **Audit & Compliance**
- Centralized audit logs
- Login attempts tracked
- Compliance reporting easier
- SOC 2 / ISO 27001 alignment

✅ **Reduced Password Fatigue**
- One login for multiple apps
- Fewer passwords to remember
- Better security hygiene

**Still Maintains Zero-Knowledge Encryption:**
- Master password never sent to server
- Vault data never exposed
- Even compromised SSO doesn't expose vault

---

## Limitations

### What SSO Cannot Do:

❌ **Bypass Master Password**
- Master password always required
- Cannot be eliminated (zero-knowledge requirement)
- SSO only handles identity, not encryption

❌ **Work with Mobile/Desktop Apps**
- Mobile apps: Must use email/password
- Desktop apps: Must use email/password
- Browser extensions: Work with SSO
- CLI: Uses API tokens

**Reason:** Apps connect directly to Vaultwarden API, bypass proxy

**Workaround:** Users use same email/password as SSO

❌ **Automatic Just-in-Time Provisioning**
- Users must be pre-provisioned in Vaultwarden
- Cannot auto-create accounts on first SSO login
- Requires bulk provisioning or API script

---

## Decision Matrix

| Factor | Email/PW + 2FA | LDAP Sync | OAuth2 Proxy |
|--------|----------------|-----------|--------------|
| **Cost** | $0 | $0 | $40-6,000+/month |
| **Setup Time** | 0 | 2-3 weeks | 6-8 weeks |
| **Complexity** | Low | Medium | High |
| **User Experience** | Good | Good | Excellent |
| **Centralized Auth** | ❌ | ✅ | ✅ |
| **True SSO** | ❌ | ❌ | ✅ |
| **MFA Enforcement** | Manual | IdP | IdP |
| **Conditional Access** | ❌ | ❌ | ✅ |
| **Audit Logs** | Vaultwarden | IdP | IdP |
| **Mobile Apps** | ✅ | ✅ | ⚠️ (fallback) |
| **Desktop Apps** | ✅ | ✅ | ⚠️ (fallback) |
| **Browser Extensions** | ✅ | ✅ | ✅ |
| **Best For** | < 100 users | 100-1K users | 1K+ users |

---

## Recommendation by Organization Size

### 1-100 Users
**Recommendation:** Email/Password + 2FA  
**Why:** Simplicity, $0 cost, adequate security  
**Skip SSO:** Overhead not justified

### 100-1,000 Users
**Recommendation:** LDAP Sync (if existing AD) OR Email/Password + 2FA  
**Why:** Balance of cost and management  
**Consider SSO if:** Already have Azure AD Premium or Okta

### 1,000-10,000 Users
**Recommendation:** OAuth2 Proxy + Existing IdP  
**Why:** Centralized management critical at scale  
**ROI Positive:** $1k-60k/year vs manual management costs

### 10,000+ Users
**Recommendation:** OAuth2 Proxy + Enterprise IdP (Azure AD Premium / Okta)  
**Why:** Required for compliance, audit, and security  
**Cost Justified:** Essential for enterprise operations

---

## Comparison with Commercial Solutions

### Bitwarden Official (Commercial)

**Includes native SSO support:**
- SAML 2.0
- OAuth 2.0 / OIDC
- Login with SSO
- Master password optional

**Cost:** $6-10/user/month ($72,000-120,000/year for 1,000 users)

**Trade-off:**
- ✅ Native SSO (no proxy)
- ✅ Official support
- ❌ 100x more expensive
- ❌ Must migrate from Vaultwarden

---

### This Solution (Vaultwarden + OAuth2 Proxy)

**Hybrid SSO approach:**
- OAuth 2.0 / OIDC
- Login with SSO
- Master password required

**Cost:** $40-6,000/month depending on IdP (vs $72k-120k/year)

**Trade-off:**
- ✅ 90-95% cost savings
- ✅ Same security
- ❌ Requires setup
- ❌ Extra infrastructure

---

## FAQ

**Q: Can users skip the master password?**  
A: No. Master password is required for zero-knowledge encryption. Cannot be bypassed.

**Q: Will mobile apps work with SSO?**  
A: Mobile apps must use email/password (direct API connection). Users can use same credentials as SSO.

**Q: What if our IdP goes down?**  
A: New logins fail (SSO unavailable). Existing sessions continue working. Can implement fallback.

**Q: Can we use multiple IdPs?**  
A: Yes, oauth2-proxy supports multiple providers. Users choose which to use.

**Q: What about compliance (SOC 2, ISO 27001)?**  
A: SSO helps with compliance by centralizing auth, audit logs, and access controls.

**Q: How do we handle contractors/external users?**  
A: Option 1: Add to IdP as guests. Option 2: Create Vaultwarden-only accounts (email/password).

---

## Next Steps

### Decide if You Need SSO

1. **Evaluate:** Organization size, budget, requirements
2. **Choose:** Email/PW, LDAP, or OAuth2 Proxy
3. **Budget:** Approve costs (IdP + infrastructure)
4. **Review:** Implementation plan
5. **Proceed:** Or defer for later

### If Proceeding with OAuth2 Proxy:

6. **Choose IdP:** Azure AD, Google, Okta, or Keycloak
7. **Week 1:** Planning and design
8. **Week 2:** IdP configuration
9. **Week 3:** Proxy deployment
10. **Week 4:** Testing
11. **Week 5:** User provisioning
12. **Week 6:** Documentation
13. **Week 7:** Pilot
14. **Week 8:** Full rollout

---

## Documentation

### Complete SSO Guides

- 📋 **[SSO Implementation Plan](SSO_IMPLEMENTATION_PLAN.md)** - Complete technical plan
- 📋 **[Azure AD Setup](SSO_SETUP_AZURE_AD.md)** - Step-by-step Azure AD configuration
- 📋 **Google Workspace Setup** - Coming soon
- 📋 **Okta Setup** - Coming soon
- 📋 **Keycloak Setup** - Coming soon

### Related Documentation

- 🔐 **[Security Guide](../operations/SECURITY.md)** - Overall security architecture
- 📈 **[Scaling Guide](../operations/SCALING_GUIDE.md)** - Infrastructure scaling
- 🚀 **[Deployment Guides](../deployment/)** - Cloud deployment

---

## Conclusion

**SSO with Vaultwarden is achievable but requires thoughtful architecture.**

**Key Takeaways:**
1. ✅ SSO handles authentication (identity)
2. ✅ Master password handles vault unlock (encryption)
3. ✅ Both required (cannot skip master password)
4. ✅ OAuth2 Proxy recommended approach
5. ✅ Cost: $40-6,000+/month depending on IdP
6. ✅ Implementation: 6-8 weeks
7. ✅ Worth it for 1,000+ users
8. ❌ Skip for < 100 users (use email/password + 2FA)

**Recommended Action:** Evaluate organization size and needs. For < 100 users, skip SSO. For 100-1,000 users, consider LDAP sync. For 1,000+ users, invest in OAuth2 Proxy + existing IdP.

---

**Status:** Documentation complete, ready for implementation evaluation

**Questions?** adrian207@gmail.com

**Last Updated:** November 5, 2025

