from PyQt5 import uic
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QMessageBox, QDialog
import sqlite3


class NewEvent(QDialog):
    def __init__(self, time_start, time_end, date):
        super().__init__()
        uic.loadUi('scripts/ui/new_event.ui', self)
        self.SaveEdit.clicked.connect(self.save)
        self.time_start = QTime(int(time_start.split(':')[0]), int(time_start.split(':')[1]))
        self.time_end = QTime(int(time_end.split(':')[0]), int(time_end.split(':')[1]))
        self.times = []
        self.date = date
        self.start()
        self.timeEditStart.setMaximumTime(QTime(23, 30))
        self.timeEditEnd.setMaximumTime(QTime(23, 45))
        self.timeEditStart.timeChanged.connect(self.on_time_changed_start)
        self.timeEditEnd.timeChanged.connect(self.on_time_changed_end)
        self.con = sqlite3.connect('scripts/db_calendar.sqlite')
        self.cur = self.con.cursor()

    def start(self):
        self.timeEditStart.setTime(self.time_start)
        self.timeEditEnd.setTime(self.time_end)
        date = QDate(int(self.date[:4]), int(self.date[5:7]), int(self.date[8:]))
        self.dateEdit.setDate(date)

    def on_time_changed_start(self):
        if self.timeEditStart.time() >= self.timeEditEnd.time():
            hour = self.timeEditStart.time().hour()
            minute = self.timeEditStart.time().minute() + 15
            if minute == 60:
                minute = 0
                hour += 1
            self.timeEditEnd.setTime(QTime(hour, minute))

        self.time_start = self.timeEditStart.time()

    def on_time_changed_end(self):
        if self.timeEditStart.time() >= self.timeEditEnd.time():
            self.timeEditEnd.setTime(self.time_end)
        else:
            self.time_end = self.timeEditEnd.time()

    def save(self):
        title = self.titleEdit.text()
        description = self.descriptionEdit.toPlainText()
        if len(description) == 0:
            description = None
        hour_start = self.timeEditStart.time().hour()
        hour_end = self.timeEditEnd.time().hour()
        minute_start = self.timeEditStart.time().minute()
        minute_end = self.timeEditEnd.time().minute()
        time_start = f'{"0" if hour_start < 10 else ""}{hour_start}:{"0" if minute_start < 10 else ""}{minute_start}'
        time_end = f'{"0" if hour_end < 10 else ""}{hour_end}:{"0" if minute_end < 10 else ""}{minute_end}'
        date = self.dateEdit.date().toString('yyyy-MM-dd')
        if len(title) == 0:
            error_message = "Обязательно должно быть название!"
            QMessageBox.critical(self, "Ошибка", error_message, QMessageBox.Ok)
        else:
            string = 'INSERT INTO events(title, description, time_start, time_end, date) VALUES(?, ?, ?, ?, ?)'
            self.cur.execute(string, (title, description, time_start, time_end, date))
            self.con.commit()
            self.hide()
