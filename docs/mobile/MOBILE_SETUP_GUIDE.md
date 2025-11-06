# Mobile Apps Setup Guide

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Estimated Time:** 5-10 minutes

## Quick Start

Your self-hosted Vaultwarden works perfectly with the **official Bitwarden mobile apps** for iOS and Android. No custom apps needed!

---

## iOS Setup (iPhone/iPad)

### Step 1: Download App (2 minutes)

1. **Open App Store** on your iPhone/iPad
2. **Search:** "Bitwarden Password Manager"
3. **Download:** Tap "GET" (it's free)
4. **Open:** Tap "OPEN" or find app icon

✅ App installed!

---

### Step 2: Configure Server (2 minutes)

⚠️ **CRITICAL:** You must configure the app to use YOUR self-hosted server.

1. **Open Bitwarden app**
2. **Tap** ⚙️ (Settings icon) in top-right
3. **Scroll down** to "Self-hosted"
4. **Enter your server URL:**
   ```
   https://vault.yourcompany.com
   ```
   (Use YOUR actual domain)
5. **Tap "Save"**

**Important:**
- Must start with `https://`
- No trailing slash `/`
- Exact URL from your deployment

✅ Server configured!

---

### Step 3: Create Account or Login (2 minutes)

#### If You Already Have an Account:

1. **Tap** "← Back" (top-left)
2. **Enter:**
   - Email: `your-email@company.com`
   - Master password: Your password
3. **Tap "Log in"**
4. **Enable Face ID/Touch ID** when prompted (recommended)

✅ Logged in!

#### If This Is Your First Account:

1. **Tap "Create account"**
2. **Enter:**
   - Email: `your-email@company.com`
   - Name: Your name (optional)
   - Master password: Create STRONG password (16+ characters)
   - Confirm password: Re-enter
3. **Tap "Submit"**
4. **Enable Face ID/Touch ID** when prompted

⚠️ **IMPORTANT:** Write down your master password! Cannot be recovered if forgotten.

✅ Account created!

---

### Step 4: Enable Auto-Fill (3 minutes)

This allows Bitwarden to fill passwords in Safari and other apps.

1. **Close Bitwarden** app
2. **Open iPhone Settings** (⚙️)
3. **Tap "Passwords"**
4. **Tap "Password Options"**
5. **Turn ON "AutoFill Passwords"**
6. **Select "Bitwarden"** (checkmark it)
7. **Turn OFF** other password managers (if any)

✅ Auto-fill enabled!

---

### Step 5: Test It! (2 minutes)

1. **Open Safari**
2. **Go to any website** with login (e.g., github.com)
3. **Tap username field**
4. **Tap 🔑 (key icon)** above keyboard
5. **Authenticate** with Face ID/Touch ID
6. **Tap a login** (or create new one)

✅ It works!

---

## Android Setup

### Step 1: Download App (2 minutes)

1. **Open Google Play Store**
2. **Search:** "Bitwarden Password Manager"
3. **Install:** Tap "Install" (it's free)
4. **Open:** Tap "OPEN" or find app icon

✅ App installed!

---

### Step 2: Configure Server (2 minutes)

⚠️ **CRITICAL:** You must configure the app to use YOUR self-hosted server.

1. **Open Bitwarden app**
2. **Tap** ☰ (Menu icon) in top-left
3. **Tap "Settings"**
4. **Scroll to "Self-hosted Environment"**
5. **Enter your server URL:**
   ```
   https://vault.yourcompany.com
   ```
   (Use YOUR actual domain)
6. **Tap "Save"**

✅ Server configured!

---

### Step 3: Create Account or Login (2 minutes)

#### If You Already Have an Account:

1. **Tap** ← (Back)
2. **Enter:**
   - Email: `your-email@company.com`
   - Master password: Your password
3. **Tap "Log in"**
4. **Enable fingerprint** when prompted (recommended)

✅ Logged in!

#### If This Is Your First Account:

1. **Tap "Create account"**
2. **Enter:**
   - Email: `your-email@company.com`
   - Name: Your name (optional)
   - Master password: Create STRONG password (16+ characters)
   - Confirm password: Re-enter
3. **Tap "Submit"**
4. **Enable fingerprint** when prompted

⚠️ **IMPORTANT:** Write down your master password! Cannot be recovered if forgotten.

✅ Account created!

---

### Step 4: Enable Auto-Fill (3 minutes)

This allows Bitwarden to fill passwords in all apps and browsers.

1. **Open Android Settings**
2. **Search:** "Autofill"
3. **Tap "Autofill service"** (or "Passwords & accounts")
4. **Select "Bitwarden"**
5. **Grant permissions** when prompted
6. **(Optional) Disable battery optimization:**
   - Settings → Apps → Bitwarden
   - Battery → Unrestricted

✅ Auto-fill enabled!

---

### Step 5: Test It! (2 minutes)

1. **Open Chrome or any app**
2. **Go to login page** (e.g., github.com)
3. **Tap username field**
4. **Bitwarden suggestion appears**
5. **Tap the suggestion**
6. **Authenticate** if needed

✅ It works!

---

## Common Features

### Save a Password

**When you login to any app/website:**
1. Enter credentials and login
2. Bitwarden notification appears: "Save?"
3. Tap "Yes"
4. ✅ Password saved!

---

### Generate Password

1. **Open Bitwarden app**
2. **Tap "Generator"** tab
3. **Adjust settings:**
   - Length: 16+ recommended
   - Characters: All checked
4. **Tap "Copy"**
5. **Use in signup form**

✅ Strong password generated!

---

### View Saved Passwords

1. **Open Bitwarden app**
2. **Browse** or **search** for item
3. **Tap** to view details
4. **Tap** 👁️ to show password
5. **Tap** to copy username/password

---

### Enable Biometric Unlock

**iOS (Face ID / Touch ID):**
1. Bitwarden → Settings → Security
2. Enable "Unlock with Face ID" or "Touch ID"
3. Verify with master password
4. ✅ Biometric unlock enabled!

**Android (Fingerprint / Face):**
1. Bitwarden → Settings → Security
2. Enable "Unlock with biometrics"
3. Verify with master password
4. ✅ Biometric unlock enabled!

---

### Sync Vault

**Auto-sync:**
- Happens every 30 minutes automatically
- Happens when you open app

**Manual sync:**
1. Open Bitwarden app
2. Pull down to refresh
3. ✅ Vault synced!

---

## Troubleshooting

### Issue: "Unable to reach server"

**Solutions:**

1. **Verify server URL:**
   - Settings → Check URL exactly
   - Must be: `https://vault.yourcompany.com`
   - No typos

2. **Test in browser:**
   - Open Safari/Chrome
   - Go to: `https://vault.yourcompany.com`
   - Should load Bitwarden web vault

3. **Check internet:**
   - WiFi or cellular data connected?
   - Try different network

4. **Clear app cache:**
   - Log out of app
   - Close app completely
   - Reopen and login

---

### Issue: Auto-fill not working (iOS)

**Solutions:**

1. **Check Settings:**
   - iPhone Settings → Passwords
   - Verify Bitwarden is selected
   - Only Bitwarden should be checked

2. **Restart iPhone:**
   - Sometimes needed after setup

3. **Update iOS:**
   - Settings → General → Software Update
   - Auto-fill requires iOS 12+

---

### Issue: Auto-fill not working (Android)

**Solutions:**

1. **Check Autofill Service:**
   - Android Settings → Autofill service
   - Must be set to "Bitwarden"

2. **Check Permissions:**
   - Settings → Apps → Bitwarden → Permissions
   - All required permissions granted

3. **Try Accessibility:**
   - Bitwarden Settings → Options
   - Enable "Use accessibility"
   - Grant accessibility permission
   - Fallback auto-fill method

4. **Disable Battery Optimization:**
   - Settings → Apps → Bitwarden → Battery
   - Select "Unrestricted"

---

### Issue: Master password not working

⚠️ If truly forgotten, there is NO recovery!

**If you know it but not working:**

1. **Check caps lock**
2. **Try copy-paste**
3. **Check keyboard language**

**If forgotten:**
- No recovery possible
- Must delete account and start over
- All data will be lost

**Prevention:** Write it down on paper, store securely!

---

### Issue: App crashes or freezes

**Solutions:**

1. **Force close app:**
   - iOS: Swipe up from bottom, swipe app away
   - Android: Recent apps button, swipe away

2. **Restart device**

3. **Update app:**
   - Check App Store/Play Store for updates

4. **Reinstall app:**
   - Uninstall
   - Reinstall
   - Login (vault syncs back)

---

## Advanced Features

### Bitwarden Send

**Share passwords/files temporarily:**

1. Open Bitwarden app
2. Tap "Send" tab
3. Choose "Text" or "File"
4. Enter content or select file
5. Set expiration (hours/days)
6. Tap "Create Send"
7. Share link with recipient

**Use cases:**
- Share password with non-user
- Send file securely
- Temporary access

---

### Password Health Report

**Check password security:**

1. Open Bitwarden app
2. Tap "Tools"
3. Tap "Password Health Report"
4. Review:
   - Exposed passwords
   - Reused passwords
   - Weak passwords
5. Update as needed

**Recommendation:** Check monthly

---

### TOTP Generator

**Built-in 2FA codes:**

1. Edit login item
2. Add custom field → "TOTP"
3. Scan QR code from website
4. Save
5. TOTP code displays on item
6. Auto-copies with password

**No separate authenticator app needed!**

---

## Tips & Best Practices

### Security

✅ **DO:**
- Enable biometric unlock
- Use strong master password (16+ chars)
- Enable 2FA on account
- Set vault timeout (15 min)
- Review password health monthly
- Write down master password (paper, safe)

❌ **DON'T:**
- Share master password
- Use same password elsewhere
- Disable auto-lock
- Store master password digitally
- Forget to sync important passwords

---

### Organization

✅ **DO:**
- Create folders (Work, Personal, Banking)
- Mark favorites for quick access
- Use descriptive names
- Add notes to items
- Tag items appropriately

---

### Performance

✅ **DO:**
- Use WiFi for initial sync
- Enable auto-sync
- Keep app updated
- Close unused apps

---

## Multi-Device Sync

Your vault automatically syncs across:
- ✅ iPhone/iPad
- ✅ Android phone/tablet
- ✅ Web browsers (Chrome, Firefox, etc.)
- ✅ Desktop apps (Windows, Mac, Linux)
- ✅ Browser extensions

**Just login with same account everywhere!**

---

## Next Steps

After successful setup:

1. **Import existing passwords:**
   - Web vault: Tools → Import
   - Supported: Chrome, Firefox, 1Password, LastPass, etc.

2. **Install on other devices:**
   - Desktop: [bitwarden.com/download](https://bitwarden.com/download/)
   - Browser extensions: Chrome/Firefox store

3. **Enable 2FA:**
   - Web vault: Settings → Two-step Login
   - Use authenticator app

4. **Explore features:**
   - Secure notes
   - Credit cards
   - Identities
   - File attachments

---

## Support

**App Issues:**
- Bitwarden Help: [bitwarden.com/help](https://bitwarden.com/help/)
- Community: r/Bitwarden

**Server Issues:**
- Your admin panel: `https://vault.yourcompany.com/admin`
- Deployment guides: See docs/
- Email: adrian207@gmail.com

---

## Success Checklist

- [ ] App installed (iOS or Android)
- [ ] Server URL configured
- [ ] Account created or logged in
- [ ] Auto-fill enabled in system settings
- [ ] At least one password saved
- [ ] Auto-fill tested and working
- [ ] Biometric unlock enabled
- [ ] Master password written down and stored safely

**All checked?** ✅ You're ready!

---

**Setup Time:** 5-10 minutes  
**Difficulty:** Easy  
**Cost:** $0

**Enjoy secure password management on your mobile device! 📱**

