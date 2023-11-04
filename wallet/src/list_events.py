from PyQt5.QtWidgets import QDialog, QWidget, QScrollArea, QVBoxLayout, QPushButton, QHBoxLayout, QLabel


class ListEvents(QDialog):
    def __init__(self, events, row, col):
        super().__init__()
        self.width = 600
        self.height = 400
        self.setGeometry(300, 300, self.width, self.height)
        self.setWindowTitle("Список событий")
        self.setFixedSize(self.width, self.height)
        self.events = events
        self.row = row
        self.day = col
        self.draw_events()

    def draw_events(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setGeometry(0, 0, self.width, self.height)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        layout = QVBoxLayout(content_widget)
        for day in self.events:
            if self.day == day:
                for key, value in self.events[day].items():
                    start = key
                    for events in value:
                        end = events[2]
                        title = events[0]
                        des = events[0]
                        id_event = events[3]
                        if int(start.split(':')[0]) <= self.row <= int(end.split(':')[0]):

                            row_widget = QWidget()
                            row_layout = QHBoxLayout(row_widget)

                            label_title = QLabel(title)
                            time_start_label = QLabel(start)
                            tire = QLabel('-')
                            time_end_label = QLabel(end)
                            button1 = QPushButton("Кнопка 1")
                            button2 = QPushButton("Кнопка 2")

                            row_layout.addWidget(label_title)
                            row_layout.addWidget(time_start_label)
                            row_layout.addWidget(tire)
                            row_layout.addWidget(time_end_label)
                            row_layout.addWidget(button1)
                            row_layout.addWidget(button2)

                            layout.addWidget(row_widget)
