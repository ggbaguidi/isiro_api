from twilio.rest import Client, TwilioException

from infrastructure.config import Config

from core.ports.notification_port import NotificationPort


class TwilioSmsAdapter(NotificationPort):
    def __init__(self):
        self.client = Client(
            Config.TWILIO_ACCOUNT_SID,
            Config.TWILIO_AUTH_TOKEN
        )

    async def send_alert(self, message: str) -> bool:
        try:
            self.client.messages.create(
                body=message,
                from_=Config.TWILIO_PHONE_NUMBER,
                to=Config.RECIPIENT_PHONE_NUMBER
            )
            return True
        except TwilioException as e:
            print(f"SMS sending failed: {str(e)}")
            return False
