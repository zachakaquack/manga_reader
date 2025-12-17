from dataclasses import dataclass


@dataclass
class Colors:
    # main
    main_background: str = "#1e1e1e"
    main_text: str = "#eeeeee"

    # reader
    reader_top_bar_background: str = "#303030"

    # side bar
    side_bar_top_bar_background: str = "#303030"
    side_bar_button_active_chapter: str = "#505050"

    # buttons
    button_background = "#404040"

    # bottom bar
    bottom_bar_background = "#303030"
    bottom_bar_filled_in = "#505050"
