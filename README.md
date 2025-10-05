# TradingView Email Notification System 📧📈

Get instant email notifications when your TradingView strategies trigger Buy/Sell signals!

## What This Does
- Receives webhook signals from TradingView Pine Script strategies
- Sends instant email notifications to your Gmail
- Runs 24/7 in the cloud (no need to keep your computer on)
- Works with any Pine Script strategy that has alert conditions

## Quick Start (5-10 minutes)

### Step 1: Get the Code
1. Download this entire folder or clone from GitHub
2. You'll need these files:
   - `simple_notifications.py` (the main server)
   - `requirements.txt` (dependencies)
   - `Procfile` (deployment config)
   - `runtime.txt` (Python version)
   - `.gitignore` (git ignore rules)

### Step 2: Setup Gmail App Password
1. Go to your **Google Account settings** → **Security**
2. Turn on **2-Factor Authentication** (required for app passwords)
3. Go to **App passwords** → Generate password for "Mail"
4. **Save this password!** You'll need it later

### Step 3: Configure Your Settings
Edit `simple_notifications.py` and change these lines:

```python
# Configuration - CHANGE THESE
WEBHOOK_SECRET = "your_secret_key_2025"  # Change to your own secret
EMAIL_USER = "your_email@gmail.com"      # Your Gmail address
EMAIL_PASSWORD = "your_app_password"     # Gmail app password from Step 2
SEND_TO_EMAIL = "your_email@gmail.com"   # Where to send notifications
```

### Step 4: Deploy to Railway (Free!)
1. **Sign up** at [Railway.app](https://railway.app) with GitHub
2. **Create a GitHub repository** and upload your files
3. In Railway: **"Start New Project"** → **"Deploy from GitHub repo"**
4. **Select your repository** → Railway will auto-deploy!
5. **Copy your Railway URL** (looks like: `https://yourapp.railway.app`)

### Step 5: Add Alerts to Your Pine Script Strategy
Add these lines to your Pine Script strategy:

```pinescript
// Add webhook alerts for LONG signals
alertcondition(long_condition, "LONG Signal", 
    '{"key": "your_secret_key_2025", "symbol": "{{ticker}}", "action": "BUY", "price": "{{close}}", "rsi": "' + str.tostring(rsi_value) + '"}')

// Add webhook alerts for SHORT signals  
alertcondition(short_condition, "SHORT Signal",
    '{"key": "your_secret_key_2025", "symbol": "{{ticker}}", "action": "SELL", "price": "{{close}}", "rsi": "' + str.tostring(rsi_value) + '"}')
```

**Replace:**
- `your_secret_key_2025` with your webhook secret
- `long_condition` with your buy condition
- `short_condition` with your sell condition
- `rsi_value` with your RSI variable (or remove if not using RSI)

### Step 6: Create TradingView Alerts
1. **Add your strategy** to a TradingView chart
2. **Right-click** → **Add Alert**
3. **Condition:** Select your strategy alert
4. **Webhook URL:** `https://yourapp.railway.app/webhook`
5. **Message:** Leave as default (Pine Script will send JSON)
6. **Click "Create"**

## Test Your Setup

1. **Test the server:** Visit `https://yourapp.railway.app/test`
2. **Check your email** - you should get a test notification
3. **Test with webhook:** Use a tool like Postman or curl:

```bash
curl -X POST https://yourapp.railway.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"key": "your_secret_key_2025", "symbol": "AAPL", "action": "BUY", "price": "150.00"}'
```

## Example Pine Script Strategies Included

### 1. Combined Indicator Strategy (`combined_indicator_with_alerts.pine`)
- **RSI crossover signals** with EMA trend filter
- **Generates big "Long +2" arrows** 
- **ATR-based stops** and profit targets
- **Already has webhook alerts built-in**

### 2. Market Trend Strategy (`original_profitable_strategy.pine`)
- **Support/resistance levels** with conservative entries
- **Gradient RSI coloring**
- **Webhook alerts included**

## Customization Options

### Change Email Template
Edit the `send_email()` function in `simple_notifications.py`:

```python
def send_email(subject, message):
    # Customize your email format here
    msg = MIMEText(f"🚨 TRADING ALERT 🚨\n\n{message}")
```

### Add SMS Notifications
You can add Twilio SMS by installing `twilio` and adding:

```python
from twilio.rest import Client
# Add SMS function alongside email
```

### Multiple Email Recipients
Change `SEND_TO_EMAIL` to a list:

```python
SEND_TO_EMAIL = ["trader1@gmail.com", "trader2@gmail.com"]
```

## Troubleshooting

### "Email failed: Authentication failed"
- Double-check your Gmail app password
- Make sure 2FA is enabled on your Google account

### "Webhook not receiving signals"
- Verify your Railway URL is correct in TradingView alerts
- Check that your webhook secret matches in both Pine Script and Python

### "Railway app sleeping"
- Railway free tier gives 500 hours/month (~20 days)
- Upgrade to Railway Pro ($5/month) for unlimited hours

### "Pine Script compilation error"
- Make sure alert messages use only const strings
- Don't use dynamic string concatenation in alertcondition()

## Free Alternatives to Railway

1. **Render.com** - 750 free hours/month
2. **Fly.io** - Limited free tier
3. **Heroku** - No longer free (starts at $5/month)

## Support

If you run into issues:
1. Check Railway logs in your dashboard
2. Test the `/test` endpoint first
3. Verify Gmail app password is correct
4. Make sure webhook secret matches everywhere

---

## Advanced Features

### Multiple Strategies
You can run multiple strategies by:
1. Using different webhook secrets for each strategy
2. Adding strategy identification in the JSON message
3. Filtering emails by strategy name

### Position Sizing
Add position size to your alerts:

```pinescript
'{"key": "your_secret", "symbol": "{{ticker}}", "action": "BUY", "price": "{{close}}", "size": "100"}'
```

### Stop Loss Alerts
Create separate alerts for stop losses:

```pinescript
alertcondition(stop_loss_condition, "STOP LOSS", 
    '{"key": "your_secret", "symbol": "{{ticker}}", "action": "STOP", "price": "{{close}}"}')
```

---

**Happy Trading! 📈✨**

*Remember: This is for notification purposes only. Always do your own research and risk management!*