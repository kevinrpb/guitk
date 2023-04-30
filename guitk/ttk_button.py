"""ttk Button widgets"""

import pathlib
import tkinter.ttk as ttk
from tkinter import filedialog
from typing import Any, Hashable

from .events import Event, EventCommand, EventType
from .types import CommandType, TooltipType, Window
from .widget import Widget

__all__ = ["Button", "BrowseFileButton", "BrowseDirectoryButton"]

_valid_standard_attributes = {
    "class",
    "compound",
    "cursor",
    "image",
    "state",
    "style",
    "takefocus",
    "text",
    "textvariable",
    "underline",
    "width",
}

_valid_ttk_button_attributes = {
    "command",
    "default",
    "width",
} | _valid_standard_attributes


_valid_askopenfile_options = {
    "defaultextension",
    "filetypes",
    "initialfile",
    "title",
}


class Button(Widget):
    """Basic button"""

    def __init__(
        self,
        text: str,
        key: Hashable | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        command: CommandType | None = None,
        **kwargs,
    ):
        """
        Initialize a Button widget.

        Args:
            text (str): Text for the button.
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (int | None, optional): X padding. Defaults to None.
            pady (int | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            command (CommandType | None, optional): Command callback. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Button.
        """
        super().__init__(
            key=key,
            disabled=disabled,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
            command=command,
            **kwargs,
        )

        self.widget_type = "ttk.Button"
        self.text = text
        self.key = key or text
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.tooltip = tooltip
        self.padx = padx
        self.pady = pady
        self.kwargs = kwargs

    @property
    def value(self) -> str:
        return self.widget["text"]

    @value.setter
    def value(self, text: str):
        self.widget["text"] = text

    def _create_widget(self, parent: Any, window: Window, row: int, col: int):
        self.window = window
        self._parent = parent
        event = Event(self, window, self.key, EventType.ButtonPress)

        # build arg list for Button()
        kwargs_button = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_button_attributes
        }

        self.widget = ttk.Button(
            parent,
            text=self.text,
            command=window._make_callback(event),
            **kwargs_button,
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )

        if self._command:
            self.events = True
            window._bind_command(
                EventCommand(
                    widget=self,
                    key=self.key,
                    event_type=EventType.ButtonPress,
                    command=self._command,
                )
            )

        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def button(self):
        """Return the Tk button widget"""
        return self.widget


class BrowseFileButton(Button):
    """
    Button that opens a file dialog to select a file.
    """

    def __init__(
        self,
        text="Browse",
        key: Hashable | None = None,
        target_key: Hashable | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        filename_only: bool = False,
        **kwargs,
    ):
        """
        Initialize a BrowseFileButton widget.

        Args:
            text (str): Text for the button.
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            target_key (Hashable, optional): Unique key for the target widget. Defaults to None.
                If set, the target widget's value is set to the selected filename.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (int | None, optional): X padding. Defaults to None.
            pady (int | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            filename_only (bool, optional): If True, only the filename is returned. Defaults to False.
            **kwargs: Additional keyword arguments are passed to ttk.Button or filedialog.askopenfilename as appropriate.
        """
        super().__init__(
            text,
            key=key,
            disabled=disabled,
            columnspan=columnspan,
            rowspan=rowspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
        )
        self.target_key = target_key
        self.widget_type = "guitk.BrowseFileButton"
        self._filename = None
        self._filename_only = filename_only
        self.kwargs = kwargs

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent
        kwargs_button = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_button_attributes
        }
        self.widget = ttk.Button(
            parent, text=self.text, command=self.browse_dialog, **kwargs_button
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def filename(self):
        return self._filename

    def browse_dialog(self):
        """Open a file dialog to select a file"""
        kwargs_options = {
            k: v for k, v in self.kwargs.items() if k in _valid_askopenfile_options
        }
        self._filename = filedialog.askopenfilename(**kwargs_options)
        if self._filename_only and self._filename:
            # only want the name, not the path
            self._filename = str(pathlib.Path(self._filename).name)
        if self.target_key and self._filename:
            self.window[self.target_key].value = self._filename
        event = Event(self, self.window, self.key, EventType.BrowseFile)
        self.window._handle_event(event)


class BrowseDirectoryButton(Button):
    def __init__(
        self,
        text="Browse",
        key: Hashable | None = None,
        target_key: Hashable | None = None,
        disabled: bool = False,
        columnspan: int | None = None,
        rowspan: int | None = None,
        padx: int | None = None,
        pady: int | None = None,
        events: bool = True,
        sticky: str | None = None,
        tooltip: TooltipType | None = None,
        **kwargs,
    ):
        """
        Initialize a BrowseDirectoryButton widget.

        Args:
            text (str): Text for the button.
            key (Hashable, optional): Unique key for this widget. Defaults to None.
            target_key (Hashable, optional): Unique key for the target widget. Defaults to None.
                If set, the target widget's value is set to the selected directory.
            disabled (bool, optional): If True, widget is disabled. Defaults to False.
            columnspan (int | None, optional): Number of columns to span. Defaults to None.
            rowspan (int | None, optional): Number of rows to span. Defaults to None.
            padx (int | None, optional): X padding. Defaults to None.
            pady (int | None, optional): Y padding. Defaults to None.
            events (bool, optional): Enable events for this widget. Defaults to False.
            sticky (str | None, optional): Sticky direction for widget layout. Defaults to None.
            tooltip (TooltipType | None, optional): Tooltip text or callback to generate tooltip text. Defaults to None.
            **kwargs: Additional keyword arguments are passed to ttk.Button or filedialog.askopenfilename as appropriate.
        """
        super().__init__(
            text,
            key=key,
            disabled=disabled,
            columnspan=columnspan,
            rowspan=rowspan,
            padx=padx,
            pady=pady,
            events=events,
            sticky=sticky,
            tooltip=tooltip,
        )
        self.target_key = target_key
        self.widget_type = "guitk.BrowseDirectoryButton"
        self._dirname = None
        self.kwargs = kwargs

    def _create_widget(self, parent, window: "Window", row, col):
        self.window = window
        self._parent = parent

        kwargs_button = {
            k: v for k, v in self.kwargs.items() if k in _valid_ttk_button_attributes
        }
        self.widget = ttk.Button(
            parent, text=self.text, command=self.browse_dialog, **kwargs_button
        )
        self._grid(
            row=row, column=col, rowspan=self.rowspan, columnspan=self.columnspan
        )
        if self._disabled:
            self.widget.state(["disabled"])

        return self.widget

    @property
    def directory(self):
        return self._dirname

    def browse_dialog(self):
        """
        Open a file dialog to select a directory.
        """
        kwargs_options = {
            k: v for k, v in self.kwargs.items() if k in _valid_askopenfile_options
        }
        self._dirname = filedialog.askdirectory(**kwargs_options)
        if self.target_key and self._dirname:
            self.window[self.target_key].value = self._dirname
        event = Event(self, self.window, self.key, EventType.BrowseDirectory)
        self.window._handle_event(event)
