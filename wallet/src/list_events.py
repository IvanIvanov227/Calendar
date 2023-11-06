from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QDialog, QWidget, QScrollArea, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QPlainTextEdit, QMessageBox, QLineEdit

from new_event import NewEvent
import sqlite3


class ListEvents(QDialog):
    """Виджет со списком событий"""
    def __init__(self, events, row, day, func_delete=None, func_edit=None):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Форма для добавления нового события
        self.event = None
        # Словарь, ключ - объект кнопки, значение - информация об это событии
        self.data_buttons_edit = None
        # Словарь, ключ - объект кнопки, значение - id события
        self.data_buttons_delete = None

        # Функции для удаления и изменения событий
        self.func_delete = func_delete
        self.func_edit = func_edit

        self.width = 800
        self.height = 400
        self.setGeometry(300, 300, self.width, self.height)
        self.setWindowTitle("Список событий")
        self.setFixedSize(self.width, self.height)
        # Данные о событиях
        self.events = events
        # Номер записи и день выбранного события
        self.row = row
        self.day = day
        self.con = sqlite3.connect('scripts/db_calendar.sqlite')
        self.cur = self.con.cursor()
        self.draw_events()

    def draw_events(self):
        """Отображение списка событий"""
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setGeometry(0, 0, self.width, self.height)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        self.data_buttons_edit = {}
        self.data_buttons_delete = {}
        layout = QVBoxLayout(content_widget)

        button = QPushButton('Добавить событие')
        font = QFont("Times New Roman", 12)
        button.setFont(font)
        button.clicked.connect(self.add_event)
        layout.addWidget(button)

        for key, value in self.events.items():
            start = key
            for events in value:
                end = events[2]
                title = events[0]
                des = events[1]
                id_event = events[3]
                if int(start.split(':')[0]) <= self.row <= int(end.split(':')[0]):
                    main_widget = QWidget()
                    row_layout = QHBoxLayout(main_widget)

                    label_title = QLineEdit(title)
                    label_title.setReadOnly(True)
                    label_title.setMinimumSize(201, 31)
                    label_title.setMaximumSize(201, 31)
                    font = QFont("Times New Roman", 14)
                    label_title.setFont(font)

                    if des is None:
                        plain_text = QLabel('Описания нет')
                        plain_text.setMinimumSize(201, 21)
                        plain_text.setMaximumSize(201, 21)
                        font = QFont("Times New Roman", 12)
                        plain_text.setFont(font)
                        plain_text.setAlignment(Qt.AlignCenter)
                    else:
                        plain_text = QPlainTextEdit()
                        plain_text.setReadOnly(True)
                        plain_text.setPlainText(des)
                        plain_text.setMinimumSize(200, 81)
                        plain_text.setMaximumSize(200, 81)
                        font = QFont("Times New Roman", 12)
                        plain_text.setFont(font)

                    label_time_start = QLabel(start)
                    label_time_start.setMinimumSize(41, 21)
                    label_time_start.setMaximumSize(41, 21)
                    font = QFont("Times New Roman", 12)
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
                    font = QFont("Times New Roman", 12)
                    label_time_end.setFont(font)
                    label_time_end.setAlignment(Qt.AlignCenter)

                    push_button_edit = QPushButton()
                    push_button_edit.setMinimumSize(31, 31)
                    push_button_edit.setMaximumSize(31, 31)
                    push_button_edit.setIconSize(QSize(35, 35))
                    pixmap = QPixmap("scripts/img/edit.png")
                    push_button_edit.setIcon(QIcon(pixmap))
                    par = (start, end, self.day, title, des, id_event)
                    self.data_buttons_edit[push_button_edit] = par
                    push_button_edit.clicked.connect(self.edit_event)

                    push_button_delete = QPushButton()
                    push_button_delete.setMinimumSize(31, 31)
                    push_button_delete.setMaximumSize(31, 31)
                    pixmap = QPixmap("scripts/img/delete.png")
                    push_button_delete.setIcon(QIcon(pixmap))
                    push_button_delete.setIconSize(QSize(35, 35))
                    self.data_buttons_delete[push_button_delete] = id_event
                    push_button_delete.clicked.connect(self.delete_event)

                    row_layout.addWidget(label_title)
                    row_layout.addWidget(plain_text)
                    row_layout.addWidget(label_time_start)
                    row_layout.addWidget(label)
                    row_layout.addWidget(label_time_end)
                    row_layout.addWidget(push_button_edit)
                    row_layout.addWidget(push_button_delete)

                    layout.addWidget(main_widget)

    def add_event(self):
        """Добавление события"""
        start = f'{"0" if self.row < 10 else ""}{self.row}:00'
        end = start.split(':')[0] + ':' + str(int(start.split(':')[1]) + 15)
        self.hide()
        self.event = NewEvent(start, end, self.day)
        self.event.exec_()

    def edit_event(self):
        """Изменение события"""
        self.func_edit(self.data_buttons_edit)
        self.hide()

    def delete_event(self):
        # Удаление события
        self.func_delete(self.data_buttons_delete)
        self.hide()
