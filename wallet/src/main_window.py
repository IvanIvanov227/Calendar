import os
from PyQt5 import uic
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QTableWidget
from PyQt5.QtGui import QColor
import datetime
from new_event import NewEvent
from settings import Settings
from list_events import ListEvents
import sqlite3

months = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
          7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
          }
name_days = {1: 'ПН', 2: 'ВТ', 3: 'СР', 4: 'ЧТ', 5: 'ПТ', 6: 'СБ', 7: 'ВС'}


class Calendar(QMainWindow):
    def __init__(self):
        super().__init__()
        os.chdir('..')
        self.list_events = None
        self.title = None
        self.settings_widget = None
        self.event = None
        self.color_today = None
        self.color_events = None
        self.set_colors_settings()
        self.dict_dates = {}
        self.list_dates_events = {}
        self.current_days = []
        self.paint_events = []

        uic.loadUi('scripts/ui/main_ui.ui', self)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.settingsButton.clicked.connect(self.settings)
        self.calendarWidget.selectionChanged.connect(self.on_calendar_selection_changed)
        self.tableWidget.cellClicked.connect(self.table_clicked)
        self.todayButton.clicked.connect(self.start)


        self.todayButton.setToolTip('Это подсказка для виджета')


        self.leftButton.clicked.connect(self.new_week)
        self.rightButton.clicked.connect(self.new_week)
        self.start()

    def set_colors_settings(self):
        with open('scripts/color_event.txt') as file:
            self.color_events = file.read()
            if self.color_events == '':
                self.color_events = QColor(0, 0, 255)

        with open('scripts/color_today.txt') as file2:
            self.color_today = file2.read()
            if self.color_today == '':
                self.color_today = QColor(255, 0, 0)

    def start(self):
        # Текущая дата
        today = datetime.date.today()
        # Номер дня в текущей неделе
        current_day_of_week = today.weekday()
        # Дата начального дня недели
        start_of_week = today - datetime.timedelta(days=current_day_of_week)
        date = QDate(today)
        self.calendarWidget.setSelectedDate(date)
        self.update_table(start_of_week)
        self.title_date_label()

    def table_clicked(self, row, col):
        if col != 0:
            flag = False
            for i in self.paint_events:
                if col == i[0] and i[1] <= row < i[2]:
                    flag = True
                    break
            if flag:
                self.list_events = ListEvents(self.dict_dates, row, self.current_days[col - 1])
                self.list_events.exec_()
            else:
                time_start = self.tableWidget.item(row, 0).text()
                time_end = time_start[:2] + ':' + str(int(time_start[3:]) + 30)
                date = self.current_days[col - 1]
                self.event = NewEvent(time_start, time_end, date)
                self.event.setModal(True)
                self.event.exec_()
                self.data_to_table()

    def new_week(self):
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
        self.settings_widget = Settings()
        self.settings_widget.setModal(True)
        self.settings_widget.exec_()
        if self.settings_widget.color_events is not None:
            self.color_events = self.settings_widget.color_events
        if self.settings_widget.color_today is not None:
            self.color_today = self.settings_widget.color_today
        self.draw_events()
        self.draw_color_today()

    def on_calendar_selection_changed(self):
        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        current_day_of_week = date.weekday()
        start_of_week = date - datetime.timedelta(days=current_day_of_week)
        self.update_table(start_of_week)
        self.title_date_label()

    def update_table(self, start_of_week):
        self.current_days.clear()
        # Даты дней выбранной недели
        for i in range(7):
            current_day = start_of_week + datetime.timedelta(days=i)
            self.current_days.append(current_day.strftime("%Y-%m-%d"))
        # Заголовок таблицы
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
        # Закрашивание ячейки с текущим днём
        today = datetime.date.today()
        if str(today) in self.current_days:
            current_day_of_week = self.current_days.index(today.strftime("%Y-%m-%d")) + 1
            header_item = QTableWidgetItem(self.title[current_day_of_week])
            header_item.setBackground(QColor(self.color_today))
            self.tableWidget.setHorizontalHeaderItem(current_day_of_week, header_item)
        else:
            for i in range(7):
                self.tableWidget.horizontalHeaderItem(i).setBackground(QColor(255, 255, 255))

    def data_to_table(self):
        con = sqlite3.connect('scripts/db_calendar.sqlite')
        cur = con.cursor()
        string = 'SELECT date, time_start, time_end, title, description, id FROM events'
        self.dict_dates = {}
        result = cur.execute(string).fetchall()
        for date in result:
            date_event = date[0]
            start = date[1]
            end = date[2]
            title = date[3]
            des = date[4]
            id_event = date[5]
            if date_event in self.current_days:
                if date_event in self.dict_dates:
                    if start in self.dict_dates[date_event]:
                        self.dict_dates[date_event][start].append([title, des, end, id_event])
                    else:
                        self.dict_dates[date_event][start] = [[title, des, end, id_event]]
                else:
                    self.dict_dates[date_event] = {start: [[title, des, end, id_event]]}
        self.draw_events()

    def draw_events(self):
        for day in self.dict_dates:
            col = self.current_days.index(day) + 1
            for key, value in self.dict_dates[day].items():
                start = int(key.split(':')[0])
                for events in value:
                    end = int(events[2].split(':')[0])
                    minute_end = int(events[2].split(':')[1])
                    if minute_end > 0:
                        end += 1
                    self.paint_events.append([col, start, end])
                    self.paint_for_table(col, start, end)

    def paint_for_table(self, col, start, end):
        for i in range(start, end):
            item = QTableWidgetItem()
            item.setBackground(QColor(self.color_events))
            self.tableWidget.setItem(i, col, item)
