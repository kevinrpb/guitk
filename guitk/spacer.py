"""Spacer class that expands to fill space in the layout"""

from __future__ import annotations

import tkinter as tk

from .ttk_label import Label
from .frame import Frame
from .types import Window
from .layout import get_parent

__all__ = ["Spacer", "VerticalSpacer"]


class Spacer(Label):
    """Spacer widget that expands to fill the horizontal space in the layout"""

    def __init__(self):
        super().__init__(
            "",
            padding=0,
            disabled=True,
            sticky="nsew",
            autoframe=False,
        )

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        parent.grid_columnconfigure(col, weight=1)

class VerticalSpacer(Label):
    """ "Spacer widget that expands to fill the vertical space in the layout"""

    def __init__(self):
        super().__init__(
            "",
            padding=0,
            disabled=True,
            sticky="nsew",
            autoframe=False,
        )

    def _create_widget(self, parent: tk.BaseWidget, window: Window, row: int, col: int):
        super()._create_widget(parent, window, row, col)
        parent.grid_rowconfigure(row, weight=1)