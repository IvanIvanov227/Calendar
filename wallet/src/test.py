import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QMessageBox, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Диалог с дополнительными кнопками")

        layout = QVBoxLayout()

        # Создаем кнопку со значком вопросительного знака
        question_button = QPushButton("Кнопка с вопросительным знаком")
        question_icon = self.style().standardIcon(QStyle.SP_MessageBoxQuestion)
        question_button.setIcon(question_icon)
        question_button.clicked.connect(self.showQuestionMessage)
        layout.addWidget(question_button)

        # Добавляем дополнительные кнопки
        custom_button1 = QPushButton("Кнопка 1")
        custom_button1.clicked.connect(self.customButtonClicked1)
        layout.addWidget(custom_button1)

        custom_button2 = QPushButton("Кнопка 2")
        custom_button2.clicked.connect(self.customButtonClicked2)
        layout.addWidget(custom_button2)

        self.setLayout(layout)

    def customButtonClicked1(self):
        print("Кнопка 1 была нажата")

    def customButtonClicked2(self):
        print("Кнопка 2 была нажата")

    def showQuestionMessage(self):
        print("Кнопка со значком вопросительного знака была нажата")
        QMessageBox.information(self, "Информация", "Справочное сообщение с вопросом")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.exec_()
    sys.exit(app.exec_())