from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "TradingView Notification System is running!"

@app.route('/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'Test endpoint working!',
        'environment': 'Railway'
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    return jsonify({'status': 'webhook received'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)