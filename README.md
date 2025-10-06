# TradingView Discord Notification System 🎮

Get instant Discord notifications when your TradingView strategies trigger Buy/Sell signals!

## ✨ What This Does
- Receives webhook signals from TradingView Pine Script strategies
- Sends instant Discord notifications with beautiful embeds
- Runs 24/7 in the cloud on Railway (no need to keep your computer on)
- Works with any Pine Script strategy that has alert conditions
- No email headaches - Discord is instant and reliable!

## 🚀 Quick Start (5-10 minutes)

### Step 1: Create Discord Webhook
1. **Create or use existing Discord server**
2. **Right-click on a text channel** (like #general)
3. **Edit Channel → Integrations → Webhooks**
4. **"New Webhook"**
5. **Name:** "TradingView Notifications"
6. **Copy the webhook URL** (save for later!)

### Step 2: Deploy to Railway (Free!)
1. **Sign up** at [Railway.app](https://railway.app) with GitHub
2. **This repository is already set up!** Just deploy it:
   - **Fork this repository** on GitHub
   - In Railway: **"Start New Project"** → **"Deploy from GitHub repo"**
   - **Select your forked repository** → Railway will auto-deploy!

### Step 3: Configure Environment Variables
In Railway dashboard → **Variables tab** → Add these:

```
WEBHOOK_SECRET = gaby_trading_secret_2025
DISCORD_WEBHOOK_URL = [your Discord webhook URL from Step 1]
```

### Step 4: Get Your Webhook URL
After deployment, your webhook URL will be:
```
https://web-production-cbdc9.up.railway.app/webhook
```

### Step 5: Test Your System
Visit this URL to test:
```
https://web-production-cbdc9.up.railway.app/test
```
You should see a test notification in Discord! 🎉
Add these lines to your Pine Script strategy:

### Step 6: Add Alerts to Your Pine Script Strategy
Add these lines to your Pine Script strategy:

```pinescript
// For Pine Script v5 - Add webhook alerts for LONG signals
alertcondition(long_condition, "LONG Signal", 
    "Symbol: {{ticker}} Action: BUY Price: {{close}}")

// Add webhook alerts for SHORT signals  
alertcondition(short_condition, "SHORT Signal",
    "Symbol: {{ticker}} Action: SELL Price: {{close}}")
```

**Replace:**
- `long_condition` with your buy condition
- `short_condition` with your sell condition

### Step 7: Create TradingView Alerts
1. **Add your strategy** to a TradingView chart
2. **Right-click** → **Add Alert**
3. **Condition:** Select your strategy alert (LONG Signal or SHORT Signal)
4. **Webhook URL:** `https://web-production-cbdc9.up.railway.app/webhook`
5. **Message:** 
```json
{"key": "gaby_trading_secret_2025", "message": "{{strategy.order.alert_message}}"}
```
6. **Click "Create"**

## 🧪 Test Your Setup

1. **Test the server:** Visit `https://web-production-cbdc9.up.railway.app/test`
2. **Check Discord** - you should see a fancy test notification! 🎮
3. **Test with webhook manually:**

```bash
curl -X POST https://web-production-cbdc9.up.railway.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"key": "gaby_trading_secret_2025", "message": "Symbol: AAPL Action: BUY Price: 150.00"}'
```

## 📊 Example Pine Script Strategies Included

### 1. Combined Indicator Strategy (`combined_indicator_with_alerts.pine`)
- **RSI crossover signals** with EMA trend filter
- **Generates big "Long +2" arrows** 
- **ATR-based stops** and profit targets
- **Discord webhook alerts built-in**

### 2. Market Trend Strategy (`original_profitable_strategy.pine`)
- **Support/resistance levels** with conservative entries
- **Gradient RSI coloring**
- **Discord webhook alerts included**

## 🎨 Discord Notification Features
- 🟢 **Green embeds** for BUY signals
- 🔴 **Red embeds** for SELL signals
- 📊 **Professional formatting** with timestamps
- ⚡ **Instant delivery** - no email delays
- 🎮 **Beautiful Discord embeds** with icons

## 🛠️ Customization Options

### Change Email Template
Edit the `send_email()` function in `simple_notifications.py`:

```python
def send_email(subject, message):
    # Customize your email format here
    msg = MIMEText(f"🚨 TRADING ALERT 🚨\n\n{message}")

### Custom Message Format
Modify the Discord embed in `simple_notifications.py`:

```python
embed = {
    "title": f"🚨 {subject}",
    "description": message,
    "color": 0x00ff00,  # Green color
    "fields": [
        {"name": "Symbol", "value": "AAPL", "inline": True},
        {"name": "Price", "value": "$150.25", "inline": True}
    ]
}
```

### Multiple Discord Channels
Add multiple webhook URLs for different strategies:

```python
DISCORD_WEBHOOK_URL_CRYPTO = os.environ.get('DISCORD_WEBHOOK_URL_CRYPTO', "")
DISCORD_WEBHOOK_URL_STOCKS = os.environ.get('DISCORD_WEBHOOK_URL_STOCKS', "")
```

### Add Email Backup
Keep email as backup notification method by adding email variables to Railway.

## 🚨 Troubleshooting

### "Discord webhook not working"
- Verify your Discord webhook URL is correct
- Check that the webhook URL is added to Railway variables
- Test the webhook URL directly in Discord

### "Webhook not receiving signals"
- Verify your Railway URL: `https://web-production-cbdc9.up.railway.app/webhook`
- Check that your webhook secret matches: `gaby_trading_secret_2025`
- Ensure TradingView alert message format is correct

### "Railway app sleeping"
- Railway free tier gives 500 hours/month (~20 days)
- App automatically wakes up when webhook is called
- Upgrade to Railway Pro ($5/month) for unlimited hours

### "Pine Script compilation error"
- Use simple strings in alertcondition() messages
- Don't use dynamic string concatenation in Pine Script v5
- Test strategy on chart before creating alerts

## 🆓 Free Alternatives to Railway

1. **Render.com** - 750 free hours/month
2. **Fly.io** - Limited free tier  
3. **Vercel** - Serverless functions (requires modification)

## 📞 Support

If you run into issues:
1. **Check Railway logs** in your dashboard
2. **Test the `/test` endpoint** first: `https://web-production-cbdc9.up.railway.app/test`
3. **Verify Discord webhook** in Discord server settings
4. **Check webhook secret** matches everywhere

---

## 🚀 Advanced Features

### Multiple Strategies
Run multiple strategies by:
1. Using different Discord channels for each strategy
2. Adding strategy identification in the message
3. Creating separate webhook URLs for different assets

### Position Sizing Alerts
Add position size to your alerts:

```json
{"key": "gaby_trading_secret_2025", "message": "Symbol: {{ticker}} Action: BUY Price: {{close}} Size: 100 shares"}
```

### Stop Loss & Take Profit Alerts
Create separate alerts for exits:

```pinescript
alertcondition(stop_loss_condition, "STOP LOSS", 
    "Symbol: {{ticker}} Action: STOP LOSS Price: {{close}}")
alertcondition(take_profit_condition, "TAKE PROFIT", 
    "Symbol: {{ticker}} Action: TAKE PROFIT Price: {{close}}")

```pinescript
alertcondition(stop_loss_condition, "STOP LOSS", 
    '{"key": "your_secret", "symbol": "{{ticker}}", "action": "STOP", "price": "{{close}}"}')
```

---

**Happy Trading! 📈✨**

*Remember: This is for notification purposes only. Always do your own research and risk management!*