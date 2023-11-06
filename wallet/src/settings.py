from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QColorDialog


class Settings(QDialog):
    """Виджет настроек приложения"""
    def __init__(self):
        super().__init__()
        uic.loadUi('scripts/ui/settings.ui', self)
        self.commandButtonColorEvents.clicked.connect(self.update_color_events)
        self.commandButtonColorToday.clicked.connect(self.update_color_today)
        # Названия цветов для выделения событий и текущего дня
        self.color_events = None
        self.color_today = None

    def update_color_events(self):
        # Получение цвета из файла для выделения событий
        color = QColorDialog.getColor()
        if color.isValid():
            with open('scripts/color_event.txt', 'w') as file:
                self.color_events = color.name()
                file.write(color.name())

    def update_color_today(self):
        # Получение цвета из файла для выделения текущего дня
        color = QColorDialog.getColor()
        if color.isValid():
            with open('scripts/color_today.txt', 'w') as file:
                self.color_today = color.name()
                file.write(color.name())
