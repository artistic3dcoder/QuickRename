from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton

from defaults import bottom_buttons_prefs as prefs


class BottomButtonsView(QWidget):
    """Bottom most view which houses rename related buttons."""
    def __init__(self):
        super(BottomButtonsView, self).__init__()
        self.layout = QHBoxLayout()
        self.rename_btn = QPushButton(prefs.RENAME)
        self._configure()

    def _configure(self) -> None:
        """Configure the current BottomButtonsView."""
        self.layout.addWidget(self.rename_btn)
        self.setLayout(self.layout)

    def set_disabled(self) -> None:
        """Disable View."""
        self.setDisabled(True)

    def set_enable(self) -> None:
        """Enable View."""
        self.setEnabled(True)
