import os

from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt, QDate, QTime, QTimer
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QTableWidget, QInputDialog, QMessageBox
from PyQt5.QtGui import QColor
import datetime

from tzlocal import get_localzone
import pytz
from new_event import NewEvent
from settings import Settings
from list_events import ListEvents
import sqlite3
from search import Search
from PyQt5.QtWinExtras import QtWin


months = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
          7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
          }
name_days = {1: 'ПН', 2: 'ВТ', 3: 'СР', 4: 'ЧТ', 5: 'ПТ', 6: 'СБ', 7: 'ВС'}


class Calendar(QMainWindow):
    """Главный виджет приложения"""
    def __init__(self):
        super().__init__()
        os.chdir('..')
        # Форма для поиска событий по названию
        self.search_widget = None
        # Форма для просмотра событий
        self.list_events_widget = None
        # Заголовок таблицы
        self.title = None
        # Форма для настроек
        self.settings_widget = None
        # Форма для добавления события
        self.event_widget = None
        # Цвет для выделения заголовка с текущим днём
        self.color_today = None
        # Цвет для выделения событий
        self.color_events = None
        # Напоминания
        self.reminders = None
        # Часовой пояс пользователя
        self.tz = None
        # Данные о событии
        self.data_for_events = {}
        # Даты дней выбранной недели
        self.current_days = []
        # Ячейки с событиями
        self.paint_events = []
        uic.loadUi('scripts/ui/main_ui.ui', self)
        self.setWindowIcon(QtGui.QIcon('scripts/img/calendar.png'))
        try:
            my_app_id = 'mycompany.myproduct.subproduct.version'
            QtWin.setCurrentProcessExplicitAppUserModelID(my_app_id)
        except ImportError:
            pass
        self.con = sqlite3.connect('../scripts/db_calendar.sqlite')
        self.cur = self.con.cursor()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.set_colors_settings()
        self.is_reminder()
        self.hints()
        self.clicks()
        self.start()
        self.timer()

    def hints(self):
        """Установление подсказок для виджетов"""
        self.todayButton.setToolTip('Перейти на текущую неделю')
        self.leftButton.setToolTip('Перейти на предыдущую неделю')
        self.rightButton.setToolTip('Перейти на следующую неделю')
        self.settingsButton.setToolTip('Настройки')
        self.searchButton.setToolTip('Поиск событий')

    def timer(self):
        """Обновление времени"""
        current_time = QTime.currentTime().toString("hh:mm")
        self.current_time.setText(current_time)

        timer = QTimer(self)
        timer.timeout.connect(self.update_current_time)
        timer.start(1000)
        timer2 = QTimer(self)
        timer2.timeout.connect(self.update_reminders)
        timer2.start(60000)

    def update_current_time(self):
        """Обновляет значение виджета current_time с текущим временем"""
        current_time = QTime.currentTime().toString("hh:mm")
        self.current_time.setText(current_time)

    def update_reminders(self):
        """Проверка событий"""
        if self.reminders:
            today = str(datetime.datetime.now(tz=self.tz).date())
            list_events = []
            if self.data_for_events:
                for start in self.data_for_events[today]:
                    if start == self.current_time.text():
                        list_events.append(self.data_for_events[today][start])
            if len(list_events) != 0:
                self.set_reminder(list_events)

    def set_reminder(self, list_events):
        """Напоминание"""
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle("Напоминание")
        string = f'В {self.current_time.text()} у вас:\n\n '
        if len(list_events) == 1:
            list_events = list_events[0]
        for i in list_events:
            title = i[0]
            end = i[2]
            string += f'- {title} до {end}\n'
        message_box.setText(string)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    def clicks(self):
        """Установление связей виджетов с функциями"""
        self.settingsButton.clicked.connect(self.settings)
        self.searchButton.clicked.connect(self.search)
        self.calendarWidget.selectionChanged.connect(self.on_calendar_selection_changed)
        self.tableWidget.cellClicked.connect(self.table_clicked)
        self.todayButton.clicked.connect(self.start)
        self.leftButton.clicked.connect(self.new_week)
        self.rightButton.clicked.connect(self.new_week)

    def set_colors_settings(self):
        """Получение цветов из файлов"""
        with open('../scripts/color_event.txt') as file:
            self.color_events = file.read()
            if self.color_events == '':
                self.color_events = QColor(0, 0, 255)

        with open('../scripts/color_today.txt') as file2:
            self.color_today = file2.read()
            if self.color_today == '':
                self.color_today = QColor(255, 0, 0)

    def is_reminder(self):
        """Узнаёт о необходимости передавать напоминания"""
        with open('../scripts/reminders.txt') as file:
            string = file.read()
            if string == 'True':
                self.reminders = True
            else:
                self.reminders = False

    def start(self):
        """Стартовая функция"""
        local_tz = str(get_localzone())
        self.tz = pytz.timezone(local_tz)

        # Текущая дата
        today = datetime.datetime.now(tz=self.tz).date()
        # Номер дня в текущей неделе
        current_day_of_week = today.weekday()
        # Дата начального дня недели
        start_of_week = today - datetime.timedelta(days=current_day_of_week)
        date = QDate(today)
        self.calendarWidget.setSelectedDate(date)
        self.update_table(start_of_week)
        self.title_date_label()

    def table_clicked(self, row, col):
        """Обрабатывание нажатия на таблицу"""
        if col != 0:
            flag = False
            # Узнаём, есть ли в нажатой ячейке событие
            for i in self.paint_events:
                if col == i[0] and i[1] <= row < i[2]:
                    flag = True
                    break
            # Если есть, то создаём виджет со списком событий в данной ячейке
            if flag:
                par = (self.data_for_events[self.current_days[col - 1]], row, self.current_days[col - 1])
                self.list_events_widget = ListEvents(*par, func_delete=self.delete_event, func_edit=self.edit_event)
                self.list_events_widget.exec_()
            # Если нет, то создаём виджет для добавления события
            else:
                time_start = self.tableWidget.item(row, 0).text()
                time_end = time_start[:2] + ':' + str(int(time_start[3:]) + 30)
                date = self.current_days[col - 1]
                self.event_widget = NewEvent(time_start, time_end, date)
                self.event_widget.setModal(True)
                self.event_widget.exec_()
            # Обновляем данные о событиях
            self.data_to_table()

    def delete_event(self, data_buttons_delete):
        """Удаление события"""
        id_event = data_buttons_delete[self.sender()]
        msg_box = QMessageBox()
        msg_box.setText("Вы уверены, что хотите удалить запись?")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Подтверждение")

        msg_box.addButton(QMessageBox.Yes)
        msg_box.addButton(QMessageBox.No)

        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            string = 'DELETE FROM events WHERE id = ?'
            self.cur.execute(string, (id_event, ))

        self.con.commit()

    def edit_event(self, data_buttons_edit):
        """Изменение события"""
        par = data_buttons_edit[self.sender()]
        time_start = par[0]
        time_end = par[1]
        date = par[2]
        title = par[3]
        description = par[4]
        id_event = par[5]
        self.event_widget = NewEvent(time_start, time_end, date, additional=[title, description, id_event])
        self.event_widget.setModal(True)
        self.event_widget.exec_()

    def new_week(self):
        """Переход на следующую или на предыдущую неделю"""
        date_string = self.current_days[0]
        day = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
        if self.sender().text() == '←':
            one_week_ago = day - datetime.timedelta(days=7)
        else:
            one_week_ago = day + datetime.timedelta(days=7)
        date = QDate(one_week_ago)
        self.calendarWidget.setSelectedDate(date)
        self.update_table(one_week_ago)
        self.title_date_label()

    def title_date_label(self):
        """Установление месяца и года выбранной недели"""
        title_months, title_years = list(), list()
        for i in self.current_days:
            if months[int(i.split('-')[1])] not in title_months:
                title_months.append(months[int(i.split('-')[1])])
            if i.split('-')[0] not in title_years:
                title_years.append(i.split('-')[0])
        label_string = title_months.pop()
        if len(title_months) > 0:
            label_string = title_months.pop() + ' - ' + label_string
        title_years = sorted(title_years, reverse=True)
        label_string += '\n' + title_years.pop()
        if len(title_years) > 0:
            label_string += ' - ' + title_years.pop()

        self.date_label.setText(label_string)

    def settings(self):
        """Открытие виджета с настройками приложения"""
        self.settings_widget = Settings()
        self.settings_widget.setModal(True)
        self.settings_widget.exec_()
        if self.settings_widget.color_events is not None:
            self.color_events = self.settings_widget.color_events
        if self.settings_widget.color_today is not None:
            self.color_today = self.settings_widget.color_today
        self.reminders = self.settings_widget.reminders

        self.draw_events()
        self.draw_color_today()

    def on_calendar_selection_changed(self):
        """Выбор пользователем даты в виджете календаря"""
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        current_day_of_week = date.weekday()
        start_of_week = date - datetime.timedelta(days=current_day_of_week)
        self.update_table(start_of_week)
        self.title_date_label()

    def update_table(self, start_of_week):
        """Обновление заголовка таблицы и её записей"""
        self.current_days.clear()

        # Даты дней выбранной недели
        for i in range(7):
            current_day = start_of_week + datetime.timedelta(days=i)
            self.current_days.append(current_day.strftime("%Y-%m-%d"))

        self.title = [' '] + [f"{name_days[i + 1]}\n{int(self.current_days[i].split('-')[-1])}" for i in range(7)]

        # Скрываем нумерацию строк
        header = self.tableWidget.verticalHeader()
        header.setVisible(False)

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(self.title)

        # Растягиваем колонки на весь виджет
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Отображение часов
        for i in range(24):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            item = QTableWidgetItem(f'{"0" if i < 10 else ""}{i}:00')
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(item))
        self.draw_color_today()
        self.data_to_table()

    def draw_color_today(self):
        """Закрашивание ячейки с текущим днём"""
        today = datetime.datetime.now(tz=self.tz).date()
        if str(today) in self.current_days:
            current_day_of_week = self.current_days.index(today.strftime("%Y-%m-%d")) + 1
            header_item = QTableWidgetItem(self.title[current_day_of_week])
            header_item.setBackground(QColor(self.color_today))
            self.tableWidget.setHorizontalHeaderItem(current_day_of_week, header_item)
        else:
            for i in range(7):
                self.tableWidget.horizontalHeaderItem(i).setBackground(QColor(255, 255, 255))

    def data_to_table(self):
        """Обновление данных о событиях"""
        string = 'SELECT date, time_start, time_end, title, description, id FROM events'
        self.data_for_events = {}
        result = self.cur.execute(string).fetchall()
        for date in result:
            date_event = date[0]
            start = date[1]
            end = date[2]
            title = date[3]
            des = date[4]
            id_event = date[5]
            if date_event in self.current_days:
                if date_event in self.data_for_events:
                    if start in self.data_for_events[date_event]:
                        self.data_for_events[date_event][start].append([title, des, end, id_event])
                    else:
                        self.data_for_events[date_event][start] = [[title, des, end, id_event]]
                else:
                    self.data_for_events[date_event] = {start: [[title, des, end, id_event]]}
        self.draw_events()

    def draw_events(self):
        """Получение ячеек таблицы с событиями"""
        self.paint_events.clear()
        for i in range(24):
            for j in range(1, 8):
                item = QTableWidgetItem()
                item.setBackground(QColor(255, 255, 255))
                self.tableWidget.setItem(i, j, item)

        for day in self.data_for_events:
            col = self.current_days.index(day) + 1
            for key, value in self.data_for_events[day].items():
                start = int(key.split(':')[0])
                for events in value:
                    end = int(events[2].split(':')[0])
                    minute_end = int(events[2].split(':')[1])
                    if minute_end > 0:
                        end += 1
                    self.paint_events.append([col, start, end])
                    self.paint_for_table(col, start, end)

    def paint_for_table(self, col, start, end):
        """Закрашивание ячеек с событиями"""
        for i in range(start, end):
            item = QTableWidgetItem()
            item.setBackground(QColor(self.color_events))
            self.tableWidget.setItem(i, col, item)

    def search(self):
        """Виджет для поиска событий по названию"""
        dialog = QInputDialog()
        title, ok_pressed = dialog.getText(self, "Введите название события",
                                           "Как называется событие?")
        if ok_pressed:
            string = 'SELECT date, time_start, time_end, title, id, description FROM events WHERE title = ?'
            result = self.cur.execute(string, (title,)).fetchall()
            if len(result) == 0:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Information)
                message_box.setWindowTitle("Информация")
                message_box.setText("Событий с данным названием не нашлось")
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec()
            else:
                self.search_widget = Search(result, func_delete=self.delete_event, func_edit=self.edit_event)
                self.search_widget.exec_()
                self.data_to_table()
