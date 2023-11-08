import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QColorDialog, QMessageBox


class Settings(QDialog):
    """Виджет настроек приложения"""
    def __init__(self):
        super().__init__()
        uic.loadUi('scripts/ui/settings.ui', self)
        self.commandButtonColorEvents.clicked.connect(self.update_color_events)
        self.commandButtonColorToday.clicked.connect(self.update_color_today)
        self.commandLinkButtonOffers.clicked.connect(self.add_offer)
        self.checkBoxEvent.clicked.connect(self.update_reminders)
        # Названия цветов для выделения событий и текущего дня
        self.color_events = None
        self.color_today = None
        # Напоминания
        self.reminders = False
        # Форма для добавления идей
        self.offers = None
        self.check()

    def add_offer(self):
        """Идеи по улучшению приложения"""
        self.offers = Offers()
        self.offers.exec_()

    def check(self):
        """Устанавливает галочку при необходимости"""
        with open('scripts/reminders.txt') as file:
            if file.read() == 'True':
                self.checkBoxEvent.setChecked(True)
            else:
                self.checkBoxEvent.setChecked(False)

    def update_color_events(self):
        # Получение цвета из файла для выделения событий
        color = QColorDialog.getColor()
        if color.isValid():
            with open('scripts/color_event.txt', 'w') as file:
                self.color_events = color.name()
                file.write(color.name())

    def update_color_today(self):
        # Получение цвета из файла для выделения текущего дня
        color = QColorDialog.getColor()
        if color.isValid():
            with open('scripts/color_today.txt', 'w') as file:
                self.color_today = color.name()
                file.write(color.name())

    def update_reminders(self):
        with open('scripts/reminders.txt', 'w') as file:
            self.reminders = self.checkBoxEvent.isChecked()
            file.write(str(self.checkBoxEvent.isChecked()))


class Offers(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('scripts/ui/offers.ui', self)
        self.pushButtonSave.clicked.connect(self.add_button)

    def add_button(self):
        plain_text = self.plainTextEdit.toPlainText()
        if plain_text == '':
            error_message = "Обязательно должен быть текст"
            QMessageBox.critical(self, "Ошибка", error_message, QMessageBox.Ok)
        else:
            con = sqlite3.connect('scripts/db_calendar.sqlite')
            cur = con.cursor()
            string = 'INSERT INTO offers(offer) VALUES(?)'
            cur.execute(string, (plain_text, ))
            con.commit()
            self.hide()
