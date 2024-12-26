# app.py
from flask import Flask, request, jsonify
from twilio.rest import Client
from models import db, OTPVerification
import random
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# # Twilio setup

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/')
def hello():
    return jsonify({'message': 'Hello This code is working'}), 200

@app.route('/send-otp/', methods=['POST'])
def send_otp():
    try:
        data = json.loads(request.data)
        phone_number = data.get('phone_number')

        if not phone_number:
            return jsonify({'error': 'Phone number is required'}), 400

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Send OTP via Twilio
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        # Save OTP to the database
        otp_record = OTPVerification(phone_number=phone_number, otp=otp)
        db.session.add(otp_record)
        db.session.commit()

        return jsonify({'message': 'OTP sent successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/verify-otp/', methods=['POST'])
def verify_otp():
    try:
        data = json.loads(request.data)
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if not phone_number or not otp:
            return jsonify({'error': 'Phone number and OTP are required'}), 400

        # Retrieve OTP record from the database
        otp_record = OTPVerification.query.filter_by(phone_number=phone_number).order_by(OTPVerification.timestamp.desc()).first()

        if not otp_record:
            return jsonify({'error': 'Phone number not found'}), 404

        # Verify OTP
        if otp_record.otp == otp:
            return jsonify({'message': 'OTP verified successfully!'}), 200
        else:
            return jsonify({'error': 'Invalid OTP'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the database tables if they don't exist
    app.run(debug=True)
