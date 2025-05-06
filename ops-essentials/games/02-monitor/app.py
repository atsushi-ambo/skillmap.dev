from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Simple counter for requests
request_counter = 0

@app.route('/')
def home():
    global request_counter
    request_counter += 1
    return jsonify({
        'status': 'running',
        'request_count': request_counter,
        'timestamp': time.time()
    })

@app.route('/metrics')
def metrics():
    return f"""# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total {request_counter}
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
