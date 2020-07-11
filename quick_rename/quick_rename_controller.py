from typing import Union, Optional, Iterable
from os import listdir, rename
from os.path import join, exists
from shutil import copy
from re import search
from collections import defaultdict

from views.messaging_view import Alert, Question
from views.quick_rename_view import QuickRenameView
from models.model import PreProcessed, RenameItem
from controllers.folder_picker_controller import FolderPickerController
from controllers.file_item_controller import FileItemController
from controllers.limit_options_controller import LimitOptionsController
from controllers.file_list_controller import FileListController
from controllers.rename_options_controller import RenameOptionsController
from controllers.bottom_buttons_controller import BottomButtonsController
from widgets.custom_widgets import Item
from defaults import quick_rename_prefs as prefs
from defaults import folder_picker_prefs as fp_prefs


class QuickRenameController(object):
    """Central Controller for managing interactions with the QuickRename application.

    Attributes:
        folder_picker_controller (FolderPickerController): Controls and provides folder picker view.
        limit_controller (LimitOptionsController): Controls and provides limit options view. This controller limits
                                                   files that are shown in the file list view.
        file_list_controller (FileListController): Controls and provides a file list view. This controller interacts
                                                   with files the end user wants to rename.
        rename_controller (RenameOptionsController): Controls and provides rename options view. This controller provides
                                                     options applied to renaming and controls how the end user's
                                                     interactions with the view.
        buttons_controller (BottomButtonsController): Controls and provides a buttons view for launching rename process.
        view (QuickRenameView): Main view associated with QuickRename.
        pre_processed (PreProcessed): Model which holds candidate items for renaming.

    """

    def __init__(self):
        self.folder_picker_controller = FolderPickerController()
        self.limit_controller = LimitOptionsController()
        self.file_list_controller = FileListController()
        self.rename_controller = RenameOptionsController()
        self.buttons_controller = BottomButtonsController()

        self.view = QuickRenameView(folder_view=self.folder_picker_controller.view,
                                    limit_view=self.limit_controller.view,
                                    file_view=self.file_list_controller.view,
                                    options_view=self.rename_controller.view,
                                    buttons_view=self.buttons_controller.view)

        self.pre_processed = PreProcessed()
        self._configure()
        self._configure_connections()

    def _configure(self) -> None:
        """Configure view on start."""
        self.limit_controller.set_disabled()
        self.file_list_controller.set_disabled()
        self.rename_controller.set_disabled()
        self.buttons_controller.set_disabled()

    def _configure_connections(self) -> None:
        """Configure connections to self.views widgets."""
        self.folder_picker_controller.view.file_browser_btn.clicked.connect(self.get_files_from_selected_folder)
        self.folder_picker_controller.view.file_browser_btn.clicked.connect(self.enable_view)
        self.folder_picker_controller.view.refresh_btn.clicked.connect(self.get_files_from_selected_folder)
        self.file_list_controller.view.clicked.connect(self.preview)

        self.limit_controller.view.limit_type_cb.toggled.connect(self.get_files_from_selected_folder)
        self.limit_controller.view.limit_type.editingFinished.connect(self.get_files_from_selected_folder)
        self.limit_controller.view.search_cb.toggled.connect(self.get_files_from_selected_folder)
        self.limit_controller.view.search.editingFinished.connect(self.get_files_from_selected_folder)

        self.rename_controller.view.preview_cb.stateChanged.connect(self.preview)
        self.rename_controller.view.change_ext_cb.stateChanged.connect(self.preview)
        self.rename_controller.view.change_ext.editingFinished.connect(self.preview)
        self.rename_controller.view.remove_ext_cb.stateChanged.connect(self.preview)
        self.rename_controller.view.complete_rename_cb.stateChanged.connect(self.preview)
        self.rename_controller.view.new_name.editingFinished.connect(self.preview)
        self.rename_controller.view.search_and_replace_cb.stateChanged.connect(self.preview)
        self.rename_controller.view.find.editingFinished.connect(self.preview)
        self.rename_controller.view.replace.editingFinished.connect(self.preview)
        self.rename_controller.view.add_prefix_cb.stateChanged.connect(self.preview)
        self.rename_controller.view.prefix.editingFinished.connect(self.preview)
        self.rename_controller.view.dot_cb.stateChanged.connect(self.preview)
        self.rename_controller.view.renumber_cb.stateChanged.connect(self.preview)
        self.rename_controller.view.start_num.editingFinished.connect(self.preview)
        self.rename_controller.view.padding.currentIndexChanged.connect(self.preview)
        self.rename_controller.view.change_ext_cb.stateChanged.connect(self.preview)
        self.rename_controller.view.change_ext.textEdited.connect(self.preview)

        self.buttons_controller.view.rename_btn.clicked.connect(self.launch_rename)

    def add_file(self, file_: object, item: object, idx: int, search_for: Optional[str] = None) -> bool:
        """Add a current file to the FileListController.
        Args:
            file_: file name to parse
            item: Item to add to the ListWidget
            idx: Index of item to add to the list (this should be a 1 based index)
            search_for: string of text to search for
        """
        if search_for is not None and search(search_for, file_.name):
            self.file_list_controller.add_item(row=idx, col=0, view=item.view)
            return True
        else:
            self.file_list_controller.add_item(row=idx, col=0, view=item.view)
            return True
        return False

    def collect_folder_items(self) -> None:
        """Collect all valid items found in the selected folder."""
        directory = self.folder_picker_controller.base_dir()
        if directory and directory != fp_prefs.SELECT_DIR:
            dir_list = listdir(directory)
            dir_list.sort()
            for cur_file in dir_list:
                self.pre_processed.add_item(item=cur_file, directory=directory)
        else:
            msg = Alert(title=fp_prefs.INVALID_FOLDER, message=fp_prefs.SELECT_DIR_MSG)
            msg.exec_()

    def enable_view(self) -> None:
        """Enable view."""
        if self.folder_picker_controller.get_dir_set():
            self.limit_controller.set_enable()
            self.file_list_controller.set_enable()
            self.rename_controller.set_enable()
            self.buttons_controller.set_enable()

    def get_files_from_selected_folder(self) -> None:
        """Collect items from directory."""
        if self.folder_picker_controller.get_dir_set():
            self.pre_processed.clear()
            self.file_list_controller.clear()
            self.collect_folder_items()
            self.file_list_controller.set_header_labels()

            do_search = self.limit_controller.search()
            do_limit = self.limit_controller.limit()
            if self.limit_controller.is_default_file_type(value=self.limit_controller.limit_to()):
                do_limit = False
            search_for = self.limit_controller.search_for()
            if self.limit_controller.is_default_search_value(value=search_for):
                do_search = False

            ext_check = self.limit_controller.get_extension()
            self.file_list_controller.set_row_count(rows=self.pre_processed.count(ext=ext_check if do_limit else None))

            column_idx = 0
            for cur_file in self.pre_processed.data:
                # Construct a FileItemController. This will be sent to the FileListView.
                item_controller = FileItemController(label=cur_file.name)
                search_for = search_for if do_search else None
                result = False
                if do_limit:
                    if cur_file.ext == ext_check:
                        result = self.add_file(search_for=search_for, file_=cur_file, item=item_controller, idx=column_idx)
                else:
                    result = self.add_file(search_for=search_for, file_=cur_file, item=item_controller, idx=column_idx)
                if result:
                    column_idx += 1
            self.preview()

    def launch_rename(self) -> None:
        """Main method for renaming files."""
        base_dir = self.folder_picker_controller.base_dir()
        checked_items = self.file_list_controller.get_checked_files()
        if not self.validate_rename(base_dir=base_dir, checked_items=checked_items):
            return None

        if Question(title=prefs.RENAME_FILES, message=prefs.RENAME_FILES_MSG):
            cur_num = self.rename_controller.start_num()
            base_dir = self.folder_picker_controller.base_dir()
            for i, item in enumerate(checked_items):
                old = join(base_dir, item.name)
                if self.rename_controller.do_backup():
                    backup_name = join(self.folder_picker_controller.get_backup_dir(), item.name)
                    copy(old, backup_name)

                new = join(base_dir, self.rename_controller.configure_name(item_name=item.name, pad_number=cur_num))
                if not exists(new):
                    rename(old, new)
                cur_num += 1

            self.get_files_from_selected_folder()

    def preview(self) -> bool:
        """Display a preview of outcome of the renaming configuration against files marked for renaming."""
        self.file_list_controller.clear_preview_column()
        self.file_list_controller.set_header_labels()
        for item in self.file_list_controller.all_items():
            item.set_invalid(state=False)
        if self.rename_controller.do_preview():
            base_dir = self.folder_picker_controller.base_dir()
            checked_items = self.file_list_controller.get_checked_files()
            # Validate rename requires are correct before attempting to preview. Do not check that items are actually
            # checked, we only want to do that when we perform the actual rename.
            if not self.validate_rename(base_dir=base_dir, checked_items=checked_items, require_checked=False):
                return False

            preview_items = defaultdict(list)
            self.collect_renamed_preview_items(checked_items=checked_items,
                                               container=preview_items,
                                               start=self.rename_controller.start_num())
            if self.find_duplicate_preview_items(container=preview_items):
                msg = Alert(title=prefs.DUPLICATES, message=prefs.DUPLICATES_MSG)
                msg.exec_()
                return False

            for item in (v[0] for v in preview_items.values()):
                self.file_list_controller.view.model.setItem(item.row, item.col, item.dest)
        return True

    @staticmethod
    def find_duplicate_preview_items(container: Iterable) -> bool:
        """Iterate all potential rename items and validate that no duplicate items are present.

        Note:
            If duplicated items are found their source Item will be highlighted red.

        Args:
            container: Iterable holding potential rename candidates.
        """
        duplicates_found = False
        for k, v in container.items():
            if len(v) > 1:
                duplicates_found = True
                for item in v:
                    item.src.set_invalid(state=True)
        return duplicates_found

    def collect_renamed_preview_items(self, checked_items: Iterable, container: dict, start: int) -> None:
        """Iterate through checked file_item_views and create a preview RenameItem."""
        for i, item in enumerate(checked_items):
            name = self.rename_controller.configure_name(item_name=item.name, pad_number=i + start)
            container[name].append(RenameItem(row=item.row(), col=1, name=name, src=item, dest=Item(label=name)))

    def show(self) -> None:
        """Show current QuickRenameView."""
        self.view.show()

    def validate_rename(self, base_dir: str, checked_items: list, require_checked: Optional[bool] = True) -> bool:
        """Validate that renaming options are valid before previewing or renaming.

        Args:
            base_dir: Base directory end user has selected.
            checked_items: Files end user has selected to rename.
            require_checked: If True, validate that items are checked.
        """
        if base_dir == fp_prefs.SELECT_DIR:
            msg = Alert(title=prefs.INVALID_FOLDER, message=prefs.INVALID_FOLDER_MSG)
            msg.exec_()
            return False

        if require_checked and not checked_items:
            msg = Alert(title=prefs.INVALID_SELECTION, message=prefs.SELECT_FILES_MSG)
            msg.exec_()
            return False

        if all([self.rename_controller.do_rename(),
                self.file_list_controller.get_checked_files_count() > 1,
                not self.rename_controller.do_renumber()]):
            msg = Alert(title=prefs.MISCONFIGURATION, message=prefs.RENUMBER_MSG)
            msg.exec_()
            return False
        return True


if __name__ == "__main__":
    from sys import argv
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCore import Qt

    app = QApplication(argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_DisableHighDpiScaling)
    ex = QuickRenameController()
    ex.show()
    exit(app.exec_())
