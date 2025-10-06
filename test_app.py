from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'success',
        'message': 'TradingView Notification System is running!',
        'environment': 'Railway',
        'endpoints': {
            'test': '/test',
            'webhook': '/webhook'
        }
    })

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'success',
        'message': 'Test endpoint working!',
        'environment': 'Railway'
    })

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return jsonify({'status': 'webhook endpoint ready', 'method': 'use POST'})
    return jsonify({'status': 'webhook received', 'data': request.get_json()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)