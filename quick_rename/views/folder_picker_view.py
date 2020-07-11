from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout

from defaults import folder_picker_prefs as prefs


class FolderPickerView(QWidget):
    """Provides a view which facilitates selecting the source folder where renamable files are found.

    Attributes:
        layout (QHBoxLayout): Main layout for view.
        label (QLabel): Label for file picker widget.
        base_dir (QLineEdit): LineEdit which displays location of where renamable files live.
        file_browser_btn (QPushButton): Button which, when pressed, presents user with a file browsers.
        refresh_btn (QPushButton): Button which, when pressed, Refreshes files in selected directory.
    """
    def __init__(self):
        super(FolderPickerView, self).__init__()
        self.layout = QHBoxLayout()
        self.label = QLabel(prefs.FILE_LOCATION)
        self.base_dir = QLineEdit(prefs.SELECT_DIR)
        self.file_browser_btn = QPushButton(prefs.OPEN_DIR)
        self.refresh_btn = QPushButton(prefs.REFRESH)
        self._configure()

    def _configure(self) -> None:
        """Configuration of FolderPickerView."""
        self.base_dir.setMinimumHeight(prefs.MIN_HEIGHT)
        self.base_dir.setDisabled(True)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.base_dir)
        self.layout.addWidget(self.file_browser_btn)
        self.layout.addWidget(self.refresh_btn)
        self.setLayout(self.layout)

    def get_base_dir(self) -> str:
        """Return path to basedir."""
        return str(self.base_dir.text())

    def get_base_dir_set(self) -> bool:
        """Return if the user has selected a base dir."""
        dir_path = self.get_base_dir()
        return dir_path and dir_path != prefs.SELECT_DIR

    def set_base_dir(self, dir_path: str) -> None:
        """Set the value of base dir.

        Args:
            dir_path : Value to add to the base dir field.
        """
        self.base_dir.setText(dir_path)
