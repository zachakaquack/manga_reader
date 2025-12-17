from dataclasses import dataclass


@dataclass
class SideBar:
    # GENERAL
    width: int = 250
    button_height: int = 50

    # COLORS
    background_color: str = "#303030"
