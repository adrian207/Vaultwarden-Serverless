# Browser Extension Installation Guide

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Last Updated:** November 5, 2025  
**Estimated Time:** 5-10 minutes

## Overview

Your self-hosted Vaultwarden instance works seamlessly with the official Bitwarden browser extensions. No custom software required!

---

## ✅ Checklist

Follow these steps in order:

- [ ] **Step 1:** Install browser extension (2 minutes)
- [ ] **Step 2:** Configure server URL (2 minutes)  
- [ ] **Step 3:** Create account or login (1 minute)
- [ ] **Step 4:** Test auto-fill (2 minutes)
- [ ] **Step 5:** Enable 2FA (optional but recommended)

**Total Time:** 5-10 minutes

---

## Step 1: Install Browser Extension

### Chrome / Edge / Brave / Opera

1. **Open Chrome Web Store:**
   - Visit: [https://chrome.google.com/webstore/detail/bitwarden-free-password-m/nngceckbapebfimnlniiiahkandclblb](https://chrome.google.com/webstore/detail/bitwarden-free-password-m/nngceckbapebfimnlniiiahkandclblb)

2. **Install:**
   - Click **"Add to Chrome"** (or Edge/Brave/Opera)
   - Click **"Add extension"** in the popup

3. **Verify:**
   - Look for the Bitwarden icon 🔐 in your browser toolbar
   - ✅ Extension installed!

**Screenshot Guide:**
```
Browser Toolbar → Look for: 🔐 Bitwarden icon
If not visible: Click puzzle piece icon → Pin Bitwarden
```

---

### Firefox

1. **Open Firefox Add-ons:**
   - Visit: [https://addons.mozilla.org/en-US/firefox/addon/bitwarden-password-manager/](https://addons.mozilla.org/en-US/firefox/addon/bitwarden-password-manager/)

2. **Install:**
   - Click **"Add to Firefox"**
   - Click **"Add"** in the popup
   - Click **"Okay, Got It"**

3. **Verify:**
   - Look for the Bitwarden icon 🔐 in your toolbar
   - ✅ Extension installed!

---

### Safari (macOS)

1. **Open Mac App Store:**
   - Search for **"Bitwarden"**
   - Or visit: [https://apps.apple.com/app/bitwarden/id1352778147](https://apps.apple.com/app/bitwarden/id1352778147)

2. **Install:**
   - Click **"Get"**
   - Enter Apple ID password if prompted
   - Click **"Install"**

3. **Enable in Safari:**
   - Open Safari
   - Safari → Preferences → Extensions
   - Check **"Bitwarden"**
   - ✅ Extension enabled!

---

## Step 2: Configure Server URL ⚠️ **CRITICAL STEP**

**⚠️ YOU MUST DO THIS:** The extension defaults to Bitwarden's commercial servers. You need to point it to YOUR self-hosted server.

### All Browsers:

1. **Click the Bitwarden icon** 🔐 in your toolbar

2. **Access Settings:**
   - Look for ⚙️ (gear icon) in the top-right corner
   - Click it

3. **Find Server Configuration:**
   - Scroll down to find **"Server URL"** section
   - Or look for **"Self-hosted Environment"**
   - Click **"Specify your server URL"** or similar button

4. **Enter Your Server URL:**
   ```
   https://vault.yourcompany.com
   ```
   
   **⚠️ IMPORTANT:**
   - Use YOUR actual domain (from deployment)
   - Must start with `https://`
   - No trailing slash `/`
   - No `/api` path
   
   **Example URLs:**
   - ✅ `https://vault.example.com`
   - ✅ `https://passwords.company.org`
   - ✅ `https://vaultwarden-prod-xyz.run.app` (GCP)
   - ✅ `https://my-alb-123.us-east-1.elb.amazonaws.com` (AWS)
   - ❌ `https://vault.example.com/` (no trailing slash)
   - ❌ `https://vault.example.com/api` (no /api)
   - ❌ `http://vault.example.com` (must be HTTPS)

5. **Save Settings:**
   - Click **"Save"** or **"Submit"**
   - Extension will test connection
   - ✅ Configuration complete!

**Visual Guide:**
```
Extension Popup
├── [⚙️ Settings] ← Click here
│
└── Settings Page
    ├── Server URL Section
    │   ├── [ ] Use default servers
    │   └── [✓] Specify server URL
    │       └── Input: https://vault.yourcompany.com
    │       └── [Save] ← Click here
```

---

## Step 3: Create Account or Login

### If You Already Created an Account:

1. **Return to extension main screen:**
   - Click the ← (back) button
   - Or click the extension icon again

2. **Login:**
   - Email: `your-email@company.com`
   - Master password: `YourStrongPassword123!`
   - Click **"Log in"**
   - ✅ Logged in!

---

### If This Is Your First Account:

1. **Click "Create Account":**
   - On the extension main screen

2. **Enter Details:**
   - **Email:** `your-email@company.com`
   - **Name:** `Your Name` (optional)
   - **Master Password:** Create a STRONG password
     - Minimum 12 characters (recommend 16+)
     - Mix uppercase, lowercase, numbers, symbols
     - Example: `My$ecureP@ssw0rd2025!`
   - **Confirm Password:** Re-enter

3. **Master Password Tips:**
   ⚠️ **CRITICAL:** Write this down and store securely!
   - ✅ **DO:** Write on paper, store in safe
   - ✅ **DO:** Use a memorable passphrase
   - ✅ **DO:** Make it unique (never reused)
   - ❌ **DON'T:** Store in plain text
   - ❌ **DON'T:** Share with anyone
   - ❌ **DON'T:** Use personal info only
   
   **⚠️ IF FORGOTTEN:** There is NO recovery! Zero-knowledge encryption means even administrators cannot reset your password.

4. **Submit:**
   - Check "I have read and agree to Terms of Service" (your instance)
   - Click **"Submit"** or **"Create Account"**
   - ✅ Account created!

5. **Verify Email (if configured):**
   - Check your email inbox
   - Click verification link
   - ✅ Email verified!

---

## Step 4: Test Auto-Fill

Let's verify everything works:

### Test 1: Save a Password

1. **Visit a website with login:**
   - Example: `https://github.com` (if you have account)
   - Or any site where you have credentials

2. **Login normally:**
   - Enter username/email
   - Enter password
   - Click "Login"

3. **Bitwarden prompt appears:**
   - "Add login for github.com?"
   - Click **"Yes"**
   - ✅ Password saved!

### Test 2: Auto-Fill Saved Password

1. **Log out of the website**

2. **Return to login page**

3. **Auto-fill options:**
   
   **Method A:** Click field icon
   - Click in username field
   - Bitwarden icon appears in field
   - Click it
   - Select your login
   - ✅ Credentials filled!

   **Method B:** Use extension
   - Click Bitwarden icon 🔐
   - Search or select login
   - Click the entry
   - ✅ Credentials filled!

   **Method C:** Keyboard shortcut
   - Press `Ctrl+Shift+L` (Windows/Linux)
   - Or `Cmd+Shift+L` (Mac)
   - ✅ Last used credentials filled!

### Test 3: Generate Password

1. **Click Bitwarden icon** 🔐

2. **Click "Generator" tab**

3. **Adjust settings:**
   - Length: 16 characters
   - Options: All checked
   - Click regenerate until satisfied

4. **Copy password:**
   - Click **"Copy"**
   - ✅ Strong password copied to clipboard!

**If all tests pass:** ✅ Setup complete!

---

## Step 5: Enable Two-Factor Authentication (Recommended)

**⚠️ HIGHLY RECOMMENDED:** Add 2FA for security.

### Setup TOTP (Authenticator App):

1. **Access Web Vault:**
   - Go to `https://vault.yourcompany.com`
   - Login with your credentials

2. **Navigate to Settings:**
   - Click profile icon (top right)
   - Click **"Account Settings"**
   - Click **"Security"**
   - Find **"Two-step Login"**

3. **Choose Method:**
   - **Authenticator App** (Recommended)
     - Free, works offline
     - Use: Google Authenticator, Authy, Microsoft Authenticator
   - **Email** (Backup option)
     - Requires email configured
   - **YubiKey** (Most secure)
     - Requires physical key

4. **For Authenticator App:**
   - Click **"Manage"** next to "Authenticator App"
   - Enter master password
   - Scan QR code with authenticator app
   - Enter 6-digit code from app
   - **⚠️ SAVE RECOVERY CODE!**
     - Print or write down
     - Store securely
     - Needed if you lose phone
   - Click **"Enable"**
   - ✅ 2FA enabled!

5. **Test 2FA:**
   - Log out
   - Log in again
   - Enter 6-digit code when prompted
   - ✅ 2FA working!

---

## Common Issues & Solutions

### Issue 1: "Unable to reach server"

**Symptoms:**
- Extension shows error on login
- "Connection refused" or timeout

**Solutions:**

1. **Verify server URL:**
   - Settings → Check URL exactly
   - Must match: `https://vault.yourcompany.com`
   - No typos, no extra slashes

2. **Test server in browser:**
   ```bash
   # Open browser and go to:
   https://vault.yourcompany.com/alive
   
   # Should see: HTTP 200 response
   ```

3. **Check SSL certificate:**
   - Browser should show 🔒 (secure)
   - If certificate error, extension won't connect
   - Fix SSL certificate first

4. **Clear extension data:**
   - Log out from extension
   - Settings → Clear cache
   - Re-configure server URL
   - Try again

---

### Issue 2: Master password not working

**Solutions:**

1. **Check caps lock:** Password is case-sensitive

2. **Try copy-paste:** Eliminate typing errors

3. **Check keyboard layout:** Different language?

4. **Verify account exists:**
   - Try web vault: `https://vault.yourcompany.com`
   - Same credentials work there?

**⚠️ If truly forgotten:**
- No recovery possible (zero-knowledge encryption)
- Must delete account and create new one
- All data will be lost

---

### Issue 3: Auto-fill not working

**Solutions:**

1. **Check URI:**
   - Extension → Edit login item
   - Verify URI matches website
   - Try different match detection

2. **Permissions:**
   - Browser → Extension permissions
   - Ensure "Access your data for all websites" enabled

3. **Conflicting extensions:**
   - Disable other password managers
   - Disable form fillers temporarily
   - Test again

4. **Re-detect fields:**
   - Log out and back in to extension
   - Clear browser cache
   - Revisit website

---

### Issue 4: Sync not working

**Solutions:**

1. **Manual sync:**
   - Extension → Settings
   - Find "Sync"
   - Click "Sync vault now"

2. **Check connection:**
   - Test server URL in browser
   - Verify internet connection

3. **Re-login:**
   - Log out completely
   - Close browser
   - Reopen and log in
   - Sync should resume

---

## Browser-Specific Notes

### Chrome / Edge / Brave:
- ✅ Full feature support
- ✅ Biometric unlock (Windows Hello)
- ✅ All autofill features work
- 🔄 Auto-updates enabled by default

### Firefox:
- ✅ Full feature support
- ❌ No biometric unlock (Firefox limitation)
- ✅ All autofill features work
- 🔄 Auto-updates enabled by default

### Safari:
- ⚠️ Partial biometric support (Touch ID on Mac)
- ⚠️ Some form detection limitations
- ✅ Core features work well
- 🔄 Updates through Mac App Store

---

## Next Steps

After successful installation:

1. **Import existing passwords:**
   - [Import Guide](../operations/IMPORT_PASSWORDS.md)

2. **Install on other devices:**
   - Desktop app: [Download](https://bitwarden.com/download/)
   - Mobile: iOS / Android app stores
   - Use same server URL and credentials

3. **Enable additional security:**
   - Vault timeout: 15 minutes recommended
   - Require master password on restart
   - Enable biometric unlock (if supported)

4. **Organize your vault:**
   - Create folders for work/personal
   - Mark favorites for quick access
   - Add secure notes for other sensitive data

5. **Share with team (if applicable):**
   - Organizations feature in web vault
   - Create collections
   - Invite team members

---

## Support

**Issues with extension:**
- Bitwarden Help: [https://bitwarden.com/help/](https://bitwarden.com/help/)
- Community: [r/Bitwarden](https://reddit.com/r/Bitwarden)

**Issues with your deployment:**
- Deployment guides: [docs/deployment/](../deployment/)
- Admin panel: `https://vault.yourcompany.com/admin`
- Email: adrian207@gmail.com

---

## Success Checklist

Before considering setup complete:

- [ ] Extension installed in browser
- [ ] Server URL configured correctly
- [ ] Account created or logged in
- [ ] At least one password saved
- [ ] Auto-fill tested and working
- [ ] Password generator tested
- [ ] 2FA enabled (highly recommended)
- [ ] Recovery code saved securely
- [ ] Master password written down and stored safely

**All checked?** ✅ You're ready to use Vaultwarden!

---

**Setup Time:** 5-10 minutes  
**Difficulty:** Easy  
**Support:** Available in docs/ or adrian207@gmail.com

**Enjoy secure, self-hosted password management! 🔐**

