from abc import ABC, abstractmethod
from datetime import datetime


class IEventRecorder(ABC):
    """
    Interface for any component that can record user events.

    Method:
      - record(e: UserEvent): store or process the given event.
    """

    @abstractmethod
    def record(self, e: "UserEvent") -> None:
        pass


class UserEvent:
    """
    Represents a user-generated event in the system.

    Attributes:
      - type: str         # e.g. 'login', 'preference_submit'
      - timestamp: datetime
    """

    def __init__(self, type: str, timestamp: datetime = None):
        self.type = type
        self.timestamp = timestamp or datetime.now()

    def __repr__(self):
        return f"<UserEvent type={self.type!r} timestamp={self.timestamp!r}>"
