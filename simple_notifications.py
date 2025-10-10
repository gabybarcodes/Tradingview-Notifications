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

@app.before_request
def log_all_requests():
    """Log every single request to help debug TradingView calls"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n📨 REQUEST at {timestamp}")
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"Remote IP: {request.remote_addr}")
    print(f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    if request.data:
        print(f"Data: {request.data}")

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
    # Log every webhook call
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n🔔 WEBHOOK CALL at {timestamp}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Content-Type: {request.content_type}")
    print(f"Raw Data: {request.data}")
    
    try:
        if request.content_type == 'application/json':
            data = request.get_json()
        else:
            raw_message = request.data.decode('utf-8')
            data = {'message': raw_message}
        
        print(f"Parsed Data: {data}")
        
        provided_key = data.get('key', '')
        print(f"Key check: provided='{provided_key}' vs expected='{WEBHOOK_SECRET}'")
        
        if provided_key != WEBHOOK_SECRET:
            print("❌ INVALID KEY!")
            return jsonify({'error': 'Invalid key'}), 401
        
        alert_message = data.get('message', 'No message provided')
        print(f"Alert Message: {alert_message}")
        
        subject = "TradingView Alert"
        if 'BUY' in alert_message.upper():
            subject = "🟢 BUY Signal"
        elif 'SELL' in alert_message.upper():
            subject = "🔴 SELL Signal"
        
        formatted_message = f"""🚨 **TRADING ALERT** 🚨

{alert_message}

🕐 **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        print(f"Sending Discord notification: {subject}")
        success = send_discord_notification(subject, formatted_message)
        print(f"Discord notification result: {success}")
        
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

@app.route('/tradingview', methods=['POST'])
def tradingview_webhook():
    """Special endpoint that accepts ANY TradingView format"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n🚨 TRADINGVIEW WEBHOOK at {timestamp}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Content-Type: {request.content_type}")
    print(f"Raw Data: {request.data}")
    print(f"Form Data: {dict(request.form)}")
    print(f"Args: {dict(request.args)}")
    
    try:
        # Try multiple ways to get the data
        message = ""
        
        if request.content_type == 'application/json':
            data = request.get_json()
            print(f"JSON Data: {data}")
            message = data.get('message', str(data))
        elif request.form:
            print(f"Form Data: {dict(request.form)}")
            message = str(dict(request.form))
        else:
            message = request.data.decode('utf-8')
            print(f"Raw Message: {message}")
        
        # Send to Discord regardless of format
        subject = "🔔 TradingView Direct"
        formatted_message = f"""🚨 **TRADINGVIEW ALERT** 🚨

{message}

🕐 **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        success = send_discord_notification(subject, formatted_message)
        print(f"Discord sent: {success}")
        
        return jsonify({
            'status': 'received',
            'message': message,
            'discord_sent': success
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/simple', methods=['POST'])
def simple_webhook():
    """Ultra-simple webhook - accepts anything and sends to Discord"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n💚 SIMPLE WEBHOOK at {timestamp}")
    print(f"Data: {request.data}")
    
    try:
        # Get any data in any format
        if request.data:
            message = request.data.decode('utf-8')
        else:
            message = "Empty webhook call"
        
        # Send directly to Discord
        success = send_discord_notification("🟢 Simple Alert", message)
        
        return "OK"
        
    except Exception as e:
        print(f"❌ Simple webhook error: {e}")
        return "ERROR"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
