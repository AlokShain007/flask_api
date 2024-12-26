# config.py
import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///otp_verification.db'  # You can change this to your database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
