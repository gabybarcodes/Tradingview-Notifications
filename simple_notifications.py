"""
Simple TradingView Buy/Sell Notification System
Receives signals from TradingView and sends notifications
"""

from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
import logging
import os
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

# Configuration - Uses environment variables from Railway
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', "gaby_trading_secret_2025")
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', "")
EMAIL_USER = os.environ.get('EMAIL_USER', "gabytrad3r@gmail.com")
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', "")
SEND_TO_EMAIL = os.environ.get('SEND_TO_EMAIL', "gabytrad3r@gmail.com")

def send_email(subject, message):
    """Send email notification with timeout protection"""
    print(f"📧 EMAIL NOTIFICATION:")
    print(f"   From: {EMAIL_USER}")
    print(f"   To: {SEND_TO_EMAIL}")
    print(f"   Subject: {subject}")
    
    if not EMAIL_PASSWORD:
        print(f"📧 Email not configured - missing password")
        logging.info(f"EMAIL NOT CONFIGURED: {subject} - {message}")
        return False
    
    try:
        # Set socket timeout for Gmail connection
        socket.setdefaulttimeout(10)
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = SEND_TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to Gmail SMTP with timeout
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
            
        logging.info(f"✅ Email sent successfully: {subject}")
        print(f"✅ Email sent successfully!")
        return True
        
    except socket.timeout:
        error_msg = f"⏰ Email timeout - Gmail connection too slow"
        print(error_msg)
        logging.warning(error_msg)
        return False
        
    except Exception as e:
        error_msg = f"❌ Email failed: {str(e)}"
        print(error_msg)
        logging.warning(error_msg)
        return False
    
    finally:
        # Reset socket timeout
        socket.setdefaulttimeout(None)

def send_discord_notification(subject, message):
    """Send notification to Discord webhook"""
    print(f"🎮 DISCORD NOTIFICATION:")
    print(f"   Subject: {subject}")
    print(f"   Message: {message}")
    
    if not DISCORD_WEBHOOK_URL:
        print(f"🎮 Discord not configured - logging instead")
        logging.info(f"NOTIFICATION: {subject} - {message}")
        return
    
    try:
        # Create Discord embed (fancy message)
        embed = {
            "title": f"🚨 {subject}",
            "description": message,
            "color": 0x00ff00 if "BUY" in message else 0xff0000 if "SELL" in message else 0x0099ff,
            "timestamp": datetime.now().isoformat(),
            "footer": {"text": "TradingView Alert System"}
        }
        
        payload = {
            "content": f"**{subject}**",
            "embeds": [embed]
        }
        
        # Send to Discord with short timeout
        response = requests.post(
            DISCORD_WEBHOOK_URL, 
            json=payload, 
            timeout=5
        )
        
        if response.status_code == 204:
            logging.info(f"✅ Discord notification sent: {subject}")
            print(f"✅ Discord notification sent successfully!")
        else:
            logging.warning(f"⚠️ Discord response: {response.status_code}")
            
    except requests.RequestException as e:
        error_msg = f"❌ Discord notification failed: {str(e)}"
        print(error_msg)
        logging.warning(error_msg)
        logging.info(f"BACKUP NOTIFICATION: {subject} - {message}")
        
    except Exception as e:
        error_msg = f"❌ Unexpected error: {str(e)}"
        print(error_msg)
        logging.warning(error_msg)
        logging.info(f"BACKUP NOTIFICATION: {subject} - {message}")

@app.route('/', methods=['GET'])
def home():
    """Home page"""
    return jsonify({
        'status': 'running',
        'service': 'TradingView Notification System v2.0',
        'endpoints': {
            'test': '/test',
            'webhook': '/webhook (POST)',
            'status': '/status'
        }
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive TradingView signals"""
    try:
        # Get raw data
        if request.content_type == 'application/json':
            data = request.get_json()
        else:
            # Handle plain text messages from TradingView
            raw_message = request.data.decode('utf-8')
            data = {'message': raw_message}
        
        # Check webhook secret for security
        webhook_key = data.get('key')
        if webhook_key != WEBHOOK_SECRET:
            logging.warning(f"Invalid webhook key: {webhook_key}")
            return jsonify({'error': 'Invalid key'}), 401
        
        # Extract message - handle the new clean format
        if 'message' in data:
            # New clean format: "Symbol: AAPL Action: BUY Price: 150.00"
            message_content = data['message']
            subject = f"🚨 TradingView Alert"
        else:
            # Fallback: JSON message with structured data
            symbol = data.get('symbol', data.get('ticker', 'UNKNOWN'))
            signal = data.get('signal', data.get('action', 'SIGNAL'))
            price = data.get('price', data.get('close', 'N/A'))
            
            subject = f"🚨 {signal} {symbol}"
            message_content = f"Symbol: {symbol} Action: {signal} Price: {price}"
        
        # Send notification
        send_discord_notification(subject, message_content)
        
        # Also show on console
        print(f"\n🚨 ALERT: {subject}")
        print(f"Message: {message_content}")
        
        logging.info(f"Alert processed: {subject}")
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test-email', methods=['GET'])
def test_email():
    """Test ONLY the email system"""
    subject = "🧪 EMAIL TEST: TradingView Alert System"
    message = f"""EMAIL TEST SUCCESSFUL!

This is a direct test of your email notification system.

🚨 TRADING SIGNAL TEST 🚨

Symbol: TEST
Action: BUY  
Price: $123.45
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If you received this email, your notification system is working perfectly!

System Status: ✅ EMAIL WORKING
"""
    
    # Test email only
    email_success = send_email(subject, message)
    
    return jsonify({
        'message': 'Email test completed!',
        'email_sent': email_success,
        'email_configured': bool(EMAIL_USER and EMAIL_PASSWORD and SEND_TO_EMAIL),
        'email_user': EMAIL_USER,
        'send_to': SEND_TO_EMAIL,
        'password_configured': bool(EMAIL_PASSWORD),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test', methods=['GET'])
def test():
    """Test the notification system"""
    # Simulate a TradingView alert message
    subject = f"🧪 TEST: TradingView Alert"
    message = f"""This is a test from your TradingView notification system!

🚨 TRADING SIGNAL TEST 🚨

Symbol: TEST
Action: BUY  
Price: $123.45
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Your alerts will appear like this when TradingView sends them.

System Status: ✅ WORKING
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Try to send email and capture any errors
    try:
        send_email(subject, message)
        email_status = "✅ Email function called successfully"
    except Exception as e:
        email_status = f"❌ Email function failed: {str(e)}"
    
    return jsonify({
        'message': 'Test notification sent!',
        'email_status': email_status,
        'email_configured': bool(EMAIL_USER and EMAIL_PASSWORD and SEND_TO_EMAIL),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/status', methods=['GET'])
def status():
    """Get system status"""
    return jsonify({
        'status': 'running',
        'discord_configured': bool(DISCORD_WEBHOOK_URL),
        'email_user': EMAIL_USER,
        'webhook_url': 'http://localhost/webhook',
        'test_url': 'http://localhost/test'
    })

if __name__ == '__main__':
    print("=== TradingView Notification System v2.0 ===")
    print("1. Update EMAIL_USER, EMAIL_PASSWORD, SEND_TO_EMAIL")
    print("2. Change WEBHOOK_SECRET to something secure")
    print("3. Use webhook URL: http://localhost:5001/webhook")
    print("4. Test URL: http://localhost:5001/test")
    print("5. Railway deployment active!")
    print("==========================================")
    
    # Use Railway's PORT environment variable or default to 5001
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)