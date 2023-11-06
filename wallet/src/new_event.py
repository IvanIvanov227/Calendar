from PyQt5 import uic
from PyQt5.QtCore import QDate, QTime, Qt
from PyQt5.QtWidgets import QMessageBox, QDialog
import sqlite3


class NewEvent(QDialog):
    """Виджет для добавления нового события или его изменения"""
    def __init__(self, time_start, time_end, date, additional=None):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        uic.loadUi('scripts/ui/new_event.ui', self)
        # Начальное и конечное время события и его дата
        self.time_start = QTime(int(time_start.split(':')[0]), int(time_start.split(':')[1]))
        self.time_end = QTime(int(time_end.split(':')[0]), int(time_end.split(':')[1]))
        self.date = date
        # Если нужно изменить существующее событие, то в additional передаются дополнительные данные
        self.additional = additional
        if additional is not None:
            self.title = additional[0]
            self.description = additional[1]
            self.id_event = additional[2]
        self.start()
        self.con = sqlite3.connect('scripts/db_calendar.sqlite')
        self.cur = self.con.cursor()

    def start(self):
        """Стартовая функция"""
        # Связь кнопок с функциями
        self.SaveEdit.clicked.connect(self.save)
        self.timeEditStart.setMaximumTime(QTime(23, 30))
        self.timeEditEnd.setMaximumTime(QTime(23, 45))
        self.timeEditStart.timeChanged.connect(self.on_time_changed_start)
        self.timeEditEnd.timeChanged.connect(self.on_time_changed_end)

        # Установление в виджеты необходимых данных
        if self.additional is not None:
            self.titleEdit.setText(self.title)
            self.descriptionEdit.setPlainText(self.description)

        self.timeEditEnd.setTime(self.time_end)
        self.timeEditStart.setTime(self.time_start)

        date = QDate(int(self.date[:4]), int(self.date[5:7]), int(self.date[8:]))
        self.dateEdit.setDate(date)

    def on_time_changed_start(self):
        """Проверка на валидность веденного времени"""
        # Стартовое время должно быть МЕНЬШЕ конечного
        if self.timeEditStart.time() >= self.timeEditEnd.time():
            hour = self.timeEditStart.time().hour()
            minute = self.timeEditStart.time().minute() + 15
            if minute == 60:
                minute = 0
                hour += 1
            self.timeEditEnd.setTime(QTime(hour, minute))

        self.time_start = self.timeEditStart.time()

    def on_time_changed_end(self):
        """Проверка на валидность веденного времени"""
        # Стартовое время должно быть МЕНЬШЕ конечного
        if self.timeEditStart.time() >= self.timeEditEnd.time():
            self.timeEditEnd.setTime(self.time_end)
        else:
            self.time_end = self.timeEditEnd.time()

    def save(self):
        """Сохранение события"""
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
            # Добавление нового события
            if self.additional is None:
                string = 'INSERT INTO events(title, description, time_start, time_end, date) VALUES(?, ?, ?, ?, ?)'
                self.cur.execute(string, (title, description, time_start, time_end, date))
            # Изменение существующего события
            else:
                string = '''UPDATE events 
                SET title = ?, description = ?, time_start = ?, time_end = ?, date = ?
                WHERE id = ?'''
                self.cur.execute(string, (title, description, time_start, time_end, date, self.id_event))
            self.con.commit()
            self.hide()

    def closeEvent(self, event):
        """Проверка перед закрытием виджета"""
        msg_box = QMessageBox()
        msg_box.setText("Вы передумали создавать событие?")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Подтверждение")

        msg_box.addButton(QMessageBox.Yes)
        msg_box.addButton(QMessageBox.No)

        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
