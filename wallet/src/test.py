import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox, QVBoxLayout


class MyInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Мое диалоговое окно")
        layout = QVBoxLayout()

        self.help_button = QPushButton('Помощь', self)
        layout.addWidget(self.help_button)

        self.help_button.clicked.connect(self.showHelp)

    def showHelp(self):
        # Ваш код для открытия окна справки или выполнения других действий
        QMessageBox.information(self, "Справка", "Это окно с контекстной справкой")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyInputDialog()
    ex.exec_()
    sys.exit(app.exec_())
