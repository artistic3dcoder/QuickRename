#!/usr/bin/python36
# Verision 1.0
# Author: Walter Behrnes
# Description:
#       File Renaming utility
# Use:
#   python quick_rename.py
# Original: 01/08/2018
# Edit:     01/10/2018


# EXTERNAL
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtGui import QColor, QDrag, QPixmap, QFont
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore


# NATIVE
import os
import sys
import re
import shutil


class CustomTable(QTableView):
    """
    CustomTable which inherits the QTableView Class.
    This implementation fixes an apparent issue with the QTableView where if you drag and drop internally
    The dragged item when dropped would overwrite the item it was dropped on and leave a hole in the table
    where the dragged item originates from.
    """
    def __init__(self):
        super().__init__()

        self.model = QStandardItemModel(1, 2)
        self.setModel(self.model)

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalHeader().hide()

        self.model.setColumnCount(2)
        self.model.setHorizontalHeaderLabels(["Original Files", "New Name - Preview"])
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setMinimumHeight(300)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropOverwriteMode(False)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def dropEvent(self, event):
        """
        overwrite drop event to handle drop events how we need to drop the item.
        """
        # The QTableWidget from which selected rows will be moved
        sender = event.source()
        # GET ROW BEING DROPPED
        dropRow = self.model.itemFromIndex(self.indexAt(event.pos())).row()
        # GET SELECTED ITEMS
        selectedItems = sender.get_selected_items()
        # MOVE ITEM
        for data in selectedItems:
            if data.text():
                checked = data.checkState()
                new_item = QStandardItem(data.text())
                new_item.setCheckState(checked)
                new_item.setCheckable(True)
                self.model.insertRow(dropRow, new_item)
        event.accept()

    def get_selected_items(self):
        """
        method used to return a list of selected items
        Returns:
            list
        """
        selected_rows = []

        for index in self.selectedIndexes():
            item = self.model.itemFromIndex(index)
            if item not in selected_rows:
                selected_rows.append(item)

        selected_rows.sort()
        return selected_rows

class QuickRename(QWidget):

    def __init__(self):
        super().__init__()

        # CREATE A DICTIONARY OF DEFAULT VALUES
        self._defaults = dict(
            select_dir="...select a directory",
            prefix="...prefix",
            new_name="...new name",
            search_for="...search for",
            replace_with="...replace with",
            file_type="...file type",
            search_str="...search str"
        )
        self.main_layout = QVBoxLayout()
        self.file_view = QHBoxLayout()
        self.process_view = QHBoxLayout()
        self.init_ui()

    def add_display_otions_ui_elements(self):
        """
        method used to add the display options to the gui
        Returns:
             None
        """
        options_layout = QHBoxLayout()
        self.limit_view = QCheckBox("Limit file type")
        self.limit_view.setToolTip("When checked only show parse type files")
        self.limit_view.toggled.connect(self.toggle_limit_view)
        self.limit_view.toggled.connect(self.get_files_from_selected_folder)
        self.limit_type = QLineEdit(self._defaults['file_type'])
        self.limit_type.setDisabled(True)
        self.limit_type.setMaximumWidth(77)
        self.limit_type.editingFinished.connect(self.check_limit_type)
        self.limit_type.textEdited.connect(self.get_files_from_selected_folder)

        self.search = QCheckBox("Limit file text")
        self.search_text = QLineEdit(self._defaults['search_str'])
        self.search_text.setDisabled(True)
        self.search.toggled.connect(self.toggle_search)
        self.search.toggled.connect(self.get_files_from_selected_folder)
        self.search_text.editingFinished.connect(self.check_search_str)
        self.search_text.textEdited.connect(self.get_files_from_selected_folder)
        options_layout.addWidget(self.limit_view)
        options_layout.addWidget(self.limit_type)
        options_layout.addSpacerItem(QSpacerItem(20, 5))
        options_layout.addWidget(self.search)
        options_layout.addWidget(self.search_text)
        options_layout.addStretch(1)

        # ADD options_layout TO self.main_layout
        self.main_layout.addLayout(options_layout)

    def add_file_list_ui_elements(self):
        """
        method used to add a list view to the  gui.
        This list view will be used to display files the user can rename
        Returns:
            None
        """
        self.files = CustomTable()
        self.files.clicked.connect(self.update_check_state)
        self.file_view.addWidget(self.files)

    def add_folder_ui_elements(self):
        """
        method used to populate folder gui elements
        Returns:
            None
        """

        folder_layout = QHBoxLayout()
        label = QLabel("Files Location : ")
        self.base_dir = QLineEdit(self._defaults['select_dir'])
        self.base_dir.setMinimumHeight(32)
        self.file_browser = QPushButton("Open Directory")
        self.file_browser.clicked.connect(self.get_dir)
        self.refresh = QPushButton("Refresh")
        self.refresh.clicked.connect(self.get_files_from_selected_folder)
        folder_layout.addWidget(label)
        folder_layout.addWidget(self.base_dir)
        folder_layout.addWidget(self.file_browser)
        folder_layout.addWidget(self.refresh)

        # ADD folder_layout TO self.main_layout
        self.main_layout.addLayout(folder_layout)

    def add_file_to_file_list(self, search, search_for, cur_file, item, index):
        """
        method used to add a current file (QTableWidgetItem) to the Files QTableWidget
        Args:
            search (bool,int): search for text string in cur_file
            search_for (str): string of text to search for
            cur_file (str): file name to parse
            item (QTableWidgetItem): Item to add to the ListWidget
            index (int): Index of item to add to the list (this should be a 1 based index)
        Returns:
            None
        """

        if search:
            # CHECK TO SEE IF SEARCH TEXT IS IN THE FILE
            if re.search(search_for, cur_file):
                self.files.model.setItem(index, 0, item)
        else:
            self.files.model.setItem(index, 0, item)

    def add_rename_options_ui_elements(self):
        """
        method used to add the rename options to the gui
        Returns:
             None
        """
        rename_layout = QVBoxLayout()
        h_layout_1 = QHBoxLayout()
        self.add_prefix = QCheckBox("Add prefix:")
        self.add_prefix.setToolTip("When checked add a prefix to the files being renamed")
        self.add_prefix.clicked.connect(self.toggle_add_prefix)
        self.prefix = QLineEdit(self._defaults['prefix'])
        self.prefix.setDisabled(True)
        self.prefix.editingFinished.connect(self.check_prefix)
        self.prefix.setMaximumWidth(200)
        self.prefix.setMinimumWidth(200)
        h_layout_1.addWidget(self.add_prefix)
        h_layout_1.addWidget(self.prefix)
        rename_layout.addLayout(h_layout_1)

        h_layout_2 = QHBoxLayout()
        self.complete_rename = QCheckBox("Complete Rename:")
        self.complete_rename.setToolTip("When checked the selected items will be completely renamed")
        self.complete_rename.clicked.connect(self.toggle_complete_rename)
        self.new_name = QLineEdit(self._defaults['new_name'])
        self.new_name.setDisabled(True)
        self.new_name.editingFinished.connect(self.check_complete_rename)
        self.new_name.setMaximumWidth(200)
        self.new_name.setMinimumWidth(200)
        h_layout_2.addWidget(self.complete_rename)
        h_layout_2.addWidget(self.new_name)
        rename_layout.addLayout(h_layout_2)

        h_layout_3 = QHBoxLayout()
        self.search_and_replace = QCheckBox("Search / Replace:")
        self.search_and_replace.setToolTip("When Checked search for a string of text and replace with a new string")
        self.search_and_replace.clicked.connect(self.toggle_search_and_replace)
        self.find = QLineEdit(self._defaults['search_for'])
        self.find.setDisabled(True)
        self.find.editingFinished.connect(self.check_search_and_replace_name)
        self.find.setMinimumWidth(200)
        self.find.setMaximumWidth(200)
        self.replace = QLineEdit(self._defaults['replace_with'])
        self.replace.setDisabled(True)
        self.replace.editingFinished.connect(self.check_search_and_replace_name)
        self.replace.setMaximumWidth(200)
        self.replace.setMinimumWidth(200)
        h_layout_3.addWidget(self.search_and_replace)
        h_layout_3.addWidget(self.find)
        h_layout_3.addWidget(self.replace)
        rename_layout.addLayout(h_layout_3)

        h_layout_4 = QHBoxLayout()
        self.renumber = QCheckBox("Renumber")
        self.renumber.setToolTip("When checked add renumbering to the selected items.\n"
                                 "Drag and Drop the selected items in the order you want the renumbering to happen.")
        self.renumber.clicked.connect(self.toggle_renumber)
        start_label = QLabel("Starting Number:")
        self.start_num = QSpinBox()
        self.start_num.setToolTip("Set the start number for the renaming utilize")
        self.start_num.setDisabled(True)
        self.start_num.setValue(1)
        self.start_num.setMinimumWidth(50)
        label = QLabel("Padding:")
        padding_list = [str(x) for x in range(10)]
        self.padding = QComboBox()
        self.padding.setToolTip("Set the padding to apply to the renumbering")
        self.padding.setDisabled(True)
        self.padding.addItems(padding_list)
        self.padding.setCurrentIndex(4)
        self.padding.setMinimumWidth(50)
        self.dot = QCheckBox("Use Dot numbering")
        self.dot.setToolTip("Use a dot notation when numbering/\nExample: name.001.ext")
        self.dot.setDisabled(True)
        self.dot.setChecked(True)
        self.dot.setMinimumWidth(200)
        self.dot.setMaximumWidth(200)
        h_layout_4.addWidget(self.renumber)
        h_layout_4.addStretch(1)
        h_layout_4.addWidget(start_label)
        h_layout_4.addWidget(self.start_num)
        h_layout_4.addSpacerItem(QSpacerItem(25, 25))
        h_layout_4.addWidget(label)
        h_layout_4.addWidget(self.padding)
        h_layout_4.addSpacerItem(QSpacerItem(25, 25))
        h_layout_4.addWidget(self.dot)
        rename_layout.addLayout(h_layout_4)

        h_layout_5 = QHBoxLayout()
        self.ext = QCheckBox("Remove Extension")
        self.ext.setToolTip("Remove the extension when renaming."
                            "\nThis is useful if you have an incorrect ext applied.")
        h_layout_5.addWidget(self.ext)
        rename_layout.addLayout(h_layout_5)
        rename_layout.addSpacerItem(QSpacerItem(25, 25))
        h_layout_6 = QHBoxLayout()
        self.backup_files = QCheckBox("Backup Files")
        self.backup_files.setToolTip("Create a backup of the files before renaming")
        self.backup_files.setChecked(True)
        self.preview_button = QPushButton("Preview")
        self.preview_button.setToolTip("When pressed show a preview of what the end result of the renaming "
                                       "will look like")
        self.preview_button.clicked.connect(self.preview)
        self.rename_button = QPushButton("Rename")
        self.rename_button.clicked.connect(self.launch_rename)
        h_layout_6.addWidget(self.backup_files)
        h_layout_6.addStretch(1)
        h_layout_6.addWidget(self.preview_button)
        h_layout_6.addWidget(self.rename_button)
        rename_layout.addLayout(h_layout_6)

        # PUSH EVERYTHING TO THE TOP
        rename_layout.addStretch(1)

        # ADD rename_layout TO self.file_view
        self.process_view.addLayout(rename_layout)

    def check_prefix(self):
        """
        method which checks the state of the prefix value to see if it is valid
        Returns:
             None
        """
        if not self.prefix.text():
            self.prefix.setText(self._defaults['prefix'])
            self.prefix.setStyleSheet("color:red")
        else:
            self.prefix.setStyleSheet("color:black")

    def check_complete_rename(self):
        """
        method which checks the state of the rename value to see if it is valid
        Returns:
             None
        """
        if not self.new_name.text():
            self.new_name.setText(self._defaults['new_name'])
            self.new_name.setStyleSheet("color:red")
        else:
            self.new_name.setStyleSheet("color:black")

    def check_search_and_replace_name(self):
        """
        method which checks the state of the rename value to see if it is valid
        Returns:
             None
        """
        if not self.find.text():
            self.find.setText(self._defaults['search_for'])
            self.find.setStyleSheet("color:red")
        else:
            self.find.setStyleSheet("color:black")

        if self.replace.text():
            self.replace.setStyleSheet("color:black")

    def check_limit_type(self):
        """
        method used to check the limit type value.
        If the limit type value is None the default value will be added
        Returns:
            None
        """
        if not self.limit_type.text():
            self.limit_type.setText(self._defaults['file_type'])
            self.limit_type.setStyleSheet("color: red")
        else:
            self.limit_type.setStyleSheet("color: black")

    def check_search_str(self):
        """
        method used to check the search str value.
        If the search str value is None the default value will be added
        Returns:
            None
        """
        if not self.search_text.text():
            self.search_text.setText(self._defaults['search_str'])
            self.search_text.setStyleSheet("color: red")
        else:
            self.search_text.setStyleSheet("color: black")

    def init_ui(self):
        self.setGeometry(300, 300, 1200, 400)
        self.setWindowTitle('Quick Rename')
        self.setWindowIcon(QIcon('images/quick_rename_icon.png'))

        self.add_folder_ui_elements()
        self.add_display_otions_ui_elements()
        self.add_file_list_ui_elements()
        self.add_rename_options_ui_elements()
        self.main_layout.addLayout(self.file_view)
        self.main_layout.addLayout(self.process_view)
        self.main_layout.addStretch(1)
        self.setLayout(self.main_layout)

        style = "QLineEdit{border-radius:5px; background-color: #d5dce0; height:20px; padding:6px;} " \
                "QPushButton{border-radius:5px; background-color:#ffa530; height:20px; padding:6px; font: bold;}" \
                "QPushButton:hover{border-radius:5px; background-color:#ff6600; height:20px; padding:6px; font: bold;}" \
                "QLabel{font: bold;}" \
                "QCheckBox{spacing:5px; font: bold;}" \
                "QCheckBox::indicator:unchecked{ image: url(images/unchecked.png);}" \
                "QCheckBox::indicator:checked{ image: url(images/checked.png);}" \
                "QCheckBox::indicator:hover{ image: url(images/hover.png);}" \
                "QComboBox{border-radius:5px; background-color: #d5dce0; height:20px; padding:6px;} "
        self.setStyleSheet(style)
        self.show()

    def get_dir(self):
        """
        method which prompts user to select folder where files live
        Returns:
            None
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory =QFileDialog.getExistingDirectory()
        if directory:
            self.base_dir.setText(directory)
            self.get_files_from_selected_folder()

    def refresh(self):
        """
        method which refreshing file list
        Returns:
            None
        """
        directory = self.base_dir.text()
        if directory == self._defaults['select_dir']:
            # ALERT USER THAT THEY NEED TO SUPPLY A FOLDER
            QMessageBox.question(self, 'Invalid Folder', 'Please select a directory to refresh', QMessageBox.Ok,
                                 QMessageBox.Ok)
            return

        self.get_files_from_selected_folder(directory)

    def toggle_add_prefix(self):
        """
        method used to toggle the prefix adding feature
        Returns:
            None
        """
        if self.add_prefix.isChecked():
            self.prefix.setEnabled(True)
            if self.prefix.text() == self._defaults['prefix']:
                self.prefix.setStyleSheet("color: red")
            else:
                self.prefix.setStyleSheet("color: black")
        else:
            self.prefix.setEnabled(False)
            self.prefix.setStyleSheet("color: gray")

    def toggle_complete_rename(self):
        """
        method used to toggle the complete rename feature
        Returns:
            None
        """
        if self.complete_rename.isChecked():
            self.new_name.setEnabled(True)
            if self.new_name.text() == self._defaults['new_name']:
                self.new_name.setStyleSheet("color: red")
            else:
                self.new_name.setStyleSheet("color: black")
        else:
            self.new_name.setEnabled(False)
            self.new_name.setStyleSheet("color: gray")

    def toggle_limit_view(self):
        """
        method used to toggle the file limiting feature
        Returns:
            None
        """
        if self.limit_view.isChecked():
            self.limit_type.setEnabled(True)
            if self.limit_type.text() == self._defaults['file_type']:
                self.limit_type.setStyleSheet("color: red")
            else:
                self.limit_type.setStyleSheet("color: black")
        else:
            self.limit_type.setEnabled(False)
            self.limit_type.setStyleSheet("color: gray")

    def toggle_renumber(self):
        """
        method used to toggle the renumber feature
        Returns:
            None
        """
        if self.renumber.isChecked():
            self.padding.setEnabled(True)
            self.start_num.setEnabled(True)
            self.dot.setEnabled(True)
        else:
            self.padding.setDisabled(True)
            self.start_num.setDisabled(True)
            self.dot.setDisabled(True)

    def toggle_search(self):
        """
        method used to toggle the search text feature
        Returns:
            None
        """
        if self.search.isChecked():
            self.search_text.setEnabled(True)
            if self.search_text.text() == self._defaults['search_str']:
                self.search_text.setStyleSheet("color: red")
            else:
                self.search_text.setStyleSheet("color: black")
        else:
            self.search_text.setEnabled(False)
            self.search_text.setStyleSheet("color: gray")

    def toggle_search_and_replace(self):
        """
        method used to toggle the search and replace feature
        Returns:
            None
        """
        if self.search_and_replace.isChecked():
            self.find.setEnabled(True)
            self.replace.setEnabled(True)
            if self.find.text() == self._defaults['search_for']:
                self.find.setStyleSheet("color: red")
            else:
                self.find.setStyleSheet("color: black")
            if self.replace.text() == self._defaults['replace_with']:
                self.replace.setStyleSheet("color: red")
            else:
                self.replace.setStyleSheet("color: black")
        else:
            self.find.setEnabled(False)
            self.replace.setEnabled(False)
            self.find.setStyleSheet("color: gray")
            self.replace.setStyleSheet("color: gray")

    def get_checked_files(self):
        """
        method used to return a list of checked files for renaming
        Returns:
             list
        """
        # COLLECT CHECKED ITEMS
        checked_items = []
        for i in range(self.files.model.rowCount()):
            item = self.files.model.item(i, 0)
            if item.checkState() == QtCore.Qt.Checked:
                checked_items.append(item)
        return checked_items

    def get_files_from_selected_folder(self):
        """
        method which gets items from directory
        Returns:
            None
        """
        directory = self.base_dir.text()
        if directory and directory != self._defaults['select_dir']:
            parse = self.limit_view.isChecked()
            parse_for = self.limit_type.text()
            if parse_for == self._defaults['file_type']:
                parse = 0
            search = self.search.isChecked()
            search_for = self.search_text.text()
            if search_for == self._defaults['search_str']:
                search = 0
            # PRE-CREATE AN EXTENSION CHECK VAR, THIS WILL BE USED IF THE USER IS LISTING BY FILE TYPE
            ext_check = ".{0}".format(parse_for)

            # CLEAR THE FILE LIST
            self.files.model.clear()
            # GET FILES FROM DIRECTORY
            dir_list = os.listdir(directory)
            # SORT DIRECTORY
            dir_list.sort()

            # GET PROPER ROW COUNT
            row_count = 0
            for cur_file in dir_list:
                # CHECK TO MAKE SURE WE DO NOT ADD A DIRECTORY
                temp_path = os.path.join(directory, cur_file)
                if not os.path.isdir(temp_path):
                    if parse:
                        ext = os.path.splitext(cur_file)[1]
                        if ext == ext_check:
                            row_count += 1
                    else:
                        row_count += 1
            self.files.model.setRowCount(row_count)
            # SET TIME IN ROW
            column_index = 0
            for cur_file in dir_list:
                # CHECK TO MAKE SURE WE DO NOT ADD A DIRECTORY
                temp_path = os.path.join(directory, cur_file)
                if not os.path.isdir(temp_path):
                    # CONSTRUCT A WIDGET ITEM THAT IS CHECKABLE
                    item = QStandardItem(cur_file)
                    item.setFlags(item.flags()|QtCore.Qt.ItemIsUserCheckable)
                    item.setCheckState(QtCore.Qt.Unchecked)
                    # CHECK TO SEE IF THE USER IS TRYING TO LIMIT THE FILE TYPE THEY WANT TO SHOW
                    if parse:
                        ext = os.path.splitext(cur_file)[1]
                        if ext == ext_check:
                            self.add_file_to_file_list(search=search, search_for=search_for, cur_file=cur_file,
                                                       item=item, index=column_index)
                            column_index += 1
                    else:
                        self.add_file_to_file_list(search=search, search_for=search_for, cur_file=cur_file, item=item,
                                                   index=column_index)
                        column_index += 1
        else:
            # ALERT USER THAT THEY NEED TO SUPPLY A FOLDER
            QMessageBox.question(self, 'Invalid Folder', 'Please select a directory to parse', QMessageBox.Ok,
                                 QMessageBox.Ok)
        self.files.model.setHorizontalHeaderLabels(["Original Files", "New Name - Preview"])

    def get_padding(self, num, pad):
        """
        set padding for naming
        Args:
            num (int): number to pad
            pad (int): padding for number valid values are 1 - 9
        Returns:
            str
        """
        xx = "_"
        # VALIDATE PAD, MAKE SURE IT IS 1 to 9
        if pad < 1:
            pad = 1
        elif pad > 9:
            pad = 9
        # EXPAND
        if pad == 1:
            xx = '{0:01d}'.format(num)
        elif pad == 2:
            xx = '{0:02d}'.format(num)
        elif pad == 3:
            xx = '{0:03d}'.format(num)
        elif pad == 4:
            xx = '{0:04d}'.format(num)
        elif pad == 5:
            xx = '{0:05d}'.format(num)
        elif pad == 6:
            xx = '{0:06d}'.format(num)
        elif pad == 7:
            xx = '{0:07d}'.format(num)
        elif pad == 8:
            xx = '{0:08d}'.format(num)
        elif pad == 9:
            xx = '{0:09d}'.format(num)
        return xx

    def configure_name(self, item_to_rename, pad_number):
        """
        method used to configure name
        Args:
            item_to_rename (str): the item to rename
            pad_number (str): padding
        Returns:
            str, None
        """

        # GET VARIABLES
        add_prefix = self.add_prefix.isChecked()
        get_prefix = self.prefix.text()
        if get_prefix == self._defaults['prefix']:
            add_prefix = False

        do_rename = self.complete_rename.isChecked()
        get_rename = self.new_name.text()
        if get_rename == self._defaults['replace_with']:
            do_rename = False

        do_search = self.search_and_replace.isChecked()
        search_for = self.find.text()
        replace_with = self.replace.text()
        if search_for == self._defaults['search_for'] or replace_with == self._defaults['replace_with']:
            do_search = False

        do_renumber = self.renumber.isChecked()
        get_padd = int(self.padding.currentText())
        do_padd = False if get_padd == 0 else True
        do_dot = self.dot.isChecked()
        no_ext = self.ext.isChecked()
        the_ext = os.path.splitext(item_to_rename)[1]
        the_name = os.path.splitext(item_to_rename)[0]
        # SET NAME
        if do_rename == 1:
            the_name = get_rename
        # SEARCH AND REPLACE THIS COMES SECOND TO A FULL RENAME
        elif do_search == 1:
            if search_for in the_name:
                the_name = the_name.replace(search_for, replace_with)
        # SET PREFIX
        if add_prefix == 1:
            the_name = "{}{}".format(get_prefix, the_name)
        # CONFIG NAME
        new_name = None
        if do_renumber == 1:
            dot = ""
            if do_dot == 1:
                dot = "."
            if do_padd == 1:
                xx = self.get_padding(pad_number, get_padd)
                if no_ext == 1:
                    new_name = "{}{}{}".format(the_name, dot, xx)
                else:
                    new_name = "{}{}{}{}".format(the_name, dot, xx, the_ext)
            else:

                if no_ext == 1:
                    new_name = "{}{}{}".format(the_name, dot, pad_number)
                else:
                    new_name = "{}{}{}{}".format(the_name, dot, pad_number, the_ext)
        else:
            if no_ext == 1:
                new_name = the_name
            else:
                new_name = "{}{}".format(the_name, the_ext)
        return new_name

    def preview(self):
        """
        method which shows a preview of action user is configuring
        Returns:
            None
        """
        base_dir = self.base_dir.text()
        if base_dir == self._defaults['select_dir']:
            # ALERT USER THAT THEY NEED TO SUPPLY A FOLDER
            QMessageBox.question(self, 'Invalid Folder', 'Please select a directory to work from', QMessageBox.Ok,
                                 QMessageBox.Ok)
            return None

        get_num = self.start_num.value()
        # COLLECT CHECKED ITEMS
        checked_items = self.get_checked_files()

        if not checked_items:
            # ALERT USER THAT THEY NEED TO SUPPLY A FOLDER
            QMessageBox.question(self, 'Invalid Selection', 'Please select files to preview', QMessageBox.Ok,
                                 QMessageBox.Ok)
            return None

        if len(checked_items) > 1 and self.complete_rename.isChecked() and not self.renumber.isChecked():

            # ALERT USER THAT THEY NEED TO SUPPLY A FOLDER
            QMessageBox.question(self, 'Invalid Selection',
                                 'Please turn on Renumber when completely renaming more that one object',
                                 QMessageBox.Ok, QMessageBox.Ok)
            return None

        for i, item in enumerate(checked_items):
            cur_num = i + get_num
            # CONFIGURE NAME
            preview_name = self.configure_name(item.text(), cur_num)
            # DISPLAY PREVIEW
            preview_item = QStandardItem(preview_name)
            preview_item.setCheckable(False)
            preview_item.setForeground(QColor('#ff0000'))
            font = QFont()
            font.setWeight(QFont.Bold)
            font.setItalic(True)
            preview_item.setFont(font)
            self.files.model.setItem(item.row(), 1, preview_item)

    def update_check_state(self, index):
        """
        private method used to update the check state of the selected item
        Args:
            index (index): Item index to toggle
        Returns:
            None
        """
        item = self.files.model.itemFromIndex(index)
        check_state = item.checkState()

        # ITERATE ALL SELECTED ITEMS AND CHANGE THEIR COLORS
        for cur_index in self.files.selectedIndexes():
            cur_item = self.files.model.itemFromIndex(cur_index)
            cur_item.setCheckState(check_state)
            if check_state == QtCore.Qt.Checked:
                cur_item.setForeground(QColor('#7fc97f'))
            else:
                cur_item.setForeground(QColor('#000000'))
        # IF NO ITEMS WERE SELECTED, AND THE USER ONLY CLICKED A CHECK BOX, HANDLE THIS
        if not self.files.selectedIndexes():
            if check_state == QtCore.Qt.Checked:
                item.setForeground(QColor('#7fc97f'))
            else:
                item.setForeground(QColor('#000000'))

    def launch_rename(self):
        """
        Main method for renaming files
        """

        # SEE IF USER WANTS TO BACK UP FILE
        backup = self.backup_files.isChecked()
        base_dir = self.base_dir.text()
        if base_dir == self._defaults['select_dir']:
            # ALERT USER THAT THEY NEED TO SUPPLY A FOLDER
            QMessageBox.question(self, 'Invalid Folder', 'Please select a directory to work from', QMessageBox.Ok,
                                 QMessageBox.Ok)
            return None

        # GET STARTING NUMBER
        get_num = self.start_num.value()
        # COLLECT CHECKED ITEMS
        checked_items = self.get_checked_files()

        if not checked_items:
            if base_dir == self._defaults['select_dir']:
                # ALERT USER THAT THEY NEED TO SUPPLY A FOLDER
                QMessageBox.question(self, 'Invalid Selection', 'Please select files to rename', QMessageBox.Ok,
                                     QMessageBox.Ok)
            return None

        if len(checked_items) > 1 and self.complete_rename.isChecked() and not self.renumber.isChecked():

            # ALERT USER THAT THEY NEED TO SUPPLY A FOLDER
            QMessageBox.question(self, 'Invalid Selection',
                                 'Please turn on Renumber when completely renaming more that one object',
                                 QMessageBox.Ok, QMessageBox.Ok)
            return None

        # VERIFY USER WANTS TO RENAME
        proceed = QMessageBox.question(self, 'Rename Files?', 'Are you sure you want to rename the selected files?',
                                       QMessageBox.Ok | QMessageBox.No, QMessageBox.Ok)

        if proceed == QMessageBox.Ok:
            for i, item in enumerate(checked_items):
                # GET THE CURRENT ITERATION / RENAMING NUMBER
                cur_num = i + get_num
                # GET THE CURRENT FILE NAME
                file_name = item.text()
                # CONFIGURE NAME
                the_new_name = self.configure_name(file_name, get_num)
                # CONFIGURE PATH TO OLD FILE
                old = os.path.join(base_dir, file_name)
                # DISPLAY PREVIEW
                if backup == 1:
                    # VALIDATE BACKUP DIRECTORY
                    directory = os.path.join(self.base_dir.text(), "quick_rename_backup")
                    if not os.path.isdir(directory):
                        os.mkdir(directory)
                    new = os.path.join(directory, file_name)
                    shutil.copy(old, new)
                # CONFIGURE PATH TO NEW FILE
                new = os.path.join(self.base_dir.text(), the_new_name)
                try:
                    os.rename(old, new)
                except:
                    pass
                get_num += 1

            self.get_files_from_selected_folder()


# MAIN PROGRAM
if __name__ == '__main__' :
    app = QApplication(sys.argv)
    gui = QuickRename()
    sys.exit(app.exec_())