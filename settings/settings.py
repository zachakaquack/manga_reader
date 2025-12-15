from dataclasses import dataclass, field

from settings.colors import Colors
from settings.reader import Reader

@dataclass
class Settings:
    # GENERAL
    reader: Reader = field(default_factory=Reader)
    colors: Colors = field(default_factory=Colors)
