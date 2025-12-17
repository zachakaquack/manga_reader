from dataclasses import dataclass


@dataclass
class SideBar:
    # GENERAL
    width: int = 250
    button_height: int = 50
    arrow_button_fixed_width: int = 32

    # COLORS
    background_color: str = "#303030"
