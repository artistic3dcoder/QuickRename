from typing import Type, Optional
from collections import namedtuple
from os.path import join, splitext, isfile


PreProcessedData = namedtuple("pre_processed_data", "name path ext")


class RenameItem(object):
    """Model which holds renamed items."""
    __slots__ = ("col", "row", "name", "src", "dest")

    def __init__(self, col, row, name, src, dest):
        self.col = col
        self.row = row
        self.name = name
        self.src = src
        self.dest = dest


class PreProcessed(object):
    """Model for handling managing unprocessed files."""

    def __init__(self):
        self._data = []

    @property
    def data(self) -> Type[PreProcessedData]:
        """ preprocessed item paths."""
        return self._data

    def add_item(self, item: str, directory: str) -> bool:
        """Add an item to the structure.

        Note:
            If item is not a file it will not be added.

        Args:
            item: File name to track.
            directory: Directory when item lives.

        """
        path = join(directory, item)
        if isfile(path):
            self._data.append(PreProcessedData(name=item, path=path, ext=splitext(item)[-1]))
            return True
        return False

    def clear(self) -> None:
        """Clear PreProcessed data."""
        self._data = []

    def count(self, ext: Optional[str] = None) -> int:
        """Return number of PreProcess items.

        Args:
            ext: Extension to consider.
        """
        if ext is not None:
            count = len([x for x in self._data if x.ext == ext])
        else:
            count = len(self._data)
        return count
