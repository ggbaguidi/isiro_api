import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MODEL_PATH = os.getenv('MODEL_PATH', 'model.pkl')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    RECIPIENT_PHONE_NUMBER = os.getenv('RECIPIENT_PHONE_NUMBER')
    FLOOD_DATASET_PATH = os.getenv('FLOOD_DATASET_PATH')
    ALERT_THRESHOLD = os.getenv('ALERT_THRESHOLD', "0.5")
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    PHONE_NUMBER = os.getenv('PHONE_NUMBER')
    CARRIER_GATEWAY = os.getenv('CARRIER_GATEWAY')
    ARDUINO_DATA_PATH = os.getenv('ARDUINO_DATA_PATH')
