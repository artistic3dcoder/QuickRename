from typing import Union

from os.path import splitext

from views.rename_options_view import RenameOptionsView
from defaults import rename_options_prefs as prefs


class RenameOptionsController(object):
    """Responsible for managing interactions with the RenameOptionsView."""
    def __init__(self):
        self._view = RenameOptionsView()
        self._add_connections()

    @property
    def view(self) -> RenameOptionsView:
        """Return the view associated with controller."""
        return self._view

    def _add_connections(self) -> None:
        """Add connections to Widgets in self._view."""
        self._view.add_prefix_cb.stateChanged.connect(self.toggle_prefix)
        self._view.prefix.editingFinished.connect(self.check_prefix)
        self._view.complete_rename_cb.clicked.connect(self.toggle_complete_rename)
        self._view.new_name.editingFinished.connect(self.check_complete_rename)
        self._view.search_and_replace_cb.clicked.connect(self.toggle_search_and_replace)
        self._view.find.editingFinished.connect(self.check_search_and_replace_name)
        self._view.replace.editingFinished.connect(self.check_search_and_replace_name)
        self._view.renumber_cb.clicked.connect(self.toggle_renumber)
        self._view.change_ext_cb.clicked.connect(self.toggle_change_ext)

    def add_prefix(self) -> bool:
        """Return if end user wants to add a prefix and it is not the default value."""
        result = self._view.get_prefix_checked()
        if result and self._view.get_prefix() == prefs.PREFIX_DEFAULT:
            result = False
        return result

    @staticmethod
    def apply_padding(num: int, pad: int) -> str:
        """Configure padding for number.

        Args:
            num: number to pad
            pad: padding for number valid values are 1 - 9
        """
        if pad < prefs.MIN_PADDING:
            pad = prefs.MIN_PADDING
        elif pad > prefs.MAX_PADDING:
            pad = prefs.MAX_PADDING
        return str(num).rjust(pad).replace(" ", "0")

    def check_complete_rename(self) -> None:
        """Checks the state of the rename value to see if it is valid."""
        if not self._view.get_new_name():
            self._view.set_new_name(value=prefs.COMPLETE_RENAME_DEFAULT)
            self._view.set_new_name_style(style=prefs.COLOR_INVALID)
        else:
            self._view.set_new_name_style(style=prefs.COLOR_VALID)

    def check_prefix(self) -> None:
        """Checks the state of the prefix value to see if it is valid."""
        if not self._view.get_prefix():
            self._view.set_prefix(value=prefs.PREFIX_DEFAULT)
            self._view.set_prefix_style(style=prefs.COLOR_INVALID)
        else:
            self._view.set_prefix_style(style=prefs.COLOR_VALID)

    def check_search_and_replace_name(self) -> None:
        """Check the state of the rename value to see if it is valid."""
        if not self._view.get_find():
            self._view.set_find(value=prefs.SEARCH_AND_REPLACE_DEFAULT)
            self._view.set_find_style(style=prefs.COLOR_INVALID)
        else:
            self._view.set_find_style(style=prefs.COLOR_VALID)

        if self._view.get_replace():
            self._view.set_replace_style(style=prefs.COLOR_VALID)

    def configure_name(self, item_name: str, pad_number: int) -> Union[str, None]:
        """Configure name of item based on settings.

        Args:
            item_name: the item to rename
            pad_number: padding
        """
        parts = splitext(item_name)
        item_name = parts[0]
        if self._view.get_remove_ext():
            ext = ""
        elif not self._view.get_do_change_ext():
            ext = parts[-1]
        else:
            ext = self._view.get_new_ext()

        if self._view.get_do_rename():
            item_name = self._view.get_new_name()
        # Search and Replace if the user is not doing a full name. This options comes second to a full rename.
        elif self._view.get_do_search():
            search_for = self._view.get_find()
            if search_for in item_name:
                item_name = item_name.replace(search_for, self._view.get_replace())
        if self._view.get_add_prefix():
            item_name = f"{self._view.get_prefix()}{item_name}"
        if self._view.get_do_renumber():
            dot = self._view.get_dot()
            if self._view.get_do_padding():
                padding_ = self.apply_padding(num=pad_number, pad=self._view.get_padding())
                new_name = f"{item_name}{dot}{padding_}{ext}"
            else:
                new_name = f"{item_name}{dot}{pad_number}{ext}"
        else:
            new_name = f"{item_name}{ext}"
        return new_name

    def do_backup(self) -> bool:
        """Return if end user wants to backup files."""
        return self._view.get_do_backup()

    def do_preview(self) -> bool:
        """Return if the end user wants to preview changes."""
        return self._view.get_do_preview()

    def do_rename(self) -> bool:
        """Return if end user wants to rename the full item and it is not the default value."""
        return self._view.get_do_rename()

    def do_renumber(self) -> bool:
        """Return if the end user wants to renumber."""
        return self._view.get_do_renumber()

    def padding(self) -> int:
        """Return the current padding value."""
        return self._view.get_padding()

    def set_disabled(self) -> None:
        """Disable View."""
        self._view.set_disabled()

    def set_enable(self) -> None:
        """Enable View."""
        self._view.set_enable()

    def start_num(self) -> int:
        """Return start number from view."""
        return self._view.get_start_num()

    def toggle_change_ext(self) -> None:
        """Toggle the change extension feature."""
        if self._view.get_change_ext():
            self._view.set_remove_ext(False)
            self._view.enable_change_ext()
            self._view.set_change_ext_style(style=prefs.COLOR_INVALID)
        else:
            self._view.disable_change_ext()
            self._view.set_change_ext_style(style=prefs.COLOR_VALID)

    def toggle_complete_rename(self) -> None:
        """Toggle the complete rename feature."""
        if self._view.get_do_complete_rename():
            self._view.enable_new_name()
            if self._view.get_new_name() == prefs.COMPLETE_RENAME_DEFAULT:
                self._view.set_new_name_style(style=prefs.COLOR_INVALID)
            else:
                self._view.set_new_name_style(style=prefs.COLOR_VALID)
        else:
            self._view.disable_new_name()
            self._view.set_new_name_style(style=prefs.COLOR_DISABLED)

    def toggle_renumber(self) -> None:
        """Toggle the renumber feature."""
        if self._view.get_do_renumber():
            self._view.enable_padding()
            self._view.enable_start_num()
            self._view.enable_dot()
        else:
            self._view.disable_padding()
            self._view.disable_start_num()
            self._view.disable_dot()

    def toggle_search_and_replace(self) -> None:
        """Toggle the search and replace feature."""
        if self._view.get_do_search_and_replace():
            self._view.enable_find()
            self._view.enable_replace()
            if self._view.get_find() == prefs.SEARCH_AND_REPLACE_DEFAULT:
                self._view.set_find_style(style=prefs.COLOR_INVALID)
            else:
                self._view.set_find_style(style=prefs.COLOR_VALID)
            if self._view.get_replace() == prefs.REPLACE_WITH_DEFAULT:
                self._view.set_replace_style(style=prefs.COLOR_INVALID)
            else:
                self._view.set_replace_style(style=prefs.COLOR_VALID)
        else:
            self._view.disable_find()
            self._view.disable_replace()
            self._view.set_find_style(style=prefs.COLOR_DISABLED)
            self._view.set_replace_style(style=prefs.COLOR_DISABLED)

    def toggle_prefix(self) -> None:
        """Toggle the prefix adding feature."""
        if self._view.get_prefix_checked():
            self._view.enable_prefix()
            if self._view.get_add_prefix():
                self._view.set_prefix_style(style=prefs.COLOR_VALID)
            else:
                self._view.set_prefix_style(style=prefs.COLOR_INVALID)
        else:
            self._view.disable_prefix()
            self._view.set_prefix_style(style=prefs.COLOR_DISABLED)
