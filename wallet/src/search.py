from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QScrollArea, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QLabel, QPlainTextEdit
import sqlite3
import datetime

name_days = {1: 'ПН', 2: 'ВТ', 3: 'СР', 4: 'ЧТ', 5: 'ПТ', 6: 'СБ', 7: 'ВС'}


class Search(QDialog):
    def __init__(self, result, func_delete=None, func_edit=None):
        super().__init__()
        # Словари объектов кнопок, где значением является информация о событии
        self.data_buttons_delete = None
        self.data_buttons_edit = None

        # Функции для удаления и изменения событий
        self.func_delete = func_delete
        self.func_edit = func_edit

        uic.loadUi('scripts/ui/list_events.ui', self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.result = result
        self.con = sqlite3.connect('scripts/db_calendar.sqlite')
        self.cur = self.con.cursor()
        self.display_events()

    def display_events(self):
        """Отображение событий"""
        self.data_buttons_edit = {}
        self.data_buttons_delete = {}
        layout = QVBoxLayout(self.content_widget)

        for value in self.result:
            date = value[0]
            start = value[1]
            end = value[2]
            title = value[3]
            id_event = value[4]
            des = value[5]
            main_widget = QWidget()
            row_layout = QHBoxLayout(main_widget)

            day = datetime.datetime(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
            current_day_of_week = day.weekday() + 1

            label_date = QLabel(date + '  ' + name_days[current_day_of_week])
            label_date.setMinimumSize(150, 31)
            label_date.setMaximumSize(150, 31)
            font = QFont("Times New Roman", 14)
            label_date.setFont(font)

            label_time_start = QLabel(start)
            label_time_start.setMinimumSize(41, 21)
            label_time_start.setMaximumSize(41, 21)
            font = QFont("Times New Roman", 14)
            label_time_start.setFont(font)
            label_time_start.setAlignment(Qt.AlignCenter)

            label = QLabel("—")
            label.setMinimumSize(16, 16)
            label.setMaximumSize(16, 16)
            font = QFont("14")
            label.setFont(font)

            label_time_end = QLabel(end)
            label_time_end.setMinimumSize(41, 21)
            label_time_end.setMaximumSize(41, 21)
            font = QFont("Times New Roman", 14)
            label_time_end.setFont(font)
            label_time_end.setAlignment(Qt.AlignCenter)

            title_line_edit = QLineEdit(title)
            title_line_edit.setReadOnly(True)
            title_line_edit.setMinimumSize(200, 21)
            title_line_edit.setMaximumSize(200, 21)
            font = QFont("Times New Roman", 14)
            title_line_edit.setFont(font)
            title_line_edit.setAlignment(Qt.AlignCenter)

            push_button_edit = QPushButton()
            push_button_edit.setToolTip('Редактировать событие')
            push_button_edit.setMinimumSize(31, 31)
            push_button_edit.setMaximumSize(31, 31)
            push_button_edit.setIconSize(QSize(35, 35))
            pixmap = QPixmap("scripts/img/edit.png")
            push_button_edit.setIcon(QIcon(pixmap))
            par = (start, end, date, title, des, id_event)
            self.data_buttons_edit[push_button_edit] = par
            push_button_edit.clicked.connect(self.edit_event)

            push_button_delete = QPushButton()
            push_button_delete.setToolTip('Удалить событие')
            push_button_delete.setMinimumSize(31, 31)
            push_button_delete.setMaximumSize(31, 31)
            push_button_delete.setIconSize(QSize(35, 35))
            pixmap = QPixmap("scripts/img/delete.png")
            push_button_delete.setIcon(QIcon(pixmap))
            self.data_buttons_delete[push_button_delete] = id_event
            push_button_delete.clicked.connect(self.delete_event)

            row_layout.addWidget(label_date)
            row_layout.addWidget(label_time_start)
            row_layout.addWidget(label)
            row_layout.addWidget(label_time_end)
            row_layout.addWidget(title_line_edit)
            row_layout.addWidget(push_button_edit)
            row_layout.addWidget(push_button_delete)

            layout.addWidget(main_widget)

    def edit_event(self):
        """Изменение выбранного события"""
        self.func_edit(self.data_buttons_edit)
        self.hide()

    def delete_event(self):
        """Удаление события"""
        self.func_delete(self.data_buttons_delete)
        self.hide()
