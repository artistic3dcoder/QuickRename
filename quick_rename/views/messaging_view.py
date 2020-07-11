from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import Qt


class Message(QMessageBox):
    """Base Messaging Widget."""
    def __init__(self, title: str, message: str):
        """Initialization of Message View.

        Args:
            title: Title applied to Message.
            message: Message to display.
        """
        super(Message, self).__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)


class Question(Message):
    """A Messaging widget configured to ask a question."""
    def __init__(self, title: str, message: str):
        """Initialization of Question Messaging View.

        Args:
            title: Title applied to Message.
            message: Message to display.
        """
        super(Question, self).__init__(title=title, message=message)
        self.setIcon(QMessageBox.Question)
        self.setStandardButtons(QMessageBox.Ok)


class Alert(Message):
    """A Messaging widget configured to alert end user a message."""

    def __init__(self, title: str, message: str):
        """Initialization of Alert Messaging View.

        Args:
            title: Title applied to Message.
            message: Message to display.
        """
        super(Alert, self).__init__(title=title, message=message)
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Ok)
