from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QCheckBox, QLineEdit, QSpinBox,
                               QComboBox, QFrame)

from defaults import rename_options_prefs as prefs


class RenameOptionsView(QWidget):
    """View responsible for holding renaming options.
    
    Attributes:
        layout (QVBoxLayout): Main layout of view.
        frame_layout (QVBoxLayout: Layout of frame which holds options.
        frame (QFrame): Frame surrounding options.
        prefix_h_layout (QHBoxLayout): Layout holding prefix options.
        complete_rename_h_layout (QHBoxLayout): Layout holding complete rename options.
        search_and_replace_h_layout (QHBoxLayout): Layout holding search and replace options.
        renumber_h_layout (QHBoxLayout): Layout holding renumber options.
        remove_ext_h_layout (QHBoxLayout): Layout holding remove options.
        change_ext_h_layout (QHBoxLayout): Layout holding change extension options.
        create_backup_h_layout (QHBoxLayout): Layout holding backup options.
        preview_h_layout (QHBoxLayout): Layout holding preview options.
        start_lbl (QLabel): Label for renumbering start.
        padding_lbl (QLabel): Label for renumbering padding.
        add_prefix_cb (QCheckBox): Used to signify the user wants to add a prefix to the renaming.
        prefix (QLineEdit): prefix to add.
        complete_rename_cb (QCheckBox): Used to signify the user wants to completely rename the file.
        new_name (QLineEdit): New name used when renaming.
        search_and_replace_cb (QCheckBox): Used to signify the user wants to partially rename files.
        find (QLineEdit): When searching and replacing this is what the user wants to search for.
        replace (QLineEdit): When searching and replacing this is what the user wants to replace with.
        renumber_cb (QCheckBox): Used to signify the user wants to renumber while renaming.
        start_num (QSpinBox): Number to start with when renumbering files.
        padding (QComboBox): Padding to apply to renaming when renumbering files.
        dot_cb (QCheckBox): When checked a dot will be used to separate the renumber from the name.
        remove_ext_cb (QCheckBox): Used to signify the user wants to remove extensions when renaming.
        backup_files_cb (QCheckBox): Used to signify the user wants to backup old files before renaming.
        change_ext_cb (QCheckBox): Used to signify the user wants to change the extension while renaming.
        change_ext (QLineEdit): New extension to add to the renamed file.
        preview_cb (QCheckBox): Used to signify the user wants to preview the rename before renaming.
    """
    def __init__(self):
        super(RenameOptionsView, self).__init__()
        self.layout = QVBoxLayout()
        self.frame_layout = QVBoxLayout()
        self.options_lbl = QLabel(prefs.OPTIONS)
        self.frame = QFrame()
        self.prefix_h_layout = QHBoxLayout()
        self.complete_rename_h_layout = QHBoxLayout()
        self.search_and_replace_h_layout = QHBoxLayout()
        self.renumber_h_layout = QHBoxLayout()
        self.remove_ext_h_layout = QHBoxLayout()
        self.change_ext_h_layout = QHBoxLayout()
        self.create_backup_h_layout = QHBoxLayout()
        self.preview_h_layout = QHBoxLayout()
        self.start_lbl = QLabel(prefs.START_NUM)
        self.padding_lbl = QLabel(prefs.PADDING)
        self.add_prefix_cb = QCheckBox(prefs.PREFIX)
        self.prefix = QLineEdit(prefs.PREFIX_DEFAULT)
        self.complete_rename_cb = QCheckBox(prefs.COMPLETE_RENAME)
        self.new_name = QLineEdit(prefs.COMPLETE_RENAME_DEFAULT)
        self.search_and_replace_cb = QCheckBox(prefs.SEARCH_AND_REPLACE)
        self.find = QLineEdit(prefs.SEARCH_AND_REPLACE_DEFAULT)
        self.replace = QLineEdit(prefs.REPLACE_WITH_DEFAULT)
        self.renumber_cb = QCheckBox(prefs.RENUMBER)
        self.start_num = QSpinBox()
        self.padding = QComboBox()
        self.dot_cb = QCheckBox(prefs.USE_DOT)
        self.remove_ext_cb = QCheckBox(prefs.REMOVE_EXT)
        self.backup_files_cb = QCheckBox(prefs.BACKUP)
        self.change_ext_cb = QCheckBox(prefs.CHANGE_EXT)
        self.change_ext = QLineEdit(prefs.CHANGE_EXT_DEFAULT)
        self.preview_cb = QCheckBox(prefs.PREVIEW)

        self._configure()

    def _configure(self) -> None:
        """Configure the RenameOptionsView."""
        self.frame.setLayout(self.frame_layout)
        self.frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.layout.addWidget(self.options_lbl)
        self.layout.addWidget(self.frame)
        self.add_prefix_cb.setToolTip(prefs.PREFIX_TOOLTIP)
        self.prefix.setDisabled(True)
        self.prefix.setMaximumWidth(prefs.PREFIX_WIDTH)
        self.prefix.setMinimumWidth(prefs.PREFIX_WIDTH)
        self.complete_rename_cb.setToolTip(prefs.COMPLETE_RENAME_TOOLTIP)
        self.new_name.setDisabled(True)
        self.new_name.setMaximumWidth(prefs.NEW_NAME_WIDTH)
        self.new_name.setMinimumWidth(prefs.NEW_NAME_WIDTH)
        self.search_and_replace_cb.setToolTip(prefs.SEARCH_AND_REPLACE_TOOLTIP)
        self.find.setDisabled(True)
        self.find.setMinimumWidth(prefs.FIND_WIDTH)
        self.find.setMaximumWidth(prefs.FIND_WIDTH)
        self.replace.setDisabled(True)
        self.replace.setMaximumWidth(prefs.REPLACE_WIDTH)
        self.replace.setMinimumWidth(prefs.REPLACE_WIDTH)
        self.renumber_cb.setToolTip(prefs.RENUMBER_TOOLTIP)
        self.start_num.setToolTip(prefs.START_NUM_TOOLTIP)
        self.start_num.setDisabled(True)
        self.start_num.setValue(prefs.START_NUM_DEFAULT)
        self.start_num.setMinimumWidth(prefs.START_NUM_MIN_WIDTH)
        self.padding.setToolTip(prefs.PADDING_TOOLTIP)
        self.padding.setDisabled(True)
        self.padding.addItems([str(x) for x in range(10)])
        self.padding.setCurrentIndex(4)
        self.padding.setMinimumWidth(prefs.PADDING_MIN_WIDTH)
        self.dot_cb.setToolTip(prefs.USE_DOT_TOOLTIP)
        self.dot_cb.setDisabled(True)
        self.dot_cb.setChecked(True)
        self.dot_cb.setMinimumWidth(prefs.DOT_WIDTH)
        self.dot_cb.setMaximumWidth(prefs.DOT_WIDTH)
        self.remove_ext_cb.setToolTip(prefs.REMOVE_EXT_TOOLTIP)
        self.change_ext.setToolTip(prefs.CHANGE_EXT_TOOLTIP)
        self.change_ext.setDisabled(True)
        self.backup_files_cb.setToolTip(prefs.BACKUP_TOOLTIP)
        self.backup_files_cb.setChecked(True)
        self.preview_cb.setToolTip(prefs.PREVIEW_TOOLTIP)
        self.preview_cb.setChecked(True)

        self.prefix_h_layout.addWidget(self.add_prefix_cb)
        self.prefix_h_layout.addWidget(self.prefix)
        self.frame_layout.addLayout(self.prefix_h_layout)

        self.complete_rename_h_layout.addWidget(self.complete_rename_cb)
        self.complete_rename_h_layout.addWidget(self.new_name)
        self.frame_layout.addLayout(self.complete_rename_h_layout)

        self.search_and_replace_h_layout.addWidget(self.search_and_replace_cb)
        self.search_and_replace_h_layout.addWidget(self.find)
        self.search_and_replace_h_layout.addWidget(self.replace)
        self.frame_layout.addLayout(self.search_and_replace_h_layout)

        self.renumber_h_layout.addWidget(self.renumber_cb)
        self.renumber_h_layout.addStretch(1)
        self.renumber_h_layout.addWidget(self.start_lbl)
        self.renumber_h_layout.addWidget(self.start_num)
        self.renumber_h_layout.addSpacerItem(QSpacerItem(*prefs.SPACER_SIZE))
        self.renumber_h_layout.addWidget(self.padding_lbl)
        self.renumber_h_layout.addWidget(self.padding)
        self.renumber_h_layout.addSpacerItem(QSpacerItem(*prefs.SPACER_SIZE))
        self.renumber_h_layout.addWidget(self.dot_cb)
        self.frame_layout.addLayout(self.renumber_h_layout)

        self.change_ext_h_layout.addWidget(self.change_ext_cb)
        self.change_ext_h_layout.addWidget(self.change_ext)
        self.frame_layout.addLayout(self.change_ext_h_layout)

        self.remove_ext_h_layout.addWidget(self.remove_ext_cb)
        self.frame_layout.addLayout(self.remove_ext_h_layout)

        self.create_backup_h_layout.addWidget(self.backup_files_cb)
        self.frame_layout.addLayout(self.create_backup_h_layout)

        self.preview_h_layout.addWidget(self.preview_cb)
        self.frame_layout.addLayout(self.preview_h_layout)

        self.frame_layout.addSpacerItem(QSpacerItem(*prefs.SPACER_SIZE))

        self.setLayout(self.layout)

    def disable_change_ext(self) -> None:
        """Disable change extension."""
        self.change_ext.setDisabled(True)

    def disable_dot(self) -> None:
        """Disable dot checkbox."""
        self.dot_cb.setDisabled(True)

    def disable_find(self) -> None:
        """Disable find."""
        self.find.setDisabled(True)

    def disable_new_name(self) -> None:
        """Disable new name."""
        print("disable new name")
        self.new_name.setDisabled(True)

    def disable_padding(self) -> None:
        """Disable padding."""
        self.padding.setDisabled(True)

    def disable_prefix(self) -> None:
        """Disable prefix."""
        self.prefix.setDisabled(True)

    def disable_start_num(self) -> None:
        """Disable start num."""
        self.start_num.setDisabled(True)

    def disable_replace(self) -> None:
        """Disable replace."""
        self.replace.setDisabled(True)

    def enable_change_ext(self) -> None:
        """Disable change extension."""
        self.change_ext.setDisabled(False)

    def enable_dot(self) -> None:
        """Enable dot checkbox."""
        self.dot_cb.setEnabled(True)

    def enable_find(self) -> None:
        """Enable find."""
        self.find.setEnabled(True)

    def enable_new_name(self) -> None:
        """Enable new name."""
        print("enable new name.")
        self.new_name.setEnabled(True)

    def enable_padding(self) -> None:
        """Enable padding."""
        self.padding.setEnabled(True)

    def enable_prefix(self) -> None:
        """Enable prefix."""
        self.prefix.setEnabled(True)

    def enable_replace(self) -> None:
        """Enable replace."""
        self.replace.setEnabled(True)

    def enable_start_num(self) -> None:
        """Enable start num."""
        self.start_num.setEnabled(True)

    def get_add_prefix(self) -> bool:
        """Return if end user wants to add a prefix and it is not the default value."""
        result = self.get_prefix_checked()
        if result and self.get_prefix() == prefs.PREFIX_DEFAULT:
            result = False
        return result

    def get_do_backup(self) -> bool:
        """Return if end user wants to backup files."""
        return self.backup_files_cb.isChecked()

    def get_change_ext(self) -> bool:
        """Return if the change extension checkbox is checked."""
        return self.change_ext_cb.isChecked()

    def get_do_complete_rename(self) -> bool:
        """Get if end user wants to completely rename."""
        return self.complete_rename_cb.isChecked()

    def get_dot(self) -> str:
        """Return dot string based on end users configuration.

        Note:
            If the end user has not enable using dot separators an empty string will be returned.
        """
        return "." if self.get_do_dot() else ""

    def get_do_dot(self) -> bool:
        """Return if the end user wants to use dot separators when renaming."""
        return self.dot_cb.isChecked()

    def get_do_change_ext(self) -> bool:
        """Return if the end user wants to change the extension."""
        result = self.change_ext_cb.isChecked()
        if self.get_new_ext() == prefs.CHANGE_EXT_DEFAULT:
            return False
        return result

    def get_do_padding(self) -> bool:
        """Return if the end user wants to add padding."""
        return False if self.get_padding() == 0 else True

    def get_do_preview(self) -> bool:
        """Return if the end user wants to preview changes."""
        return self.preview_cb.isChecked()

    def get_do_rename(self) -> bool:
        """Return if end user wants to rename the full item and it is not the default value."""
        result = self.complete_rename_cb.isChecked()
        if result and self.get_new_name() == prefs.COMPLETE_RENAME_DEFAULT:
            result = False
        return result

    def get_do_renumber(self) -> bool:
        """Return if the end user wants to renumber."""
        return self.renumber_cb.isChecked()

    def get_do_search(self) -> bool:
        """Return if end user wants to perform a search and replace AND it is not the default values respectfully.

        Note:
            If you only want to know if search and replace is checked use get_search_and_replace.
        """
        result = self.search_and_replace_cb.isChecked()
        if result and (self.get_find() == prefs.SEARCH_AND_REPLACE_DEFAULT
                       or self.get_replace() == prefs.REPLACE_WITH_DEFAULT):
            result = False
        return result

    def get_do_search_and_replace(self) -> bool:
        """Return if end user wants to perform a search and replace."""
        return self.search_and_replace_cb.isChecked()

    def get_find(self) -> str:
        """Return find value."""
        return str(self.find.text())

    def get_new_ext(self) -> str:
        """Return new ext."""
        return str(self.change_ext.text())

    def get_new_name(self) -> str:
        """Return new_name value."""
        return str(self.new_name.text())

    def get_padding(self) -> int:
        """Return the current padding value."""
        return int(self.padding.currentText())

    def get_prefix_checked(self) -> bool:
        """Return if the prefix checkbox is checked."""
        return self.add_prefix_cb.isChecked()
    
    def get_prefix(self) -> str:
        """Return the current prefix value end user has entered."""
        return str(self.prefix.text())

    def get_remove_ext(self) -> bool:
        """Return if end user has checked the remove extension checkbox."""
        return self.remove_ext_cb.isChecked()

    def get_replace(self) -> str:
        """Return the current replace value end user has entered."""
        return str(self.replace.text())

    def get_start_num(self) -> int:
        """Return start number from view."""
        return int(self.start_num.value())

    def set_change_ext_style(self, style: str) -> None:
        """Set style of change extension.

        Args:
            style: Style sheet applied to change extension.
        """
        self.change_ext.setStyleSheet(style)

    def set_disabled(self) -> None:
        """Disable View."""
        self.setDisabled(True)

    def set_enable(self) -> None:
        """Enable View."""
        self.setEnabled(True)

    def set_find(self, value: str) -> None:
        """Set the value of find.

        Args:
            value: Value applied to find
        """
        self.find.setText(value)

    def set_find_style(self, style: str) -> None:
        """Set style of find.

        Args:
            style: Style sheet applied to find.
        """
        self.find.setStyleSheet(style)

    def set_new_name(self, value: str) -> None:
        """Set the value of new name.

        Args:
            value: Value applied to new_name
        """
        self.new_name.setText(value)
        
    def set_new_name_style(self, style: str) -> None:
        """Set style of new_name.
        
        Args:
            style: Style sheet applied to new_name.
        """
        self.new_name.setStyleSheet(style)

    def set_prefix(self, value: str) -> None:
        """Set the value of prefix.

        Args:
            value: Value applied to prefix
        """
        self.prefix.setText(value)

    def set_prefix_style(self, style: str) -> None:
        """Set style of prefix.

        Args:
            style: Style sheet applied to prefix.
        """
        self.prefix.setStyleSheet(style)

    def set_remove_ext(self, state: bool) -> None:
        """Set the remove_ext checkbox as checked or unchecked.

        Args:
            state: Check state of remove_ext.
        """
        self.remove_ext_cb.setCheckState(Qt.Checked if state else Qt.Unchecked)

    def set_replace(self, value: str) -> None:
        """Set the value of replace.

        Args:
            value: Value applied to replace
        """
        self.replace.setText(value)

    def set_replace_style(self, style: str) -> None:
        """Set style of replace.

        Args:
            style: Style sheet applied to replace.
        """
        self.replace.setStyleSheet(style)