import re
from email.message import EmailMessage

import aiosmtplib
from infrastructure.config import Config
from core.ports.notification_port import NotificationPort

CARRIER_MAP = {
    "verizon": "vtext.com",
    "tmobile": "tmomail.net",
    "sprint": "messaging.sprintpcs.com",
    "at&t": "txt.att.net",
    "boost": "smsmyboostmobile.com",
    "cricket": "sms.cricketwireless.net",
    "uscellular": "email.uscc.net",
    "googlefi": "msg.fi.google.com",
    "ting": "message.ting.com",
    "tracfone": "mmst5.tracfone.com",
    "metropcs": "mymetropcs.com",
    "mintmobile": "mailmymobile.net",
    "republicwireless": "text.republicwireless.com",
}


class EmailSmsAdapter(NotificationPort):
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.email = Config.EMAIL_ADDRESS
        self.password = Config.EMAIL_PASSWORD
        self.phone_number = Config.PHONE_NUMBER
        self.carrier = Config.CARRIER_GATEWAY.lower()

        self._validate_config()

    def _validate_config(self):
        """Validate configuration on initialization"""
        if self.carrier not in CARRIER_MAP:
            raise ValueError(
                f"Unsupported carrier: {
                    self.carrier}. Valid options: {
                    list(
                        CARRIER_MAP.keys())}")
        if not re.match(r"^\+?[1-9]\d{1,14}$", str(self.phone_number)):
            raise ValueError("Invalid phone number format")

    async def send_alert(self, message: str) -> bool:
        """Asynchronously send SMS alert using email-to-SMS gateway"""
        try:
            response = await self._send_sms(
                number=self.phone_number,
                carrier=self.carrier,
                message=message,
                subject="Alerte Inondation"
            )
            return self._is_success(response)
        except Exception as e:
            print(f"SMS sending error: {str(e)}")
            return False

    async def _send_sms(self, number: str, carrier: str, message: str, subject: str) -> dict:
        """Core async SMS sending logic"""
        to_email = f"{number}@{CARRIER_MAP[carrier]}"

        email_msg = EmailMessage()
        email_msg["From"] = self.email
        email_msg["To"] = to_email
        email_msg["Subject"] = subject
        email_msg.set_content(message)

        return await aiosmtplib.send(
            email_msg,
            hostname=self.smtp_server,
            port=self.smtp_port,
            username=self.email,
            password=self.password,
            start_tls=True
        )

    def _is_success(self, response: dict) -> bool:
        """Check if SMS was successfully sent"""
        return any("OK" in str(part) for part in response)
