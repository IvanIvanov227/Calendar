import sys
from PyQt5.QtWidgets import QApplication
from main_window import Calendar

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    calendar = Calendar()
    calendar.show()
    sys.exit(app.exec())
