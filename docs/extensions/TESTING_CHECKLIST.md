# Browser Extension Testing Checklist

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Purpose:** Verify official Bitwarden extensions work with your Vaultwarden deployment  
**Time Required:** 30-45 minutes

## Pre-Testing Setup

Before beginning tests, ensure:

- [ ] Vaultwarden instance deployed and accessible
- [ ] Admin panel accessible at `/admin`
- [ ] SSL certificate valid (browser shows 🔒)
- [ ] At least one test user account created
- [ ] Admin token available

**Server URL:** `_____________________________`  
**Test User Email:** `_____________________________`  
**Test Date:** `_____________________________`  
**Tester Name:** `_____________________________`

---

## Test Suite 1: Installation (Chrome)

### Test 1.1: Install Extension

- [ ] Navigate to Chrome Web Store
- [ ] Search for "Bitwarden Password Manager"
- [ ] Click "Add to Chrome"
- [ ] Extension installed successfully
- [ ] Icon appears in toolbar

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 1.2: Configure Server URL

- [ ] Click extension icon
- [ ] Click settings (⚙️) icon
- [ ] Find "Server URL" section
- [ ] Enter your server URL: `https://vault.yourcompany.com`
- [ ] Click "Save"
- [ ] No error messages appear

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 1.3: Login

- [ ] Return to main extension screen
- [ ] Enter test user email
- [ ] Enter master password
- [ ] Click "Log in"
- [ ] Login succeeds
- [ ] Vault loads (even if empty)

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

## Test Suite 2: Core Functionality

### Test 2.1: Save Password

- [ ] Navigate to https://github.com/login
- [ ] Enter credentials (use test account)
- [ ] Click login
- [ ] Bitwarden prompts "Save login?"
- [ ] Click "Yes"
- [ ] Password saved successfully

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 2.2: Auto-Fill Password

- [ ] Log out of GitHub
- [ ] Return to login page
- [ ] Click username field
- [ ] Bitwarden icon appears in field
- [ ] Click Bitwarden icon
- [ ] Select saved login
- [ ] Credentials filled correctly

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 2.3: Password Generator

- [ ] Click extension icon
- [ ] Click "Generator" tab
- [ ] Verify default settings (12+ chars)
- [ ] Click "Regenerate" multiple times
- [ ] Each generates new password
- [ ] Click "Copy"
- [ ] Password copied to clipboard

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 2.4: Add Secure Note

- [ ] Click extension icon
- [ ] Click "+" (add item)
- [ ] Select "Secure Note"
- [ ] Enter name: "Test Note"
- [ ] Enter note: "This is a test"
- [ ] Click "Save"
- [ ] Note appears in vault

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 2.5: Search Vault

- [ ] Click extension icon
- [ ] Use search bar
- [ ] Search for saved item
- [ ] Item appears in results
- [ ] Click item to view
- [ ] Details displayed correctly

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

## Test Suite 3: Sync

### Test 3.1: Manual Sync

- [ ] Click extension icon
- [ ] Go to Settings
- [ ] Find "Sync" section
- [ ] Click "Sync vault now"
- [ ] Sync completes without error
- [ ] Timestamp updates

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 3.2: Cross-Browser Sync

- [ ] Install extension in Firefox
- [ ] Configure same server URL
- [ ] Login with same credentials
- [ ] Items from Chrome appear
- [ ] Add new item in Firefox
- [ ] Force sync in Firefox
- [ ] Return to Chrome
- [ ] Sync in Chrome
- [ ] New item appears

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

## Test Suite 4: Security Features

### Test 4.1: Vault Timeout

- [ ] Settings → Vault Timeout
- [ ] Set to "1 minute"
- [ ] Save settings
- [ ] Wait 1 minute
- [ ] Extension auto-locks
- [ ] Requires master password to unlock

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 4.2: Logout/Login

- [ ] Click extension icon
- [ ] Find "Log out" option
- [ ] Log out
- [ ] Extension cleared
- [ ] Log back in
- [ ] Vault reloads successfully
- [ ] All items present

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 4.3: Master Password Verification

- [ ] Log out
- [ ] Attempt login with wrong password
- [ ] Login fails with error message
- [ ] Login with correct password
- [ ] Login succeeds

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

## Test Suite 5: Advanced Features

### Test 5.1: Folders

- [ ] Click extension icon
- [ ] Create new folder: "Test Folder"
- [ ] Move item into folder
- [ ] Item appears in folder
- [ ] Filter by folder works

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 5.2: Favorites

- [ ] Select any vault item
- [ ] Click star icon (favorite)
- [ ] Item marked as favorite
- [ ] Favorites filter shows item
- [ ] Un-favorite works

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 5.3: Edit Item

- [ ] Click on saved login
- [ ] Click edit
- [ ] Change password
- [ ] Click "Save"
- [ ] Changes saved
- [ ] Auto-fill uses new password

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 5.4: Delete Item

- [ ] Select test item
- [ ] Click delete
- [ ] Confirm deletion
- [ ] Item removed from vault
- [ ] Sync confirms deletion

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

## Test Suite 6: Edge Cases

### Test 6.1: Network Interruption

- [ ] Login to extension
- [ ] Disconnect internet
- [ ] View saved passwords (should work)
- [ ] Try to add new item (should fail gracefully)
- [ ] Reconnect internet
- [ ] Force sync
- [ ] Normal operation resumes

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 6.2: Invalid Server URL

- [ ] Log out
- [ ] Settings → Change server URL to invalid: `https://invalid.example.com`
- [ ] Try to login
- [ ] Error message displayed
- [ ] Change back to correct URL
- [ ] Login works

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 6.3: Long Passwords

- [ ] Generate 128-character password
- [ ] Save to vault
- [ ] Auto-fill works correctly
- [ ] Password displays properly

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

## Test Suite 7: Browser Compatibility

### Test 7.1: Firefox

- [ ] Install in Firefox
- [ ] Configure server URL
- [ ] Login works
- [ ] Auto-fill works
- [ ] Sync works
- [ ] All core features functional

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 7.2: Edge

- [ ] Install in Edge
- [ ] Configure server URL
- [ ] Login works
- [ ] Auto-fill works
- [ ] Sync works
- [ ] All core features functional

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 7.3: Safari (if applicable)

- [ ] Install from Mac App Store
- [ ] Enable in Safari preferences
- [ ] Configure server URL
- [ ] Login works
- [ ] Auto-fill works
- [ ] Sync works
- [ ] All core features functional

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

## Test Suite 8: Performance

### Test 8.1: Extension Load Time

- [ ] Close browser completely
- [ ] Reopen browser
- [ ] Click extension icon
- [ ] Time to display: ______ seconds
- [ ] Acceptable if < 3 seconds

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

### Test 8.2: Search Performance (100+ items)

Prerequisites: Vault with 100+ items

- [ ] Click extension icon
- [ ] Type search query
- [ ] Results appear within 1 second
- [ ] Results accurate

**Result:** ✅ Pass / ❌ Fail / ⚠️ N/A (< 100 items)  
**Notes:** _____________________________

---

### Test 8.3: Sync Speed

- [ ] Note current item count: ______
- [ ] Force sync
- [ ] Measure sync time: ______ seconds
- [ ] Acceptable: < 5 seconds for < 100 items

**Result:** ✅ Pass / ❌ Fail  
**Notes:** _____________________________

---

## Results Summary

### Pass/Fail Count

- **Total Tests:** 30
- **Passed:** ______
- **Failed:** ______
- **N/A:** ______
- **Pass Rate:** ______%

### Critical Issues (must be ✅)

- [ ] Installation works
- [ ] Server URL configuration works
- [ ] Login works
- [ ] Save password works
- [ ] Auto-fill works
- [ ] Sync works

**All critical tests passed?** ✅ Yes / ❌ No

---

### Failed Tests

List any failed tests and details:

1. **Test:** _____________________________  
   **Issue:** _____________________________  
   **Severity:** ⚠️ Low / 🔶 Medium / 🔴 High  
   **Action:** _____________________________

2. **Test:** _____________________________  
   **Issue:** _____________________________  
   **Severity:** ⚠️ Low / 🔶 Medium / 🔴 High  
   **Action:** _____________________________

3. **Test:** _____________________________  
   **Issue:** _____________________________  
   **Severity:** ⚠️ Low / 🔶 Medium / 🔴 High  
   **Action:** _____________________________

---

## Sign-Off

### Tester

**Name:** _____________________________  
**Date:** _____________________________  
**Signature:** _____________________________

### Approver

**Name:** _____________________________  
**Date:** _____________________________  
**Signature:** _____________________________

---

## Recommendations

Based on test results:

- [ ] ✅ **READY FOR PRODUCTION** - All critical tests passed
- [ ] ⚠️ **READY WITH NOTES** - Minor issues, document workarounds
- [ ] 🔶 **NOT READY** - Medium severity issues, fix before rollout
- [ ] 🔴 **BLOCKED** - Critical issues, must resolve

**Notes:** _____________________________

---

## Next Steps

After successful testing:

1. [ ] Document any issues in FAQ
2. [ ] Update user guides with findings
3. [ ] Communicate rollout to users
4. [ ] Schedule training sessions (if needed)
5. [ ] Monitor support tickets after rollout

---

## Appendix: Test Environment

**Server Details:**
- URL: _____________________________
- Cloud Provider: ☐ AWS ☐ GCP ☐ Azure
- Version: _____________________________
- Deployment Date: _____________________________

**Browser Versions Tested:**
- Chrome: _____________________________
- Firefox: _____________________________
- Edge: _____________________________
- Safari: _____________________________

**Extension Versions:**
- Bitwarden Extension: _____________________________

**Network:**
- Connection Type: _____________________________
- Firewall: ☐ Yes ☐ No
- Proxy: ☐ Yes ☐ No

---

**Testing completed on:** _____________________________  
**Report saved to:** _____________________________  
**Follow-up date:** _____________________________

