from abc import ABC, abstractmethod

class NotificationPort(ABC):
    """Notification port interface"""
    @abstractmethod
    def send_alert(self, message: str) -> bool:
        """Send alert message"""
        raise NotImplementedError