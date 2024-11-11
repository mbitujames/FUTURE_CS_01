from flask import Flask, render_template, request, redirect, session, url_for
import pyotp

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Generate a base32 secret key
user_otp_secret = pyotp.random_base32()

@app.route('/')
def index():
    return 'Welcome to the 2FA Demo'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['authenticated'] = False
        # This would be where you verify username and password
        return redirect(url_for('verify_2fa'))
    return render_template('login.html')

@app.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    totp = pyotp.TOTP(user_otp_secret)
    if request.method == 'POST':
        otp_input = request.form.get('otp')
        if totp.verify(otp_input):
            session['authenticated'] = True
            return 'You are authenticated!'
        else:
            return 'Invalid OTP. Please try again.'

    # Generate QR code for easy scanning with apps like Google Authenticator
    qr_uri = totp.provisioning_uri("username", issuer_name="YourApp")
    return render_template('verify_2fa.html', qr_uri=qr_uri)

if __name__ == '__main__':
    app.run(debug=True)
