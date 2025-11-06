# Browser Extension Setup Guide

**Author:** Adrian Johnson <adrian207@gmail.com>

## Quick Start (5 Minutes)

Your self-hosted Vaultwarden works perfectly with the **official Bitwarden browser extensions**. No custom extensions needed!

### Step 1: Install Extension (2 minutes)

Choose your browser:

#### Chrome / Edge / Brave / Opera
1. Visit: [https://chrome.google.com/webstore/detail/bitwarden-free-password-m/nngceckbapebfimnlniiiahkandclblb](https://chrome.google.com/webstore/detail/bitwarden-free-password-m/nngceckbapebfimnlniiiahkandclblb)
2. Click **"Add to Chrome"** (or Edge/Brave)
3. Click **"Add extension"**
4. ✅ Extension installed!

#### Firefox
1. Visit: [https://addons.mozilla.org/en-US/firefox/addon/bitwarden-password-manager/](https://addons.mozilla.org/en-US/firefox/addon/bitwarden-password-manager/)
2. Click **"Add to Firefox"**
3. Click **"Add"**
4. ✅ Extension installed!

#### Safari
1. Visit Mac App Store
2. Search for **"Bitwarden"**
3. Click **"Get"**
4. Enable in Safari > Preferences > Extensions
5. ✅ Extension installed!

---

### Step 2: Configure Self-Hosted Server (2 minutes)

**Important:** You MUST configure the extension to use your self-hosted server.

#### For All Browsers:

1. **Click the Bitwarden icon** in your browser toolbar
2. **Click "Create Account"** (or login if you see that)
3. **BEFORE entering anything**, click **"⚙️ Settings"** (top right)
4. Find **"Server URL"** or **"Self-hosted Environment"**
5. Click **"Specify server URL"** or similar option
6. Enter your Vaultwarden URL:
   ```
   https://vault.example.com
   ```
   (Replace with YOUR actual domain)
7. Click **"Save"**
8. ✅ Extension configured!

**Screenshots:**

```
┌─────────────────────────────────┐
│  Bitwarden                [⚙️]  │
├─────────────────────────────────┤
│                                 │
│  Email: ___________________     │
│                                 │
│  Master password: _________     │
│                                 │
│  [Login]  [Create Account]      │
│                                 │
│  ⚠️ Click ⚙️ Settings first!     │
│     to set server URL           │
└─────────────────────────────────┘
```

---

### Step 3: Create Account or Login (1 minute)

#### If You Haven't Created an Account:
1. Click extension icon
2. Click **"Create Account"**
3. Enter your email
4. Create a **strong master password** (16+ characters)
   - ⚠️ **NEVER forget this!** Cannot be recovered!
5. Click **"Submit"**
6. Verify email (check your inbox)
7. ✅ Account created!

#### If You Already Have an Account:
1. Click extension icon
2. Enter your email
3. Enter master password
4. Click **"Log in"**
5. ✅ Logged in!

---

### Step 4: Start Using (1 minute)

#### Save Your First Password:
1. Go to any website with a login form
2. Enter credentials and login
3. Bitwarden will prompt: **"Save login?"**
4. Click **"Yes"**
5. ✅ Password saved!

#### Auto-fill Saved Password:
1. Go to a website where you saved credentials
2. Click the Bitwarden icon in the login field
   OR
   Click the extension icon and select the login
3. ✅ Password auto-filled!

#### Generate Strong Password:
1. Click extension icon
2. Click **"Generator"** tab
3. Adjust settings (length, characters)
4. Click **"Copy"**
5. ✅ Strong password generated!

---

## Detailed Configuration

### Server URL Format

Your server URL should be:
```
https://vault.example.com
```

**DO NOT include:**
- ❌ `/` at the end
- ❌ `/api` path
- ❌ Port numbers (unless custom)
- ❌ `http://` (must be HTTPS)

**Examples:**
- ✅ `https://vault.company.com`
- ✅ `https://bitwarden.example.org`
- ✅ `https://vaultwarden-prod-abc123.run.app` (Cloud Run)
- ✅ `https://my-alb-123456.us-east-1.elb.amazonaws.com` (AWS ALB)
- ❌ `https://vault.example.com/`
- ❌ `https://vault.example.com/api`
- ❌ `http://vault.example.com`

### Advanced Settings

#### Vault Timeout
Control when the extension locks:

1. Click extension icon
2. Settings > Vault Timeout
3. Choose:
   - **Immediately** - Lock on browser close
   - **1 minute** - Lock after 1 min idle
   - **5 minutes** - Lock after 5 min idle
   - **15 minutes** - Recommended
   - **1 hour**
   - **Never** - Stay unlocked (⚠️ not recommended)

#### Biometric Unlock
Enable fingerprint/face unlock:

1. Settings > Security
2. Enable **"Unlock with biometrics"**
3. Follow your OS prompts
4. ✅ Biometric unlock enabled!

**Supported on:**
- ✅ Windows Hello (Windows 10/11)
- ✅ Touch ID (macOS)
- ✅ Fingerprint (Linux with compatible hardware)

#### Auto-fill on Page Load
Automatically fill credentials when visiting login pages:

1. Settings > Options
2. Enable **"Auto-fill on page load"**
3. ⚠️ **Warning:** Less secure, only enable for trusted sites

#### Default URI Match Detection
How Bitwarden matches saved logins to websites:

1. Settings > Options
2. **Default URI match detection:**
   - **Base domain** (Recommended) - Matches all subdomains
   - **Host** - Exact subdomain match
   - **Starts with** - Flexible matching
   - **Regex** - Advanced pattern matching
   - **Exact** - Must match exactly
   - **Never** - Manual selection only

---

## Features Guide

### Auto-fill
**Automatically fill login credentials:**

#### Method 1: Click Field Icon
1. Click username or password field
2. Click Bitwarden icon that appears
3. Select the login
4. ✅ Credentials filled!

#### Method 2: Extension Popup
1. Navigate to login page
2. Click extension icon
3. Search or select login
4. Click the login entry
5. ✅ Credentials filled!

#### Method 3: Keyboard Shortcut
- **Chrome/Edge:** `Ctrl+Shift+L` (Windows) or `Cmd+Shift+L` (Mac)
- **Firefox:** `Ctrl+Shift+L` (Windows) or `Cmd+Shift+L` (Mac)

### Auto-save
**Automatically save new credentials:**

1. Enter credentials on a new site
2. Submit/login
3. Bitwarden prompts: **"Save this login?"**
4. Options:
   - **Yes** - Save to vault
   - **Never for this site** - Ignore permanently
   - **Not now** - Skip this time
5. Edit details if needed
6. Click **"Save"**
7. ✅ Credentials saved!

### Password Generator
**Generate strong passwords:**

1. Click extension icon
2. Click **"Generator"** tab
3. Configure:
   - **Length:** 8-128 characters (recommended: 16+)
   - **Include:** Uppercase, lowercase, numbers, symbols
   - **Avoid ambiguous:** Reduces confusion (0/O, 1/l)
4. Click **"Regenerate"** until satisfied
5. Click **"Copy"** to clipboard
6. ✅ Strong password ready!

**Example strong password:**
```
K9$mPz2@vL4xN8wQ
```

### Secure Notes
**Store sensitive text securely:**

1. Click extension icon
2. Click **"+"** (Add item)
3. Select **"Secure Note"**
4. Enter:
   - Name
   - Notes (sensitive text)
5. Click **"Save"**
6. ✅ Secure note saved!

**Use cases:**
- WiFi passwords
- Server credentials
- Recovery codes
- Personal information
- Secure links

### Credit Cards
**Store payment information:**

1. Extension icon > **"+"** > **"Card"**
2. Enter:
   - Cardholder name
   - Card number
   - Expiration date
   - Security code (CVV)
3. Click **"Save"**
4. ✅ Card saved!

**Auto-fill on checkout pages!**

### Identities
**Store personal information:**

1. Extension icon > **"+"** > **"Identity"**
2. Enter:
   - Name
   - Address
   - Phone
   - Email
   - etc.
3. Click **"Save"**
4. ✅ Identity saved!

**Auto-fill on forms!**

---

## Troubleshooting

### Extension Not Connecting

**Symptoms:**
- "Connection refused" error
- "Unable to reach server"
- Login button does nothing

**Solutions:**

1. **Verify server URL:**
   - Settings > Check server URL
   - Must be exact: `https://vault.example.com`
   - No trailing slash

2. **Check HTTPS certificate:**
   - Visit server URL in browser
   - Should show 🔒 (secure)
   - If certificate error, extension won't connect

3. **Test server directly:**
   ```bash
   curl https://vault.example.com/alive
   # Should return: HTTP 200
   ```

4. **Check firewall:**
   - Ensure port 443 is open
   - Check browser proxy settings

5. **Clear extension cache:**
   - Settings > Log out
   - Clear browser cache
   - Re-configure server URL
   - Log in again

---

### Auto-fill Not Working

**Solutions:**

1. **Check URI match:**
   - Edit login item
   - Verify URI is correct
   - Try different match detection

2. **Check form fields:**
   - Some sites use non-standard fields
   - Try manual copy-paste

3. **Disable conflicting extensions:**
   - Other password managers
   - Form fillers
   - Privacy extensions might block

4. **Re-detect fields:**
   - Settings > Options
   - **"Clear cache"**
   - Reload page

---

### Master Password Not Working

**⚠️ CRITICAL: If you forget your master password, your data is UNRECOVERABLE!**

**If you know it but it's not working:**

1. **Check caps lock:** Master password is case-sensitive
2. **Try copy-paste:** Eliminate typing errors
3. **Check keyboard layout:** Different language?

**If you truly forgot it:**
- ❌ No recovery possible (zero-knowledge encryption)
- ❌ Support cannot help
- ✅ Only option: Delete account and start fresh
- 💡 **Prevention:** Write it down and store securely!

---

### Sync Not Working

**Solutions:**

1. **Force sync:**
   - Settings > Sync
   - Click **"Sync vault now"**

2. **Check connection:**
   - Verify internet connection
   - Test server URL in browser

3. **Re-login:**
   - Log out
   - Log back in
   - Sync should resume

4. **Check server logs:**
   ```bash
   # AWS
   aws logs tail /aws/ecs/vaultwarden-prod --follow
   
   # GCP
   gcloud run services logs read vaultwarden-prod-service --follow
   ```

---

### Extension Updates

**Automatic:**
- Browser automatically updates extensions
- Usually within 24-48 hours of release
- No action needed

**Manual:**
1. Browser > Extensions > Manage Extensions
2. Enable **"Developer mode"** (top right)
3. Click **"Update"**
4. ✅ Extensions updated!

---

## Security Best Practices

### Master Password

✅ **DO:**
- Use 16+ characters
- Mix uppercase, lowercase, numbers, symbols
- Make it memorable but unique
- Write it down and store securely offline
- Use a passphrase: `correct-horse-battery-staple-2025!`

❌ **DON'T:**
- Reuse from other services
- Share with anyone
- Store in plain text digitally
- Use dictionary words only
- Use personal information

### Vault Timeout

**Recommended settings:**
- **Office/work:** 15 minutes
- **Home:** 30-60 minutes
- **Public computer:** Immediately or 1 minute
- **Shared computer:** Never log in!

### Biometric Unlock

**Safe to enable IF:**
- ✅ You trust your device
- ✅ Only you have biometric access
- ✅ Device is encrypted
- ✅ Device has screen lock

**Don't enable IF:**
- ❌ Shared computer
- ❌ Public computer
- ❌ Someone could access your biometrics

### Two-Factor Authentication

**Enable 2FA on your Vaultwarden account:**
1. Web vault > Settings > Two-step Login
2. Choose method:
   - **Authenticator app** (Recommended)
   - **Email**
   - **YubiKey** (Most secure)
3. Save recovery code!
4. ✅ 2FA enabled!

---

## Keyboard Shortcuts

### Windows / Linux
- `Ctrl+Shift+L` - Auto-fill last used login
- `Ctrl+Shift+9` - Generate password
- `Ctrl+Shift+Y` - Open extension popup

### macOS
- `Cmd+Shift+L` - Auto-fill last used login
- `Cmd+Shift+9` - Generate password
- `Cmd+Shift+Y` - Open extension popup

### Customize:
1. Browser > Extensions > Keyboard shortcuts
2. Find "Bitwarden"
3. Assign custom shortcuts

---

## Multi-Device Sync

Your vault automatically syncs across:
- ✅ All browsers (Chrome, Firefox, Edge, etc.)
- ✅ Desktop apps (Windows, Mac, Linux)
- ✅ Mobile apps (iOS, Android)
- ✅ Web vault

**Just login with the same account!**

**Sync happens:**
- On login
- Every 30 minutes (automatic)
- On manual sync (Settings > Sync)
- On vault changes

---

## Import Existing Passwords

### From Chrome
1. Chrome > Settings > Passwords
2. Click ⋮ > Export passwords
3. Save CSV file
4. Bitwarden web vault > Tools > Import Data
5. Format: **Chrome (csv)**
6. Select file > Import
7. ✅ Passwords imported!

### From Firefox
1. Firefox > about:logins
2. Click ⋮ > Export Logins
3. Save CSV file
4. Bitwarden web vault > Tools > Import Data
5. Format: **Firefox (csv)**
6. Select file > Import
7. ✅ Passwords imported!

### From 1Password / LastPass / Others
1. Export from existing password manager
2. Bitwarden web vault > Tools > Import Data
3. Select format (1Password, LastPass, etc.)
4. Select file > Import
5. ✅ Passwords imported!

⚠️ **After import:** Delete exported files securely!

---

## Getting Help

### Documentation
- 📖 [Getting Started](../GETTING_STARTED.md)
- 🔧 [Troubleshooting](../deployment/TROUBLESHOOTING.md)
- 📊 [Scaling Guide](../operations/SCALING_GUIDE.md)

### Support
- **Official Bitwarden Help:** https://bitwarden.com/help/
- **Vaultwarden Wiki:** https://github.com/dani-garcia/vaultwarden/wiki
- **Community:** Reddit r/Bitwarden
- **Issues:** GitHub Issues

### Your Self-Hosted Instance
- **Admin Panel:** `https://vault.example.com/admin`
- **Server Logs:** See deployment guide for your cloud provider
- **Email:** adrian207@gmail.com for deployment support

---

## Summary

✅ **Install official Bitwarden extension** (5 minutes)  
✅ **Configure self-hosted server URL** (2 minutes)  
✅ **Create account or login** (1 minute)  
✅ **Start saving passwords** (immediate)

**No custom extensions needed!** The official Bitwarden extensions work perfectly with your self-hosted Vaultwarden instance.

**Total setup time:** < 10 minutes  
**Cost:** $0  
**Maintenance:** Automatic updates

---

**Next Steps:**
1. Install extension in your browser(s)
2. Configure server URL
3. Login or create account
4. Import existing passwords (optional)
5. Enable 2FA for security
6. Install on mobile devices
7. Enjoy self-hosted password management!

**Questions?** See [Browser Extensions Plan](BROWSER_EXTENSIONS_PLAN.md) for detailed information about custom extensions.

