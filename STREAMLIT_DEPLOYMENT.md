# 🚀 Streamlit Cloud Deployment Guide

## Prerequisites

- GitHub account
- Streamlit Cloud account (free at https://share.streamlit.io)
- At least one AI API key (Groq, Gemini, or OpenAI)

---

## Step 1: Push Code to GitHub

### Option A: Using VS Code (Recommended)

1. Open Source Control panel (Ctrl+Shift+G)
2. Stage all changes (click + next to Changes)
3. Enter commit message: "Initial commit - LillyHelper AI app"
4. Click ✓ Commit
5. Click "Sync Changes" or "Push"

### Option B: Using Git Command Line

```bash
# Navigate to project directory
cd "c:\Users\L108094\OneDrive - Eli Lilly and Company\Nexus\6 month challenge"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - LillyHelper AI app"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/jacktilfordcarey/6-month-challenge.git

# Push to GitHub
git push -u origin master
```

### Option C: Using GitHub Desktop

1. Open GitHub Desktop
2. Add existing repository
3. Select your project folder
4. Commit changes
5. Publish repository to GitHub

---

## Step 2: Deploy to Streamlit Cloud

### 2.1 Go to Streamlit Cloud

Visit: https://share.streamlit.io

### 2.2 Sign In

- Click "Sign in" (top right)
- Sign in with GitHub account

### 2.3 Create New App

1. Click "New app" button
2. Fill in details:
   - **Repository**: `jacktilfordcarey/6-month-challenge`
   - **Branch**: `master`
   - **Main file path**: `lillyextractor.py`
   - **App URL**: Choose custom URL (e.g., `lillyhelper-ai`)

### 2.4 Configure Secrets (IMPORTANT!)

Before deploying, click "Advanced settings" → "Secrets"

Paste your API keys in TOML format:

```toml
# Add at least ONE of these:

GROQ_API_KEY = "gsk_your_actual_groq_key_here"
GEMINI_API_KEY = "AIza_your_actual_gemini_key_here"
OPENAI_API_KEY = "sk-proj_your_actual_openai_key_here"
```

**⚠️ Important**:

- Don't include quotes around the keys in TOML format
- Get fresh API keys with available quotas
- Groq is recommended (fastest and free tier)

### 2.5 Deploy!

Click "Deploy!" button

---

## Step 3: Wait for Deployment

The app will:

1. Install dependencies from `requirements.txt` (2-3 minutes)
2. Start the Streamlit server
3. Show your app URL when ready

**Your app will be live at**: `https://lillyhelper-ai.streamlit.app`

---

## Step 4: Test Your Deployment

1. Open your Streamlit Cloud URL
2. Upload a CSV file or enter text
3. Select user profile (Knowledge Level, Country, HCP Type)
4. Click "Ask AI to Analyze"
5. Test accessibility features (Contrast, Magnify, TTS)
6. Try the chatbot in the sidebar

---

## Troubleshooting

### Build Fails

- Check `requirements.txt` is in repository root
- Verify Python version compatibility
- Check logs in Streamlit Cloud dashboard

### API Errors

- Verify API keys are correctly formatted in Secrets
- Ensure keys have available quota
- Check for typos in key names

### App Runs But No AI Response

- Check Secrets are saved correctly
- Verify at least one API key is valid
- Look at app logs for error messages

### CSS Not Applying

- Hard refresh browser: Ctrl+F5
- Clear Streamlit cache: Click "⋮" menu → "Clear cache"

---

## Updating Your Deployed App

### Automatic Updates

Every git push to GitHub automatically redeploys:

```bash
git add .
git commit -m "Update description"
git push
```

### Manual Reboot

In Streamlit Cloud dashboard:

1. Click your app
2. Click "⋮" menu (top right)
3. Select "Reboot app"

---

## Managing Secrets After Deployment

1. Go to https://share.streamlit.io
2. Click your app
3. Click "⚮" Settings
4. Select "Secrets" tab
5. Edit and save

**Note**: App automatically reboots when secrets change

---

## Custom Domain (Optional)

Streamlit Cloud provides free subdomain: `your-app.streamlit.app`

For custom domain (e.g., `lillyhelper.com`):

1. Upgrade to Streamlit Cloud Teams/Enterprise
2. Configure CNAME in your DNS settings

---

## Monitoring & Analytics

### View Logs

- Click app in dashboard
- Click "⋮" menu → "Logs"
- Monitor errors and usage

### App Status

- Dashboard shows: Running, Sleeping, or Error
- Apps sleep after inactivity (free tier)
- Wake automatically when accessed

---

## Getting Fresh API Keys

### Groq (Recommended)

1. Visit: https://console.groq.com
2. Sign up for free account
3. Go to "API Keys" section
4. Create new key
5. Copy and add to Streamlit Secrets

### Google Gemini

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Create API key
4. Copy and add to Streamlit Secrets

### OpenAI

1. Visit: https://platform.openai.com/api-keys
2. Sign in
3. Create new secret key
4. Add payment method (required after free trial)
5. Copy and add to Streamlit Secrets

---

## Security Best Practices

✅ **DO:**

- Use Streamlit Secrets for API keys
- Keep `.env` in `.gitignore`
- Rotate API keys regularly
- Monitor API usage

❌ **DON'T:**

- Commit API keys to GitHub
- Share your secrets.toml file
- Use same keys for dev and production
- Expose keys in client-side code

---

## Cost Considerations

### Free Tier Limits

- **Streamlit Cloud**: 1 private app (unlimited public)
- **Groq**: Generous free tier
- **Gemini**: Rate limits on free tier
- **OpenAI**: Requires payment after trial

### Recommendations

- Start with Groq (free, fast)
- Monitor API usage in provider dashboards
- Set up billing alerts
- Consider caching for repeated queries

---

## Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Community Forum**: https://discuss.streamlit.io
- **Status Page**: https://streamlit.statuspage.io
- **Groq Docs**: https://console.groq.com/docs
- **Gemini Docs**: https://ai.google.dev/docs

---

## Quick Reference

```bash
# Check git status
git status

# Add changes
git add .

# Commit
git commit -m "Your message"

# Push to GitHub (triggers auto-deploy)
git push

# View remote URL
git remote -v
```

**Streamlit Cloud Dashboard**: https://share.streamlit.io/

**Your GitHub Repo**: https://github.com/jacktilfordcarey/6-month-challenge

---

## Next Steps After Deployment

1. ✅ Test all features on live app
2. ✅ Share URL with stakeholders
3. ✅ Set up monitoring/alerts
4. ✅ Gather user feedback
5. ✅ Plan feature enhancements
6. ✅ Document any issues

---

**Need Help?** Check the troubleshooting section or Streamlit Community Forum!
