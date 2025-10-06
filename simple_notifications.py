"""
TradingView Discord Notification System
"""

from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
app = Flask(__name__)

WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', "gaby_trading_secret_2025")
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', "")

def send_discord_notification(subject, message):
    """Send notification to Discord"""
    if not DISCORD_WEBHOOK_URL:
        print("❌ Discord webhook not configured!")
        return False
    
    try:
        embed = {
            "title": f"🚨 {subject}",
            "description": message,
            "color": 0x00ff00 if "BUY" in message.upper() else 0xff0000 if "SELL" in message.upper() else 0x0099ff,
            "timestamp": datetime.now().isoformat(),
            "footer": {"text": "TradingView Alert System"}
        }
        
        payload = {
            "content": f"**{subject}**",
            "embeds": [embed]
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        
        if response.status_code == 204:
            print("✅ Discord notification sent!")
            return True
        else:
            print(f"⚠️ Discord response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Discord error: {e}")
        return False

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'running',
        'service': 'TradingView Discord Notification System',
        'discord_configured': bool(DISCORD_WEBHOOK_URL),
        'webhook_url': 'https://web-production-cbdc9.up.railway.app/webhook'
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.content_type == 'application/json':
            data = request.get_json()
        else:
            raw_message = request.data.decode('utf-8')
            data = {'message': raw_message}
        
        provided_key = data.get('key', '')
        if provided_key != WEBHOOK_SECRET:
            return jsonify({'error': 'Invalid key'}), 401
        
        alert_message = data.get('message', 'No message provided')
        
        subject = "TradingView Alert"
        if 'BUY' in alert_message.upper():
            subject = "🟢 BUY Signal"
        elif 'SELL' in alert_message.upper():
            subject = "🔴 SELL Signal"
        
        formatted_message = f"""🚨 **TRADING ALERT** 🚨

{alert_message}

🕐 **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        success = send_discord_notification(subject, formatted_message)
        
        return jsonify({
            'status': 'success', 
            'notification_sent': success,
            'message': alert_message
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    subject = "🧪 DISCORD TEST"
    message = f"""🚨 **TEST NOTIFICATION** 🚨

Symbol: AAPL
Action: BUY  
Price: $150.25

🕐 **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ Discord system working!
"""
    
    success = send_discord_notification(subject, message)
    
    return jsonify({
        'message': 'Discord test sent!',
        'notification_sent': success,
        'discord_configured': bool(DISCORD_WEBHOOK_URL)
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'running',
        'discord_configured': bool(DISCORD_WEBHOOK_URL),
        'webhook_secret_configured': bool(WEBHOOK_SECRET)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
