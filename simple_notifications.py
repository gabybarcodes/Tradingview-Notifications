"""
Simple TradingView Buy/Sell Notification System
Receives signals from TradingView and sends notifications
"""

from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

# Configuration - CHANGE THESE
WEBHOOK_SECRET = "gaby_trading_secret_2025"  # Change this to your secret
EMAIL_USER = "gabytrad3r@gmail.com"  # Your email (e.g., "your_email@gmail.com")
EMAIL_PASSWORD = "hmvk pacd qhui dbme"  # Your email app password
SEND_TO_EMAIL = "gabytrad3r@gmail.com"  # Where to send notifications

def send_email(subject, message):
    """Send email notification"""
    if not EMAIL_USER or not EMAIL_PASSWORD or not SEND_TO_EMAIL:
        print(f"📧 {subject}: {message}")
        return
    
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = SEND_TO_EMAIL
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, SEND_TO_EMAIL, msg.as_string())
        
        logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Email failed: {e}")

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
        
        # Extract message - could be JSON or plain text
        if 'message' in data:
            # Plain text message from TradingView
            message_content = data['message']
            subject = f"🚨 TradingView Alert"
        else:
            # JSON message with structured data
            symbol = data.get('symbol', data.get('ticker', 'UNKNOWN'))
            signal = data.get('signal', data.get('action', 'SIGNAL'))
            price = data.get('price', data.get('close', 'N/A'))
            
            subject = f"🚨 {signal} {symbol}"
            message_content = f"""
Trading Signal Alert!

Symbol: {symbol}
Signal: {signal}
Price: {price}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Raw data: {data}
"""
        
        # Send notification
        send_email(subject, message_content)
        
        # Also show on console
        print(f"\n🚨 ALERT: {subject}")
        print(f"Message: {message_content}")
        
        logging.info(f"Alert processed: {subject}")
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Test the notification system"""
    # Simulate a TradingView alert message
    subject = f"🧪 TEST: TradingView Alert"
    message = f"""This is a test from your TradingView notification system!

Your alerts will appear like this when TradingView sends them.

System Status: ✅ WORKING
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    send_email(subject, message)
    
    return jsonify({'message': 'Test notification sent!'})

@app.route('/status', methods=['GET'])
def status():
    """Get system status"""
    return jsonify({
        'status': 'running',
        'email_configured': bool(EMAIL_USER and EMAIL_PASSWORD and SEND_TO_EMAIL),
        'email_user': EMAIL_USER,
        'webhook_url': 'http://localhost/webhook',
        'test_url': 'http://localhost/test'
    })

if __name__ == '__main__':
    print("=== TradingView Notification System ===")
    print("1. Update EMAIL_USER, EMAIL_PASSWORD, SEND_TO_EMAIL")
    print("2. Change WEBHOOK_SECRET to something secure")
    print("3. Use webhook URL: http://localhost:5001/webhook")
    print("4. Test URL: http://localhost:5001/test")
    print("==========================================")
    
    # Use Railway's PORT environment variable or default to 5001
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)