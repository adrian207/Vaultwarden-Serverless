# Organization & Team Features Guide

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Date:** November 5, 2025  
**Status:** Documentation Complete - Ready for Use

## Executive Summary

**Good News:** Vaultwarden includes full organization and team collaboration features out of the box!

**What You Get:**
- ✅ Organizations (unlimited)
- ✅ User groups and collections
- ✅ Secure password sharing
- ✅ Role-based access control (RBAC)
- ✅ Granular permissions
- ✅ Event logs and auditing
- ✅ Emergency access
- ✅ Directory sync (LDAP)

**Cost:** $0 (all features included in self-hosted Vaultwarden)

**vs Commercial Bitwarden:**
- Bitwarden Teams: $5/user/month ($60/year)
- Bitwarden Enterprise: $7/user/month ($84/year)
- Vaultwarden: **$0** (all enterprise features free!)

**Savings for 100 users:** $6,000-8,400/year

---

## Understanding Organizations

### What is an Organization?

An **Organization** in Vaultwarden is a shared vault for teams where:
- Multiple users can access shared passwords
- Admins control who can access what
- Items can be organized in collections
- Access can be granted by user or group
- Full audit trail of all actions

**Use Cases:**
- Company-wide shared credentials
- Department-specific passwords
- Project team collaboration
- Client access management
- Vendor credential sharing

---

### Organization vs Personal Vault

**Personal Vault:**
- Private to individual user
- Not shared with anyone
- User has full control
- No admin oversight

**Organization Vault:**
- Shared with team members
- Managed by admins/owners
- Controlled access (collections)
- Audit logs of all activity
- Can be accessed by multiple users

**Users have BOTH:** Personal vault + Organization vault(s)

---

## Organization Roles

### Owner

**Highest level of control**

**Can:**
- ✅ Manage all organization settings
- ✅ Add/remove users
- ✅ Assign all roles
- ✅ Create/manage collections
- ✅ Delete organization
- ✅ View all items
- ✅ Manage billing (in commercial; N/A for self-hosted)

**Best For:** CEO, IT Director, System Administrator

**Recommendation:** Limit to 1-2 trusted individuals

---

### Admin

**Full management capabilities (except deleting org)**

**Can:**
- ✅ Add/remove users
- ✅ Assign roles (except Owner)
- ✅ Create/manage collections
- ✅ Manage groups
- ✅ View all items
- ✅ Manage policies

**Cannot:**
- ❌ Delete organization
- ❌ Remove owners
- ❌ Change organization settings (some)

**Best For:** IT Managers, Security Team

**Recommendation:** 2-5 admins depending on org size

---

### User

**Standard team member**

**Can:**
- ✅ Access assigned collections
- ✅ Add items to collections (if permitted)
- ✅ Edit items in collections (if permitted)
- ✅ Share items with other collection members
- ✅ Use passwords for auto-fill

**Cannot:**
- ❌ Manage users
- ❌ Create collections
- ❌ Change permissions
- ❌ View unassigned collections

**Best For:** Employees, team members

**Recommendation:** Most users should be this role

---

### Manager

**Collection-level management**

**Can:**
- ✅ Create and manage specific collections
- ✅ Assign users to their collections
- ✅ Manage items in their collections
- ✅ View assigned collections

**Cannot:**
- ❌ Manage all collections
- ❌ Add/remove users from organization
- ❌ Assign admin roles
- ❌ View all items

**Best For:** Team Leads, Department Managers

**Recommendation:** 5-10% of users

---

### Custom Role (via Permissions)

**Granular control through collection assignments**

**Examples:**
- Read-only access to specific collections
- Edit access to subset of collections
- Mixed permissions across collections

**Configured via:** Collection assignments + permissions

---

## Collections

### What are Collections?

**Collections** are folders within an organization that group related items together.

**Think of collections as:**
- Departments (HR, Finance, Engineering)
- Projects (Project Alpha, Client X)
- Environments (Production, Staging, Development)
- Applications (AWS, Google Workspace, GitHub)

**Benefits:**
- Organize passwords logically
- Grant access to specific teams
- Separate concerns (developers don't see HR passwords)
- Fine-grained permissions

---

### Collection Permissions

**For each collection, users can have:**

**Can View:**
- See items in collection
- Use passwords for login
- Cannot edit or add items

**Can View & Edit:**
- See and modify existing items
- Cannot add new items
- Cannot delete items

**Can View, Edit & Add:**
- Full access to collection
- Add new items
- Edit existing items
- Still cannot delete collection

**Best Practice:**
- Most users: View only
- Power users: View & Edit
- Managers: View, Edit & Add
- Admins/Owners: Full access

---

### Collection Structure Examples

#### Example 1: By Department

```
Organization: Company Vault
├── Collections:
    ├── HR
    │   └── Members: HR Team (View & Edit)
    ├── Finance
    │   └── Members: Finance Team (View & Edit)
    ├── Engineering
    │   ├── Members: Engineers (View & Edit)
    │   └── Sub-collections:
    │       ├── Production Servers
    │       │   └── Members: Senior Engineers (View & Edit)
    │       └── Development Tools
    │           └── Members: All Engineers (View & Edit)
    └── Executives
        └── Members: C-Suite (View & Edit)
```

---

#### Example 2: By Client/Project

```
Organization: Agency Vault
├── Collections:
    ├── Internal Tools
    │   └── Members: All Employees (View & Edit)
    ├── Client: Acme Corp
    │   ├── Members: Acme Team (View & Edit)
    │   └── Sub-collections:
    │       ├── Acme Production
    │       │   └── Members: Senior Devs (View & Edit)
    │       └── Acme Staging
    │           └── Members: All Devs (View)
    └── Client: TechStart
        └── Members: TechStart Team (View & Edit)
```

---

#### Example 3: By Environment

```
Organization: DevOps Vault
├── Collections:
    ├── Production
    │   ├── Members: DevOps Team (View & Edit)
    │   └── Members: Developers (View only)
    ├── Staging
    │   └── Members: All Engineers (View & Edit)
    ├── Development
    │   └── Members: All Engineers (View & Edit)
    └── CI/CD Secrets
        └── Members: DevOps Team (View & Edit)
```

---

## Groups

### What are Groups?

**Groups** simplify user management by assigning permissions to groups instead of individual users.

**Benefits:**
- Manage 100 users with 5 groups instead of 100 individual assignments
- Add new hire to group → instantly gets all permissions
- Remove from group → instantly loses all access
- Change group permissions → affects all members

---

### Group Setup

**Step 1: Create Groups**

Examples:
- HR Team
- Finance Team
- Engineering - Frontend
- Engineering - Backend
- Engineering - DevOps
- Management
- Contractors
- Interns

**Step 2: Assign Users to Groups**

- User can be in multiple groups
- Group membership additive (more groups = more access)

**Step 3: Assign Groups to Collections**

- Grant HR Team access to HR collection
- Grant Engineering groups access to respective collections
- Grant Management access to all collections (read-only)

**Step 4: Manage at Group Level**

- New engineer? Add to "Engineering - Backend" group → done
- Employee promoted? Add to "Management" group → additional access
- Employee leaves? Remove from all groups → access revoked

---

### Group Example

**Group: Engineering - DevOps**

**Members:**
- alice@company.com
- bob@company.com
- charlie@company.com

**Collection Access:**
- Production Servers: View & Edit
- Staging Servers: View & Edit
- Development Servers: View & Edit
- CI/CD Secrets: View & Edit
- AWS Root Accounts: View only

**When you add david@company.com to this group:**
→ Instantly gets access to all 5 collections with specified permissions

---

## Setting Up Your First Organization

### Step 1: Create Organization (5 minutes)

**Via Web Vault:**

1. Login to `https://vault.yourcompany.com`
2. Click **"New Organization"** (top right)
3. Enter Organization Name: `"Company Vault"` or your company name
4. Billing Email: `admin@yourcompany.com` (not used in self-hosted, but required)
5. Plan: Select "Enterprise" (free in self-hosted!)
6. Click **"Submit"**

✅ **Organization created!**

---

### Step 2: Invite Users (10 minutes)

**Option A: Invite Individual Users**

1. Go to Organization → **Manage** → **People**
2. Click **"Invite User"**
3. Enter email: `user@company.com`
4. Select role: User (default), Admin, or Manager
5. Select collections (optional, can assign later)
6. Click **"Save"**
7. User receives invitation email
8. User accepts invitation

**Option B: Bulk Invite via Admin Panel**

1. Go to `https://vault.yourcompany.com/admin`
2. Users section
3. Can invite multiple users at once

**Option C: Automate via API or LDAP Sync**

See: LDAP Configuration section below

---

### Step 3: Create Collections (15 minutes)

1. Go to Organization → **Manage** → **Collections**
2. Click **"New Collection"**
3. Name: `"Engineering"`
4. External ID: (optional, for LDAP sync)
5. Click **"Save"**

Repeat for each department/team/project

**Example Collections:**
- HR
- Finance
- Engineering
- Marketing
- Sales
- Executive Team
- Production Servers
- Development Tools
- Client Access

✅ **Collections created!**

---

### Step 4: Assign Users to Collections (15 minutes)

**Method 1: Via Collections**

1. Go to Organization → **Manage** → **Collections**
2. Click on collection (e.g., "Engineering")
3. **Access** tab
4. Click **"Add Users"** or **"Add Groups"**
5. Select users
6. Choose permission level (View, View & Edit, View Edit & Add)
7. Click **"Save"**

**Method 2: Via Users**

1. Go to Organization → **Manage** → **People**
2. Click on user
3. **Collections** tab
4. Checkboxes for each collection
5. Choose permission level
6. Click **"Save"**

✅ **Users assigned to collections!**

---

### Step 5: Add Shared Items (10 minutes)

**Create New Item in Organization:**

1. Click **"New Item"** (+ icon)
2. Select **"Organization"** instead of "Personal"
3. Choose organization from dropdown
4. Choose collection(s) to add to
5. Fill in item details:
   - Name: "Production Database"
   - Username: `dbadmin`
   - Password: (generate strong password)
   - URL: `https://db.company.com`
   - Notes: "Production DB - requires VPN"
6. Click **"Save"**

**Move Existing Item from Personal to Organization:**

1. Open personal item
2. Click **"Edit"**
3. Change **"Ownership"** from Personal to Organization
4. Select collection(s)
5. Click **"Save"**

✅ **Shared items added!**

---

## Groups Setup (Optional but Recommended)

### Step 1: Create Groups

1. Go to Organization → **Manage** → **Groups**
2. Click **"New Group"**
3. Name: `"Engineering - DevOps"`
4. External ID: (optional, for LDAP sync)
5. Click **"Save"**

Repeat for each logical group

---

### Step 2: Assign Users to Groups

1. Go to Organization → **Manage** → **Groups**
2. Click on group (e.g., "Engineering - DevOps")
3. **Members** tab
4. Click **"Add Members"**
5. Select users
6. Click **"Save"**

---

### Step 3: Assign Groups to Collections

1. Go to Organization → **Manage** → **Collections**
2. Click on collection
3. **Access** tab
4. Click **"Add Groups"**
5. Select groups
6. Choose permission level
7. Click **"Save"**

✅ **Groups configured!**

---

## Advanced Features

### Event Logs & Auditing

**What's Logged:**
- User logins
- Item access
- Item modifications
- Collection access
- User invitations
- Permission changes
- Organization changes

**How to Access:**

1. Go to Organization → **Manage** → **Events**
2. Filter by:
   - Date range
   - User
   - Event type
   - Item

**Export Events:**
- Click **"Export"**
- CSV format
- Use for compliance reporting

**Use Cases:**
- Security audits
- Compliance reporting (SOC 2, ISO 27001)
- Investigating suspicious activity
- User activity monitoring

---

### Emergency Access

**What is Emergency Access?**

Allows a trusted user (e.g., manager) to request access to another user's vault in case of emergency.

**Use Cases:**
- Employee on medical leave
- Unexpected departure
- Lost master password (rare)
- Business continuity

**How it Works:**

1. **Setup Phase:**
   - User A grants Emergency Access to User B
   - Sets wait time (0 hours to 30 days)
   
2. **Request Phase:**
   - User B requests emergency access
   - User A is notified
   - Wait time starts (unless approved immediately)
   
3. **Access Phase:**
   - After wait time, User B can view User A's vault
   - Or User A can approve immediately
   - User A can reject request

**Configuration:**

1. Settings → **Emergency Access**
2. Click **"Invite"**
3. Enter trusted user's email
4. Select wait time (recommendation: 7-14 days)
5. Click **"Save"**

**Recommendation:** 
- All employees grant emergency access to their manager
- Wait time: 7-14 days (balance of security and urgency)
- Document in employee handbook

---

### Bitwarden Send (Temporary Sharing)

**What is Bitwarden Send?**

Secure way to share text or files temporarily with anyone (even non-users).

**Use Cases:**
- Share password with contractor (expires in 24 hours)
- Send file securely (auto-deletes after download)
- Temporary client access
- Share API key with vendor

**How to Use:**

1. Organization → **Send**
2. Click **"Create Send"**
3. Choose type: Text or File
4. Enter content or upload file
5. Set expiration: 1 hour to 31 days
6. Set deletion date (after expiration)
7. Optional: Set password protection
8. Optional: Maximum access count
9. Click **"Save"**
10. Copy link and share

**Security:**
- End-to-end encrypted
- Auto-expires
- Can require password
- Can limit access count
- Cannot be viewed after deletion

**Example:**

```
Sharing production database password with contractor for 48 hours:

1. Create Send (Text type)
2. Text: "Username: admin\nPassword: SecureP@ss123\nURL: db.company.com"
3. Expiration: 2 days
4. Deletion: Immediately after expiration
5. Password: contractor_pass_2025
6. Max accesses: 5
7. Share link with contractor
```

---

### Two-Step Login for Organizations

**Enforce 2FA for all organization members:**

1. Go to Organization → **Manage** → **Policies**
2. Enable **"Two-step Login"** policy
3. All users must enable 2FA to access organization

**Supported 2FA Methods:**
- Authenticator apps (Authy, Google Authenticator, etc.)
- Email codes
- YubiKey / FIDO2
- Duo Security

**Recommendation:** Always enable for organizations

---

### Master Password Policies

**Enforce strong master passwords:**

1. Go to Organization → **Manage** → **Policies**
2. Enable **"Master Password"** policy
3. Set minimum requirements:
   - Minimum length: 12-16 characters
   - Require uppercase
   - Require lowercase
   - Require numbers
   - Require symbols

**Recommendation:** 
- Minimum 14 characters
- All character types required
- Document in security policy

---

### Password Generator Policies

**Standardize password generation:**

1. Go to Organization → **Manage** → **Policies**
2. Enable **"Password Generator"** policy
3. Set defaults:
   - Default length: 16-24 characters
   - Minimum length: 16 characters
   - Require uppercase/lowercase/numbers/symbols
   - Use words (passphrase) option

**Recommendation:**
- Default to 20 characters
- Minimum 16 characters
- All character types

---

### Personal Ownership Policy

**Prevent users from creating personal items (org-only):**

1. Go to Organization → **Manage** → **Policies**
2. Enable **"Personal Ownership"** policy
3. Effect: Users can only create items in organization, not personal vault

**Use Case:** 
- Highly regulated industries
- Prevent shadow IT
- Ensure all credentials under org control

**Recommendation:** Only for specific compliance requirements

---

## LDAP/Directory Sync

### What is Directory Sync?

Automatically sync users and groups from Active Directory or LDAP to Vaultwarden.

**Benefits:**
- Automatic user provisioning
- Automatic deprovisioning (when user disabled in AD)
- Sync group memberships
- Single source of truth

---

### Vaultwarden Directory Connector

**Setup:**

1. **Install Directory Connector:**
   - Download from [bitwarden.com/download](https://bitwarden.com/download/)
   - Works with Vaultwarden!

2. **Configure Connection:**
   ```json
   {
     "server": "https://vault.yourcompany.com",
     "organizationId": "your-org-id",
     "directoryType": "ldap",
     "ldap": {
       "hostname": "ldap.company.com",
       "port": 636,
       "ssl": true,
       "username": "cn=admin,dc=company,dc=com",
       "password": "secure_password",
       "baseDn": "ou=users,dc=company,dc=com"
     }
   }
   ```

3. **Configure Sync:**
   - User filter: `(&(objectClass=person)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))`
   - Group filter: `(objectClass=group)`
   - Sync interval: Every 30 minutes

4. **Test Sync:**
   - Click "Test" to verify connection
   - Click "Sync" to run initial sync
   - Review imported users and groups

5. **Schedule Automatic Sync:**
   - Run as service/daemon
   - Syncs on schedule (e.g., every 30 minutes)

---

### LDAP Authentication

**Enable LDAP login (users authenticate against AD):**

**Environment Variables:**

```bash
LDAP_ENABLED=true
LDAP_URL=ldaps://ldap.company.com:636
LDAP_BIND_DN=cn=admin,dc=company,dc=com
LDAP_BIND_PASSWORD=secure_password
LDAP_USER_BASE_DN=ou=users,dc=company,dc=com
LDAP_USER_SEARCH_FILTER=(&(objectClass=person)(mail=%s))
LDAP_USER_EMAIL_ATTRIBUTE=mail
LDAP_SYNC_GROUPS=true
LDAP_SYNC_INTERVAL=3600
```

**Benefits:**
- Users login with AD credentials
- Same password as Windows login
- Automatic sync
- Centralized management

---

## Security Best Practices

### Organization Security Checklist

- [ ] **Enable 2FA policy** for all organization members
- [ ] **Set master password policy** (minimum 14 characters)
- [ ] **Create separate collections** for different teams/projects
- [ ] **Use groups** instead of individual user assignments
- [ ] **Limit Owner role** to 1-2 trusted individuals
- [ ] **Limit Admin role** to IT team only
- [ ] **Grant least privilege** (most users should be "User" role)
- [ ] **Review event logs** monthly
- [ ] **Configure emergency access** for business continuity
- [ ] **Document procedures** for adding/removing users
- [ ] **Regular access reviews** (quarterly)
- [ ] **Offboarding process** (immediate access revocation)
- [ ] **Enable LDAP sync** if using Active Directory

---

### Access Control Principles

**Least Privilege:**
- Users only get access to what they need
- Default to read-only
- Grant edit only when necessary

**Separation of Duties:**
- Developers shouldn't see Finance passwords
- HR shouldn't see production server passwords
- Use collections to enforce boundaries

**Regular Reviews:**
- Quarterly access reviews
- Remove unused accounts
- Remove excessive permissions
- Verify group memberships

**Onboarding:**
- Add user to organization
- Assign to appropriate groups
- Grant collection access
- Verify user can access what they need

**Offboarding:**
- Remove from all groups (immediately!)
- Remove from organization
- User loses access to all shared items
- Personal vault remains (if needed for transition)

---

## Scaling Organizations

### Small Team (1-20 users)

**Structure:**
- 1 organization
- 3-5 collections (by department)
- No groups needed (assign users directly)
- 1 Owner, 1 Admin
- Review access monthly

**Estimated Setup Time:** 2-4 hours

---

### Medium Company (20-200 users)

**Structure:**
- 1-2 organizations (main + contractors)
- 10-20 collections (by department + project)
- 5-10 groups
- 1 Owner, 2-3 Admins, 5-10 Managers
- Review access quarterly

**Estimated Setup Time:** 8-16 hours

**Recommendations:**
- Use groups for all assignments
- Enable LDAP sync
- Document procedures
- Designate collection managers

---

### Large Enterprise (200-10,000+ users)

**Structure:**
- 3-5 organizations (by business unit)
- 50-100 collections per org
- 20-50 groups per org
- Multiple Owners/Admins per org
- Dedicated admin team
- Review access quarterly

**Estimated Setup Time:** 40-80 hours initial, ongoing management

**Recommendations:**
- Must use LDAP sync
- Automated provisioning/deprovisioning
- Integration with HRIS
- Formal access request process
- Dedicated password management team
- Regular security audits
- Compliance reporting

---

## Cost Comparison

### Commercial Bitwarden

**Bitwarden Teams:**
- $5/user/month ($60/year)
- Basic organization features
- 2 GB encrypted file storage per org
- Event logs

**Bitwarden Enterprise:**
- $7/user/month ($84/year)
- All Teams features plus:
  - SSO integration (SAML)
  - Directory sync
  - Enterprise policies
  - Families organization sponsorship

**Cost for 100 users:**
- Teams: $6,000/year
- Enterprise: $8,400/year

---

### Self-Hosted Vaultwarden

**All Features Included:**
- ✅ Organizations (unlimited)
- ✅ Collections (unlimited)
- ✅ Groups (unlimited)
- ✅ Event logs
- ✅ Emergency access
- ✅ Bitwarden Send
- ✅ Policies
- ✅ LDAP integration
- ✅ Directory sync
- ✅ Unlimited file storage (limited by your infrastructure)
- ✅ All enterprise features

**Cost for 100 users:** $0

**Savings:** $6,000-8,400/year

**Cost for 1,000 users:**
- Commercial: $60,000-84,000/year
- Vaultwarden: $0
- **Savings: $60,000-84,000/year**

---

## Troubleshooting

### Issue: User can't see organization items

**Causes:**
1. User not assigned to any collections
2. User not in correct group
3. Collection permissions incorrect

**Solutions:**
1. Check Organization → Manage → People → [User] → Collections
2. Verify user in appropriate groups
3. Check collection access settings
4. Try removing and re-adding user

---

### Issue: User can see but not edit items

**Cause:** User has "View" permission only

**Solution:** 
1. Organization → Manage → Collections → [Collection] → Access
2. Find user or group
3. Change permission to "View & Edit" or "View, Edit & Add"

---

### Issue: LDAP sync not working

**Solutions:**
1. Verify LDAP connection: Test connection in Directory Connector
2. Check filters: Ensure user/group filters return results
3. Check permissions: LDAP bind user needs read access
4. Review logs: Check Directory Connector logs for errors
5. Firewall: Ensure port 636 (LDAPS) or 389 (LDAP) open

---

### Issue: Event logs not showing

**Causes:**
1. Database issue
2. Timing (recent events may take a few minutes)

**Solutions:**
1. Wait 5 minutes and refresh
2. Check database connectivity
3. Verify organization admin access

---

## FAQ

**Q: How many organizations can I create?**  
A: Unlimited in self-hosted Vaultwarden.

**Q: Can a user be in multiple organizations?**  
A: Yes, users can be members of multiple organizations.

**Q: What happens to personal items when user joins organization?**  
A: Personal items remain private unless explicitly moved to organization.

**Q: Can I move items between organizations?**  
A: No, items cannot move between organizations. Must delete and recreate.

**Q: How do I delete an organization?**  
A: Only Owners can delete. Organization → Settings → Delete Organization.

**Q: What happens when I delete an organization?**  
A: All organization items are permanently deleted. Users' personal vaults are unaffected.

**Q: Can I recover deleted organization items?**  
A: Only from backups. See: Backup & Restore guide.

**Q: How do I export organization items?**  
A: Organization → Tools → Export Vault → CSV or JSON.

**Q: Can users create their own organizations?**  
A: Yes, by default. Can be disabled via server configuration.

---

## Next Steps

1. **Create organization** (5 minutes)
2. **Invite users** (10 minutes)
3. **Create collections** (15 minutes)
4. **Assign users to collections** (15 minutes)
5. **Add shared items** (10 minutes)
6. **Configure groups** (optional, 30 minutes)
7. **Enable policies** (10 minutes)
8. **Set up LDAP sync** (optional, 60 minutes)
9. **Document procedures** (60 minutes)
10. **Train users** (ongoing)

**Total Setup Time:** 1-4 hours (depending on organization size)

---

## Related Documentation

- 📊 **[Scaling Guide](../operations/SCALING_GUIDE.md)** - Scale organizations to 100,000+ users
- 🔐 **[SSO Integration](../sso/)** - Single Sign-On for enterprises
- 📱 **[Client Applications](../CLIENT_APPLICATIONS_STATUS.md)** - Browser/mobile/desktop access
- 💾 **[Backup & Restore](../operations/BACKUP_RESTORE.md)** - Disaster recovery
- 📈 **[Monitoring](../operations/MONITORING.md)** - Track usage and events

---

## Conclusion

**Vaultwarden includes enterprise-grade organization features at zero cost.**

**Key Takeaways:**
1. ✅ All organization features included (free!)
2. ✅ Unlimited organizations, collections, users
3. ✅ Role-based access control
4. ✅ Groups for easy management
5. ✅ Event logs for auditing
6. ✅ LDAP sync for automation
7. ✅ Scales to 100,000+ users
8. ✅ Saves $60,000-84,000/year vs commercial (1,000 users)

**Recommended Action:** Create your first organization today (1 hour setup) and start sharing passwords securely with your team.

---

**Document Version:** 1.0  
**Last Updated:** November 5, 2025  
**Next Review:** February 2026

**Questions?** adrian207@gmail.com

