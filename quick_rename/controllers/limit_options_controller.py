from views.limit_options_view import LimitOptionsView
from defaults import limit_options_prefs as prefs


class LimitOptionsController(object):
    """Responsible for managing LimitOptionsView."""
    def __init__(self):
        self._view = LimitOptionsView()
        self._add_connections()

    def _add_connections(self) -> None:
        """Add Connections to self._view."""
        self._view.limit_type_cb.toggled.connect(self.toggle_limit_view)
        self._view.limit_type.editingFinished.connect(self.check_limit_type)
        self._view.search_cb.toggled.connect(self.toggle_search)
        self._view.search.textEdited.connect(self.check_search_str)

    @property
    def view(self) -> LimitOptionsView:
        return self._view

    def check_limit_type(self) -> None:
        """Check the limit type value.

        Note:
            If the limit type value is None the default value will be added
        """
        if not self._view.get_limit_type():
            self._view.set_limit_type(value=prefs.LIMIT_DEFAULT)
            self._view.set_limit_type_style(style=prefs.COLOR_INVALID)
        else:
            self._view.set_limit_type_style(style=prefs.COLOR_VALID)

    def check_search_str(self) -> None:
        """Check the search str value.

        Note:
            If the search str value is None the default value will be added
        """
        if not self._view.get_search():
            self._view.set_search(value=prefs.SEARCH_DEFAULT)
            self._view.set_search_style(style=prefs.COLOR_INVALID)
        else:
            self._view.set_search_style(style=prefs.COLOR_VALID)

    def get_extension(self) -> str:
        """Return formatted extension from self._view.limit_type"""
        ext = self._view.get_limit_type()
        return f".{ext}" if ext else None

    @staticmethod
    def is_default_file_type(value: str) -> bool:
        """Return if the value is the default file extension hint value."""
        return value == prefs.LIMIT_DEFAULT

    @staticmethod
    def is_default_search_value(value: str) -> bool:
        """Return if the value is the default search hint value."""
        return value == prefs.SEARCH_DEFAULT

    def limit(self) -> bool:
        """Return if the self.view's  limit is checked."""
        return self._view.get_do_limit_type()

    def limit_to(self) -> str:
        """Return the value self.view's limit is set to."""
        return self._view.get_limit_type()

    def search(self) -> bool:
        """Return if the self.view's  search is checked."""
        return self._view.get_do_search()

    def search_for(self) -> str:
        """Return the value self.view's search is set to."""
        return self._view.get_search()

    def set_disabled(self) -> None:
        """Disable View."""
        self._view.set_disabled()

    def set_enable(self) -> None:
        """Enable View."""
        self._view.set_enable()

    def toggle_limit_view(self) -> None:
        """Toggle file limiting feature for LimitOptionsView."""
        if self._view.get_do_limit_type():
            self._view.enable_limit_type()
            if self._view.get_limit_type() == prefs.LIMIT_DEFAULT:
                self._view.set_limit_type_style(style=prefs.COLOR_INVALID)
            else:
                self._view.set_limit_type_style(style=prefs.COLOR_VALID)
        else:
            self._view.disable_limit_type()
            self._view.set_limit_type_style(style=prefs.COLOR_DISABLED)

    def toggle_search(self) -> None:
        """Toggle the search text feature."""
        if self._view.get_do_search():
            self._view.enable_search()
            if self._view.get_search() == prefs.SEARCH_DEFAULT:
                self._view.set_search_style(style=prefs.COLOR_INVALID)
            else:
                self._view.set_search_style(style=prefs.COLOR_VALID)
        else:
            self._view.disable_search()
            self._view.set_search_style(style=prefs.COLOR_DISABLED)
