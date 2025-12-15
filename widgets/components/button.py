from PySide6.QtWidgets import QPushButton, QSizePolicy
from settings.loader import load_settings

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        settings = load_settings()

        self.setStyleSheet(
            f"""
            background-color: {settings.colors.button_background_color};
            color: {settings.colors.main_text_color};
            """
        )
