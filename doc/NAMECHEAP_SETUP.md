# Namecheap API Setup Guide

## ❌ Error: "API Key is invalid or API access has not been enabled"

If you're seeing this error, follow these steps:

## 🔧 Step-by-Step Setup

### 1. Enable API Access in Namecheap

1. **Log in** to your Namecheap account: https://www.namecheap.com/myaccount/login/
2. Navigate to: **Profile → Tools → Business & Dev Tools → API Access**
   - Direct link: https://ap.www.namecheap.com/settings/tools/apiaccess
3. Click **"Enable API Access"**
4. **Important**: You need at least **$50 account balance** to enable API access

### 2. Get Your API Key

After enabling API access:

1. Your **API Key** will be displayed on the API Access page
2. Copy the full API key (it's a long string like: `d01aec89241e4b609041f2376f0798a9`)

### 3. Whitelist Your IP Address

1. On the same API Access page, find the **"Manage IP Addresses"** section
2. Click **"Add a New IP Address"**
3. Enter your public IP: **101.2.185.165**
   - Find your IP at: https://whatismyipaddress.com/
4. Click **"Save"**
5. **Wait 5-10 minutes** for the IP whitelist to take effect

### 4. Update Your .env File

Edit your `.env` file with the correct information:

```env
NAMECHEAP_API_KEY=d01aec89241e4b609041f2376f0798a9
NAMECHEAP_API_USER=liupetech
NAMECHEAP_USERNAME=liupetech
NAMECHEAP_CLIENT_IP=101.2.185.165
```

**Important Notes:**
- `NAMECHEAP_API_USER` and `NAMECHEAP_USERNAME` should be the same (your Namecheap username)
- The API key should be exactly as shown in your Namecheap dashboard
- The IP must match exactly what's whitelisted

### 5. Test Your Setup

Run the test script:

```bash
python test_api.py
```

You should see:
```
✅ SUCCESS! API credentials are working correctly!
```

## 🚨 Common Issues

### Issue 1: "API Key is invalid"
- **Cause**: API access not enabled or wrong API key
- **Solution**: 
  1. Ensure API access is enabled in Namecheap
  2. Verify you have $50+ account balance
  3. Double-check API key is copied correctly (no extra spaces)

### Issue 2: "IP not whitelisted"
- **Cause**: Your IP hasn't been added or changes haven't propagated
- **Solution**: 
  1. Add IP in Namecheap API settings
  2. Wait 5-10 minutes
  3. Verify your current IP hasn't changed: https://whatismyipaddress.com/

### Issue 3: "Insufficient balance"
- **Cause**: Account balance is below $50
- **Solution**: Add funds to your Namecheap account

### Issue 4: Using Sandbox instead of Production
- **Cause**: Wrong API endpoint
- **Solution**: The code uses production endpoint by default:
  ```python
  api_url = "https://api.namecheap.com/xml.response"
  ```
  (NOT sandbox: `https://api.sandbox.namecheap.com/xml.response`)

## 📞 Still Having Issues?

1. **Check Namecheap API Documentation**: https://www.namecheap.com/support/api/intro/
2. **Contact Namecheap Support**: They can verify if API is properly enabled
3. **Check Namecheap Status Page**: Ensure API services are operational

## ✅ Verification Checklist

Before running the domain checker, ensure:

- [ ] API access is enabled in Namecheap account
- [ ] Account balance is $50 or more
- [ ] API key is correct in .env file
- [ ] Username is correct (exactly as shown in Namecheap)
- [ ] Public IP (101.2.185.165) is whitelisted
- [ ] Waited 5-10 minutes after whitelisting IP
- [ ] Test script (`python test_api.py`) passes successfully

## 🎯 Next Steps

Once `test_api.py` shows success:

```bash
# Run the domain checker
python main.py
```

Your domains will be checked with **Namecheap API verification** for maximum accuracy!

---

## 💡 Alternative: Run Without API

If you can't enable API access right now, the tool still works using WHOIS + DNS verification:

The program will automatically detect if API credentials are missing and fall back to:
- WHOIS lookup
- DNS verification

This provides good accuracy, though not as precise as API verification.

---

**Need help?** Open an issue: https://github.com/sithulaka/DomainChecker/issues
