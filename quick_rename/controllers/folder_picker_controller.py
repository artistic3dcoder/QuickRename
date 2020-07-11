from os.path import join, isdir
from os import makedirs
from datetime import datetime

from views.folder_picker_view import FolderPickerView
from widgets.custom_widgets import FileDirectoryDialog
from defaults.quick_rename_prefs import BACKUP_DIR


class FolderPickerController(object):
    """Responsible for managing interactions with the FolderPickerView."""
    def __init__(self):
        self._view = FolderPickerView()
        self._configure_connections()

    @property
    def view(self) -> object:
        """Return view associated with controller."""
        return self._view

    def _configure_connections(self) -> None:
        """Configure connections to self._views widgets."""
        self._view.file_browser_btn.clicked.connect(self.get_dir)

    def base_dir(self) -> str:
        """Return users selected base directory."""
        return self._view.get_base_dir()

    def get_dir(self) -> None:
        """Prompts user to select folder where files live."""
        directory = FileDirectoryDialog().get_directory()
        if directory:
            self._view.set_base_dir(dir_path=directory)

    def get_dir_set(self) -> bool:
        """Return if the base dir has been set."""
        return self._view.get_base_dir_set()

    def get_backup_dir(self) -> str:
        """Format and Return location where backup are stored for rename.

        Note:
            If the folder does not exist, it will be created.
        """
        date = datetime.now()
        date_folder = f"{date.year}_{date.month}_{date.day}_{date.minute}{date.second}"
        directory = join(self.base_dir(), BACKUP_DIR, date_folder)
        if not isdir(directory):
            makedirs(directory)
        return directory
