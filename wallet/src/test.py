import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox


class ComboBoxWithScroll(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('ComboBox with Scroll')

        combo = QComboBox(self)
        combo.setGeometry(50, 50, 200, 30)

        combo.addItem("Option 1")
        combo.addItem("Option 2")
        combo.addItem("Option 3")
        combo.addItem("Option 4")
        combo.addItem("Option 5")
        combo.addItem("Option 1")
        combo.addItem("Option 2")
        combo.addItem("Option 3")
        combo.addItem("Option 4")
        combo.addItem("Option 5")
        combo.addItem("Option 1")
        combo.addItem("Option 2")
        combo.addItem("Option 3")
        combo.addItem("Option 4")
        combo.addItem("Option 5")

        combo.setMaxVisibleItems(5)  # Установите максимальное количество видимых элементов

        combo.view().setVerticalScrollBarPolicy(2)  # Настройте полосу прокрутки


def main():
    app = QApplication(sys.argv)
    ex = ComboBoxWithScroll()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
