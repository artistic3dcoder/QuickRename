from PySide2.QtWidgets import QWidget, QCheckBox, QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QFrame, QLabel
from PySide2.QtCore import Qt

from defaults import limit_options_prefs as prefs


class LimitOptionsView(QWidget):
    """View which displays options for limiting they type of files to work with.

    Attributes:
        layout (QVBoxLayout): Main layout for view.
        frame (QFrame): Frame around limit options.
        frame_layout (QHBoxLayout): Layout associated with frame.
        title (QLabel): Title associated with view.
        limit_type_cb (QCheckBox): CheckBox which controls if view should be limited by file type.
        limit_type (QLineEdit): File type to limit to.
        search_cb (QCheckBox): CheckBox which controls if the view should limit by a search word.
        search (QLineEdit): Word to search for when renaming.
    """
    def __init__(self):
        super(LimitOptionsView, self).__init__()
        self.layout = QVBoxLayout()
        self.title = QLabel(prefs.TITLE)
        self.frame_layout = QHBoxLayout()
        self.frame = QFrame()
        self.limit_type_cb = QCheckBox(prefs.LIMIT)
        self.limit_type = QLineEdit(prefs.LIMIT_DEFAULT)
        self.search_cb = QCheckBox(prefs.SEARCH)
        self.search = QLineEdit(prefs.SEARCH_DEFAULT)

        self._configure()

    def _configure(self) -> None:
        """Configure LimitOptionsView."""
        self.frame.setLayout(self.frame_layout)
        self.layout.setAlignment(Qt.AlignLeft)
        self.limit_type_cb.setToolTip(prefs.LIMIT_TOOLTIP)
        self.search_cb.setToolTip(prefs.SEARCH_TOOLTIP)

        self.frame_layout.addWidget(self.limit_type_cb)
        self.frame_layout.addWidget(self.limit_type)
        self.frame_layout.addSpacerItem(QSpacerItem(*prefs.ITEM_SPACING))
        self.frame_layout.addWidget(self.search_cb)
        self.frame_layout.addWidget(self.search)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)

    def disable_limit_type(self) -> None:
        """Disable limit type functionality."""
        self.limit_type.setDisabled(True)

    def disable_search(self) -> None:
        """Disable search functionality."""
        self.search.setDisabled(True)

    def enable_limit_type(self) -> None:
        """Enable limit type functionality."""
        self.limit_type.setEnabled(True)

    def enable_search(self) -> None:
        """Enable limit type functionality."""
        self.limit_type.setEnabled(True)

    def get_limit_type(self) -> str:
        """Return the limit type."""
        return str(self.limit_type.text())

    def get_do_limit_type(self) -> bool:
        """Return if end user wants to limit the file type."""
        return self.limit_type_cb.isChecked()
    
    def get_search(self) -> str:
        """Return the search value."""
        return str(self.search.text())

    def get_do_search(self) -> bool:
        """Return if the end user wants to limit files by a search."""
        return self.search_cb.isChecked()

    def set_disabled(self) -> None:
        """Disable View."""
        self.setDisabled(True)

    def set_enable(self) -> None:
        """Enable View."""
        self.setEnabled(True)

    def set_limit_type(self, value: str) -> None:
        """Set the value in the limit type."""
        self.limit_type.setText(value)
        
    def set_limit_type_style(self, style: str) -> None:
        """Set the style applied to limit type."""
        self.limit_type.setStyleSheet(style)

    def set_search(self, value: str) -> None:
        """Set the value in the search."""
        self.search.setText(value)

    def set_search_style(self, style: str) -> None:
        """Set the style applied to search."""
        self.search.setStyleSheet(style)
