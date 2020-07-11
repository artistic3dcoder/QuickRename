from typing import Type
from views.file_item_view import FileItemView


class FileItemController(object):
    """Responsible for managing FileItemView."""
    def __init__(self, label: str):
        """Instantiation of FileItemController.

        Args:
            label: Name of item being tracked by controller.
        """
        self._view = FileItemView()
        self._label = label
        self._configure()

    def _configure(self) -> None:
        """Configure controller."""
        self._view.set_label(label=self._label)
        self._view.add_controller(controller=self)

    @property
    def view(self) -> Type[FileItemView]:
        """FileItemView: View associated with controller."""
        return self._view

    @property
    def name(self) -> str:
        """Name associated with the FileItemView."""
        return self._view.name

    def checked(self) -> bool:
        """Return if the current item is checked."""
        return self._view.checked()

    def set_check_state(self, check_state: object) -> None:
        """Set the check_state of the current view."""
        self._view.set_check_state(state=check_state)
