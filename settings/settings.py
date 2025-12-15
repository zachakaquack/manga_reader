from dataclasses import dataclass, field

from settings.colors import Colors
from settings.reader import Reader
from settings.side_bar import SideBar

@dataclass
class Settings:
    # GENERAL
    reader: Reader = field(default_factory=Reader)
    side_bar: SideBar = field(default_factory=SideBar)
    colors: Colors = field(default_factory=Colors)
