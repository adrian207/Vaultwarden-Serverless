# Browser Extensions - Frequently Asked Questions

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Last Updated:** November 5, 2025

## General Questions

### Q: Do I need custom browser extensions?

**A:** No! The official Bitwarden extensions work perfectly with your self-hosted Vaultwarden. Just configure the server URL and you're ready to go.

**Why this works:**
- Vaultwarden is 100% API-compatible with Bitwarden
- All official clients (browser, desktop, mobile) work without modification
- You get all features, updates, and security audits for free

---

### Q: What's the difference between Bitwarden and Vaultwarden?

**A:** 
- **Bitwarden** = Commercial password manager service + open-source client apps
- **Vaultwarden** = Unofficial, lightweight server implementation (Rust)
- **Your Setup** = Vaultwarden server (self-hosted) + Official Bitwarden clients

**Key Points:**
- You're hosting the SERVER yourself (Vaultwarden)
- You're using OFFICIAL clients (Bitwarden apps/extensions)
- Clients don't know or care which server implementation
- Everything works seamlessly

---

### Q: Why does the extension say "Bitwarden"?

**A:** Because you're using the official Bitwarden extension. This is intentional and correct.

**It's like:**
- Gmail app connecting to your own email server
- Outlook connecting to your Exchange server
- Chrome accessing your own website

The branding shows the client name, not your server. This is normal and expected.

---

### Q: Can I customize or rebrand the extensions?

**A:** Not easily. Options:

1. **Use official extensions as-is** (Recommended)
   - Works perfectly
   - Zero cost
   - Zero maintenance
   - Shows "Bitwarden" branding

2. **Fork and customize** (Enterprise only)
   - 3-6 months development
   - $200,000+ cost
   - Ongoing maintenance
   - Custom branding
   - Only worth it for 10,000+ users

**For 99% of users:** Option 1 is the right choice.

---

## Installation & Setup

### Q: Which browsers are supported?

**A:**
- ✅ Chrome
- ✅ Firefox
- ✅ Edge
- ✅ Safari
- ✅ Opera
- ✅ Brave
- ✅ Vivaldi
- ✅ Tor Browser (Firefox-based)

**Basically:** All major browsers.

---

### Q: How do I configure the extension for my self-hosted server?

**A:** Simple 3-step process:

1. Install extension from browser store
2. Click ⚙️ Settings in extension
3. Enter your server URL: `https://vault.yourcompany.com`

**Full guide:** [Installation Guide](INSTALLATION_GUIDE.md)

---

### Q: What should the server URL be?

**A:** Your Vaultwarden deployment URL from Terraform outputs.

**Format:**
```
https://your-domain.com
```

**Examples:**
- `https://vault.company.com`
- `https://passwords.example.org`
- `https://vaultwarden-prod.run.app` (GCP Cloud Run)
- `https://my-alb-123.elb.amazonaws.com` (AWS ALB)

**Don't include:**
- ❌ Trailing slash: `https://vault.com/`
- ❌ API path: `https://vault.com/api`
- ❌ Port (unless custom): `https://vault.com:8000`
- ❌ HTTP: `http://vault.com` (must be HTTPS)

---

### Q: Can I use the extension without creating an account?

**A:** No. You must create an account to use Vaultwarden.

**Why:**
- Your vault is encrypted with your master password
- Account stores your encrypted vault
- Zero-knowledge means server never knows your passwords

**Don't worry:** Account creation takes 2 minutes and is free.

---

### Q: Do I need a separate account for each browser?

**A:** No! One account syncs everywhere.

**Login with same credentials on:**
- Chrome (work computer)
- Firefox (home computer)
- Edge (laptop)
- Safari (Mac)
- Mobile apps (iOS/Android)
- Desktop apps (Windows/Mac/Linux)

**Vault syncs automatically** across all devices.

---

## Security

### Q: Is my master password sent to the server?

**A:** NO! Zero-knowledge architecture means:

1. Master password stays on YOUR device
2. Client derives encryption key from it
3. Vault is encrypted locally
4. Encrypted vault sent to server
5. Server NEVER sees your master password

**Even admins cannot:**
- See your passwords
- Reset your master password
- Decrypt your vault
- Access your data

---

### Q: What if I forget my master password?

**A:** ⚠️ **CRITICAL:** There is NO recovery!

**Zero-knowledge encryption means:**
- Admin cannot reset password
- Support cannot help
- Recovery codes don't help with master password
- **Your data is permanently inaccessible**

**Only option:** Delete account and start over.

**Prevention:**
- ✅ Write it down on paper
- ✅ Store paper in safe place
- ✅ Use memorable passphrase
- ❌ Never store digitally in plain text

---

### Q: Should I enable two-factor authentication?

**A:** YES! Highly recommended.

**Why 2FA:**
- Protects if master password is compromised
- Required for many compliance standards
- Small effort, huge security gain
- Takes 5 minutes to setup

**Recommended method:**
- **Authenticator app** (Google Authenticator, Authy, Microsoft Authenticator)
- Free, works offline, very secure

**Also available:**
- Email (if SMTP configured)
- YubiKey (most secure, requires hardware)
- Duo (requires subscription)

---

### Q: How secure is the browser extension?

**A:**
- ✅ Security-audited by Bitwarden
- ✅ Open source (community reviewed)
- ✅ Used by millions of users
- ✅ Regular security updates
- ✅ Follows browser security best practices

**More secure than:**
- Browser's built-in password manager
- Writing passwords down
- Reusing passwords
- Spreadsheets

**Security features:**
- End-to-end encryption (AES-256)
- Secure password derivation (PBKDF2)
- Auto-lock on timeout
- Biometric unlock support
- Clipboard clearing

---

### Q: Can websites steal my passwords through the extension?

**A:** No. Multiple protections:

1. **Domain matching:** Extension only fills on matching domains
2. **User confirmation:** You control when to fill
3. **Isolated storage:** Extension data protected by browser
4. **No JavaScript access:** Websites can't read extension memory
5. **HTTPS only:** Extension warns on HTTP sites

**Best practices:**
- Only auto-fill on HTTPS sites
- Verify URL before filling
- Don't disable security warnings

---

## Features & Usage

### Q: What features are included?

**A:** All premium Bitwarden features:

**Core:**
- ✅ Auto-fill logins
- ✅ Auto-save new passwords
- ✅ Password generator
- ✅ Secure notes
- ✅ Credit cards
- ✅ Identities
- ✅ File attachments
- ✅ Folders and collections
- ✅ Favorites
- ✅ Search and filtering

**Security:**
- ✅ Two-factor authentication
- ✅ Biometric unlock
- ✅ Vault timeout
- ✅ Password health reports
- ✅ Breach monitoring
- ✅ Emergency access

**Sharing:**
- ✅ Organizations (teams)
- ✅ Secure sharing
- ✅ Collections
- ✅ Bitwarden Send

**Advanced:**
- ✅ Import/export
- ✅ Custom fields
- ✅ TOTP generator
- ✅ API access
- ✅ CLI tools

**Cost:** $0 (all features included in self-hosted)

---

### Q: How do I import passwords from Chrome/Firefox?

**A:** Easy import process:

**From Chrome:**
1. Chrome Settings → Passwords
2. Export passwords (saves CSV)
3. Bitwarden web vault → Tools → Import
4. Select "Chrome (csv)"
5. Upload file → Import

**From Firefox:**
1. about:logins → Export
2. Save CSV file
3. Same import process as Chrome

**From other password managers:**
- 1Password, LastPass, KeePass, etc.
- All supported formats
- Instructions in web vault

**⚠️ After import:** Delete exported CSV files securely!

---

### Q: Can I use the extension offline?

**A:** Partially.

**Works offline:**
- ✅ View saved passwords
- ✅ Auto-fill from cache
- ✅ Generate passwords
- ✅ Search vault
- ✅ Copy passwords

**Requires online:**
- ❌ Add new items
- ❌ Edit items
- ❌ Delete items
- ❌ Sync changes
- ❌ Login to extension

**How it works:**
- Extension caches vault locally
- Cache encrypted with master password
- Manual sync when back online

---

### Q: How do I share passwords with my team?

**A:** Use Organizations feature:

1. Web vault → Organizations → New Organization
2. Create organization (e.g., "Engineering Team")
3. Invite members by email
4. Create collections (e.g., "AWS Credentials")
5. Add items to collections
6. Members auto-sync shared items

**Permissions:**
- Owner: Full control
- Admin: Manage users
- User: View/use passwords
- Manager: Manage collections

**Shared items:**
- Appear in members' vaults
- Encrypted per-user
- Synced automatically
- Audited for compliance

---

## Troubleshooting

### Q: Extension not connecting to my server

**Check:**

1. **Server URL correct?**
   - Settings → Verify exactly
   - Try copying from Terraform output

2. **Server running?**
   ```bash
   curl https://vault.yourcompany.com/alive
   # Should return HTTP 200
   ```

3. **SSL certificate valid?**
   - Browser should show 🔒
   - No certificate errors
   - If self-signed, add to trusted certificates

4. **Firewall blocking?**
   - Check port 443 open
   - Check browser proxy settings
   - Try different network

5. **Clear extension cache:**
   - Log out
   - Clear browser cache
   - Re-configure and try again

**Still stuck?** See [Troubleshooting Guide](../deployment/TROUBLESHOOTING.md)

---

### Q: Auto-fill not working on certain websites

**Solutions:**

1. **Check URI match:**
   - Edit login item
   - Verify URI correct
   - Try "Base domain" match type

2. **Non-standard forms:**
   - Some sites use unusual fields
   - Try manual copy-paste
   - Report to Bitwarden (they can fix)

3. **Conflicting extensions:**
   - Disable other password managers
   - Disable autofill extensions
   - Test with just Bitwarden

4. **Site blocking:**
   - Some sites block autofill
   - Use copy-paste instead
   - Contact site support

**Known problematic sites:**
- Government sites (security policies)
- Banking sites (sometimes)
- Sites with custom security

---

### Q: Extension keeps logging me out

**Solutions:**

1. **Increase timeout:**
   - Settings → Vault Timeout
   - Change from "Immediately" to "15 minutes"
   - Or "On browser restart"

2. **Enable biometric unlock:**
   - Stays unlocked longer
   - Quick re-authentication
   - Settings → Security → Biometric

3. **Check browser settings:**
   - Ensure browser not clearing data on close
   - Settings → Privacy → On exit

4. **Pin extension:**
   - Keeps extension active
   - Browser → Extensions → Pin Bitwarden

---

### Q: Sync seems slow or not working

**Solutions:**

1. **Manual sync:**
   - Extension → Settings → Sync
   - Click "Sync vault now"

2. **Check sync settings:**
   - Sync interval: 30 minutes default
   - Can force sync anytime

3. **Network issues:**
   - Verify internet connection
   - Check firewall not blocking
   - Try different network

4. **Server issues:**
   - Check server logs
   - Verify server healthy
   - See deployment guide

5. **Re-login:**
   - Log out completely
   - Log back in
   - Sync should resume

---

## Comparison Questions

### Q: How does this compare to LastPass/1Password?

**A:**

| Feature | This Solution | LastPass | 1Password |
|---------|--------------|----------|-----------|
| **Cost** | $15-45/mo for 1000 users | $8/user/mo = $8,000/mo | $19.95/user/mo = $19,950/mo |
| **Self-hosted** | ✅ Yes | ❌ No | ❌ No |
| **Open source** | ✅ Yes | ❌ No | ❌ No |
| **Data privacy** | ✅ You control | ❌ Their servers | ❌ Their servers |
| **Features** | ✅ All | ✅ All | ✅ All |
| **Browser extensions** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Mobile apps** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Team sharing** | ✅ Yes | ✅ Yes | ✅ Yes |

**Savings for 1,000 users:**
- vs LastPass: **$93,840/year**
- vs 1Password: **$237,240/year**

**This solution wins on:**
- Cost (90% cheaper)
- Privacy (your data, your servers)
- Control (you manage everything)
- Compliance (data stays in your infrastructure)

---

### Q: Why not just use browser's built-in password manager?

**A:** Browser password managers have limitations:

**Browser password manager:**
- ❌ Single browser only (doesn't sync to others)
- ❌ Basic security (not zero-knowledge)
- ❌ No organization/sharing features
- ❌ No secure notes or other item types
- ❌ Limited password generator
- ❌ No password health analysis
- ❌ No emergency access
- ❌ No audit logs

**Vaultwarden:**
- ✅ Works everywhere (all browsers, mobile, desktop)
- ✅ Military-grade encryption
- ✅ Team features (organizations, sharing, collections)
- ✅ Secure notes, cards, identities, files
- ✅ Advanced password generator
- ✅ Password health reports
- ✅ Emergency access
- ✅ Complete audit trail

**Use case:** Browser manager for casual use, Vaultwarden for security-conscious users and businesses.

---

## Cost & Licensing

### Q: Is there any ongoing cost for the extensions?

**A:** No! Zero cost forever.

**Why it's free:**
- Official Bitwarden extensions are open source
- Distributed through browser stores (free)
- No licensing fees
- No per-user costs
- No subscription required

**You only pay for:**
- Cloud infrastructure ($15-8,000/month depending on scale)
- Your time for setup/management

**Extensions themselves:** $0

---

### Q: What about mobile apps and desktop apps?

**A:** Also free and work the same way!

**Available apps:**
- Mobile: iOS and Android (free in app stores)
- Desktop: Windows, Mac, Linux (free download)
- CLI: Command-line tool (free)
- All configured the same way (just enter server URL)

**Cost:** $0 for all apps

---

## Support

### Q: Where can I get help?

**A:**

**For extension issues:**
- Official Bitwarden Help: https://bitwarden.com/help/
- Community: r/Bitwarden on Reddit
- GitHub: Bitwarden clients issues

**For self-hosted deployment:**
- This documentation: [docs/](../)
- Vaultwarden Wiki: https://github.com/dani-garcia/vaultwarden/wiki
- Your admin panel: `https://vault.yourcompany.com/admin`
- Email: adrian207@gmail.com

**For security issues:**
- Email: adrian207@gmail.com (do not open public issues)
- Bitwarden security: security@bitwarden.com

---

### Q: Can I get commercial support?

**A:** Options:

**Included (free):**
- Documentation (comprehensive)
- Community support (active)
- Self-service troubleshooting

**Available (paid):**
- Deployment consultation
- Custom feature development
- SLA-backed support
- Training sessions
- Contact: adrian207@gmail.com for quote

---

## Still Have Questions?

**Check these resources:**
- 📖 [Installation Guide](INSTALLATION_GUIDE.md)
- 🔧 [Troubleshooting Guide](../deployment/TROUBLESHOOTING.md)
- 📋 [Complete Extensions Plan](BROWSER_EXTENSIONS_PLAN.md)
- 💬 [GitHub Discussions](https://github.com/your-repo/discussions)
- ✉️ Email: adrian207@gmail.com

**Can't find your answer?** Open a GitHub issue or email adrian207@gmail.com

---

**Last Updated:** November 5, 2025  
**Questions about this FAQ?** Submit a pull request or open an issue.

