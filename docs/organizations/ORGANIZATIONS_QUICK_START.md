# Organization Quick Start Guide

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Estimated Time:** 30-60 minutes  
**Difficulty:** Easy

## Get Your Team Sharing Passwords in 30 Minutes

This guide walks you through creating your first organization and sharing passwords with your team.

---

## What You'll Achieve

By the end of this guide:
- ✅ Organization created
- ✅ Team members invited
- ✅ Collections organized
- ✅ Shared passwords accessible by team
- ✅ Ready for production use

---

## Prerequisites

- ✅ Vaultwarden deployed and accessible
- ✅ Admin access to web vault
- ✅ List of team members' email addresses
- ✅ List of passwords to share

**Estimated Cost:** $0 (all features included!)

---

## Step 1: Create Organization (5 minutes)

1. **Login to Web Vault**
   - Go to: `https://vault.yourcompany.com`
   - Enter your email and master password

2. **Create New Organization**
   - Click **"New Organization"** button (top right)
   - Or click your name → "New Organization"

3. **Fill in Organization Details**
   ```
   Organization Name: Your Company Name
   Billing Email: admin@yourcompany.com
   Plan: Enterprise (free in self-hosted!)
   ```

4. **Click "Submit"**

✅ **Organization created! You are now the Owner.**

---

## Step 2: Create Collections (10 minutes)

Collections organize your shared passwords into logical groups.

**Recommended First Collections:**
- Engineering
- Marketing
- Sales
- Finance
- HR
- Executive Team

**To Create a Collection:**

1. Click your organization name (top left)
2. **Manage** → **Collections**
3. Click **"New Collection"**
4. Enter name: `"Engineering"`
5. Click **"Save"**

**Repeat for each department/team.**

✅ **Collections created!**

**Example Structure:**
```
Company Vault
├── Engineering
├── Marketing
├── Sales
├── Finance
├── HR
└── Executive Team
```

---

## Step 3: Invite Team Members (10 minutes)

**Option A: Invite Individual Users (Recommended for small teams)**

1. **Manage** → **People**
2. Click **"Invite User"**
3. Fill in:
   ```
   Email: john@company.com
   Role: User (default for most team members)
   Collections: Select relevant collections
   ```
4. Click **"Save"**
5. User receives invitation email

**Option B: Bulk Invite (For larger teams)**

1. Create CSV file:
   ```csv
   email,role,collections
   john@company.com,User,"Engineering"
   jane@company.com,User,"Marketing"
   bob@company.com,Admin,"All"
   ```
2. **Manage** → **People** → **Import**
3. Upload CSV
4. Click **"Import"**

**Invitation Email:**
Users will receive an email with a link to accept the invitation.

✅ **Team members invited!**

---

## Step 4: Assign Users to Collections (5 minutes)

**Method 1: During Invitation (Done in Step 3)**

**Method 2: After Invitation**

1. **Manage** → **Collections**
2. Click on collection (e.g., "Engineering")
3. **Access** tab
4. Click **"Add"**
5. Select users
6. Choose permission:
   - **Can View** - Can see and use passwords (read-only)
   - **Can View & Edit** - Can modify existing passwords
   - **Can View, Edit & Add** - Can add new passwords
7. Click **"Save"**

**Recommendation for most users:** Can View & Edit

✅ **Users assigned to collections!**

---

## Step 5: Add Shared Passwords (10 minutes)

**Create New Item in Organization:**

1. Click **"+"** or **"New Item"**
2. **Important:** Change ownership from "Personal" to your organization
3. Select collection(s)
4. Fill in details:
   ```
   Name: Production Database
   Username: dbadmin
   Password: (click generate for strong password)
   URL: https://db.company.com
   Notes: Requires VPN connection
   ```
5. Click **"Save"**

**Move Existing Item from Personal to Organization:**

1. Open personal item
2. Click **"Edit"**
3. Change **"Ownership"** to organization
4. Select collection(s)
5. Click **"Save"**

**Example Items to Share:**
- Company Wi-Fi password
- Shared email accounts
- Social media accounts
- Production server credentials
- Database passwords
- API keys
- Cloud service accounts

✅ **Shared passwords added!**

---

## Step 6: Test Access (5 minutes)

**As an Organization Admin:**

1. Go to organization view
2. Browse collections
3. Verify items are visible

**As a Team Member:**

1. Ask a team member to login
2. They should see organization in sidebar
3. Click on organization
4. They should see assigned collections
5. They should see items in those collections

✅ **Access verified!**

---

## Step 7: Enable Security Policies (5 minutes)

**Recommended Policies:**

### Two-Factor Authentication (2FA)

1. **Manage** → **Policies**
2. Find **"Two-step Login"** policy
3. Toggle **"Enabled"**
4. Effect: All organization members must enable 2FA

### Master Password Requirements

1. **Manage** → **Policies**
2. Find **"Master Password"** policy
3. Toggle **"Enabled"**
4. Set requirements:
   ```
   Minimum length: 14 characters
   Require uppercase: Yes
   Require lowercase: Yes
   Require numbers: Yes
   Require symbols: Yes
   ```

### Password Generator Defaults

1. **Manage** → **Policies**
2. Find **"Password Generator"** policy
3. Toggle **"Enabled"**
4. Set defaults:
   ```
   Default length: 20 characters
   Minimum length: 16 characters
   Require uppercase/lowercase/numbers/symbols: Yes
   ```

✅ **Security policies enabled!**

---

## Step 8: Train Your Team (10 minutes)

**Send this email to your team:**

---

**Subject:** Welcome to [Company] Password Manager

Hi team,

We've set up a company password manager to securely share passwords.

**What you need to do:**

1. **Check your email** for invitation from Bitwarden/Vaultwarden
2. **Click "Join Organization"** in the email
3. **Login** to https://vault.yourcompany.com
4. **Set up 2FA** (required) - Settings → Two-step Login
5. **Browse shared passwords** - Click "Company Vault" in sidebar

**What you can do:**

- Access shared passwords for your team/department
- Add new passwords to shared collections
- Use auto-fill in browser/mobile apps
- Generate strong passwords

**Need help?**

- **Documentation:** [link to your docs]
- **Support:** admin@yourcompany.com

**Security reminders:**

- ✅ Never share your master password
- ✅ Use a strong, unique master password
- ✅ Enable 2FA
- ✅ Only save work passwords in company vault

Questions? Reply to this email!

---

✅ **Team trained!**

---

## Success Checklist

- [ ] Organization created
- [ ] At least 3 collections created
- [ ] Team members invited
- [ ] Users assigned to collections
- [ ] At least 5 shared passwords added
- [ ] Access tested by team member
- [ ] 2FA policy enabled
- [ ] Master password policy enabled
- [ ] Team training email sent
- [ ] Support process documented

**All checked?** ✅ You're ready for production!

---

## What's Next?

### Short Term (This Week)

1. **Monitor adoption**
   - Check event logs: Manage → Events
   - Verify team members are accepting invitations
   - Address any support questions

2. **Add more passwords**
   - Continue migrating shared passwords
   - Organize into appropriate collections

3. **Refine permissions**
   - Adjust user access as needed
   - Create more collections if necessary

### Medium Term (This Month)

4. **Set up groups** (if > 20 users)
   - Create groups by department/team
   - Assign users to groups
   - Assign groups to collections
   - See: Organizations Guide for details

5. **Configure emergency access**
   - Set up manager access for business continuity
   - See: Organizations Guide for details

6. **Review event logs**
   - Monitor for unusual activity
   - Verify expected usage patterns

### Long Term (Ongoing)

7. **Regular access reviews**
   - Quarterly: Review user permissions
   - Remove unused accounts
   - Adjust collections as team changes

8. **Onboarding process**
   - Document steps for adding new hires
   - Automate with LDAP sync (optional)

9. **Offboarding process**
   - Document steps for removing departures
   - Enforce immediate access revocation

---

## Common Tasks

### Add a New Team Member

1. **Manage** → **People**
2. Click **"Invite User"**
3. Enter email, role, collections
4. Click **"Save"**
5. User receives invitation

**Time:** 2 minutes

---

### Remove a Team Member

1. **Manage** → **People**
2. Find user
3. Click settings icon → **"Remove"**
4. Confirm

**Effect:** User immediately loses access to all organization passwords

**Time:** 1 minute

---

### Create a New Collection

1. **Manage** → **Collections**
2. Click **"New Collection"**
3. Enter name
4. Click **"Save"**
5. Assign users or groups

**Time:** 3 minutes

---

### Share a Password with Specific Users

**Option 1: Add to Existing Collection**
1. Create/edit item
2. Set ownership to organization
3. Select collection that contains those users

**Option 2: Create New Collection**
1. Create new collection for specific users
2. Add those users to collection
3. Add item to collection

**Time:** 5 minutes

---

### Temporarily Share a Password with Non-User

**Use Bitwarden Send:**

1. **Send** tab
2. **"Create Send"**
3. Type: Text
4. Enter password
5. Set expiration: 24 hours
6. Set password protection (optional)
7. Click **"Save"**
8. Copy and share link

**Time:** 2 minutes

---

## Troubleshooting

### User can't see organization

**Cause:** User hasn't accepted invitation

**Solution:**
1. Check if invitation was sent: Manage → People → find user
2. Resend invitation if needed
3. Check spam folder
4. Verify email address is correct

---

### User can see organization but no items

**Cause:** User not assigned to any collections

**Solution:**
1. Manage → People → click user
2. Collections tab
3. Assign to relevant collections
4. Set permissions
5. Click "Save"

---

### User can't edit items

**Cause:** User has "View" permission only

**Solution:**
1. Manage → Collections → find collection
2. Access tab
3. Find user
4. Change permission to "Can View & Edit"
5. Click "Save"

---

### Can't invite user

**Possible causes:**
1. User already in organization
2. Invalid email address
3. Server configuration issue

**Solutions:**
1. Check if user already exists: Manage → People
2. Verify email address
3. Check server logs
4. Verify email server configured (if using email invitations)

---

## Tips & Best Practices

### Organization Structure

✅ **DO:**
- Create collections by department/team
- Use descriptive collection names
- Start simple, add complexity as needed
- Document your structure

❌ **DON'T:**
- Create too many collections initially (3-5 is good to start)
- Use vague names ("Stuff", "Misc")
- Grant "All" access to everyone
- Ignore permission levels

---

### User Management

✅ **DO:**
- Grant least privilege (minimal access needed)
- Use "User" role for most team members
- Limit "Admin" role to IT team
- Limit "Owner" role to 1-2 people
- Review permissions quarterly

❌ **DON'T:**
- Make everyone an Admin
- Share Owner access widely
- Forget to remove departed employees
- Grant access "just in case"

---

### Security

✅ **DO:**
- Enable 2FA policy
- Set master password requirements
- Monitor event logs monthly
- Document security procedures
- Train users on security best practices

❌ **DON'T:**
- Disable security policies for convenience
- Ignore event logs
- Allow weak passwords
- Skip user training

---

## Cost Savings Calculator

**Your Organization Size:** ___ users

### Commercial Bitwarden Costs

**Bitwarden Teams:** $5/user/month
- Your cost: ___ users × $5 = $___/month ($___/year)

**Bitwarden Enterprise:** $7/user/month
- Your cost: ___ users × $7 = $___/month ($___/year)

### Vaultwarden Cost

**All Features:** $0/year

### Your Savings

**vs Bitwarden Teams:** $___/year  
**vs Bitwarden Enterprise:** $___/year

**Examples:**
- 10 users: Save $600-840/year
- 50 users: Save $3,000-4,200/year
- 100 users: Save $6,000-8,400/year
- 1,000 users: Save $60,000-84,000/year

---

## Support & Resources

### Documentation

- 📋 **[Complete Organizations Guide](ORGANIZATIONS_GUIDE.md)** - Detailed features
- 🔐 **[Security Best Practices](../operations/SECURITY.md)** - Secure your deployment
- 📈 **[Scaling Guide](../operations/SCALING_GUIDE.md)** - Grow to 100,000+ users

### Need Help?

- **Email:** adrian207@gmail.com
- **Vaultwarden:** [github.com/dani-garcia/vaultwarden](https://github.com/dani-garcia/vaultwarden)
- **Bitwarden Docs:** [bitwarden.com/help](https://bitwarden.com/help/) (compatible with Vaultwarden)

---

## Conclusion

**Congratulations!** You've successfully set up organization password sharing for your team.

**What you've accomplished:**
- ✅ Secure password sharing infrastructure
- ✅ Organized collections for your team
- ✅ Security policies enforced
- ✅ Team trained and ready to use
- ✅ Saved $6,000-84,000/year vs commercial solutions

**Next steps:**
- Continue adding shared passwords
- Monitor usage and adoption
- Refine structure as team grows
- Enjoy secure, seamless password sharing!

---

**Setup Time:** 30-60 minutes  
**Annual Cost:** $0  
**Value:** Secure team collaboration + Massive cost savings

**Questions?** adrian207@gmail.com

**Last Updated:** November 5, 2025

