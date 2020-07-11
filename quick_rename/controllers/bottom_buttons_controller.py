from views.bottom_buttons_view import BottomButtonsView


class BottomButtonsController(object):
    """Responsible for managing interactions with the BottomButtonsView."""
    def __init__(self):
        self._view = BottomButtonsView()

    @property
    def view(self) -> BottomButtonsView:
        return self._view

    def set_disabled(self) -> None:
        """Disable View."""
        self._view.set_disabled()

    def set_enable(self) -> None:
        """Enable View."""
        self._view.set_enable()
