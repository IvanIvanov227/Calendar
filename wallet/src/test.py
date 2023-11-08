# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
# from PyQt5.QtGui import QColor, QPainter
# from PyQt5.QtCore import Qt
#
# class CustomTableWidget(QTableWidget):
#     def __init__(self):
#         super().__init__()
#
#     def paintEvent(self, event):
#         super().paintEvent(event)
#         painter = QPainter(self.viewport())
#         painter.setPen(Qt.red)
#         painter.drawLine(20, 30, 90, 30)  # Пример: рисование красной линии
#
# app = QApplication(sys.argv)
#
# window = QMainWindow()
# table_widget = CustomTableWidget()
# window.setCentralWidget(table_widget)
#
# table_widget.setColumnCount(4)
# table_widget.setRowCount(4)
#
# table_widget.setItem(1, 1, QTableWidgetItem("Cell Content"))
#
# window.show()
#
# sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, QTime

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Обновление времени")

layout = QVBoxLayout()

# Создаем виджет для отображения времени
time_label = QLabel()
layout.addWidget(time_label)

def update_time():
    current_time = QTime.currentTime()
    time_label.setText(current_time.toString("hh:mm:ss"))

# Создаем QTimer и соединяем его со слотом для обновления времени
timer = QTimer()
timer.timeout.connect(update_time)
timer.start(60000)  # Обновление каждую минуту (60 000 миллисекунд)

# Инициализируем время
update_time()

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
