# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
# from PyQt5.QtGui import QColor, QPainter, QPen
# from PyQt5.QtCore import Qt
#
#
#
# class CustomTableWidget(QTableWidget):
#     def __init__(self):
#         super().__init__()
#
#     def paintEvent(self, event):
#         #super().paintEvent(event)
#         painter = QPainter(self.viewport())
#         painter.setPen(QPen(Qt.red, 4))
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


# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.tableWidget = QTableWidget(self)
#         self.tableWidget.setRowCount(5)
#         self.tableWidget.setColumnCount(5)
#
#         for row in range(5):
#             for col in range(5):
#                 item = QTableWidgetItem(f"Row {row}, Col {col}")
#                 self.tableWidget.setItem(row, col, item)
#
#         self.setCentralWidget(self.tableWidget)
#
#         # Выбрать ячейку в строке 2 и столбце 3
#         self.tableWidget.setCurrentCell(2, 3)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())
from tzlocal import get_localzone
import datetime
import pytz

local_tz = str(get_localzone())
tz = pytz.timezone(local_tz)
current_time = datetime.datetime.now(tz)

print(current_time)
