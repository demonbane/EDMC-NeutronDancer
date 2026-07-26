import tkinter as tk
from tkinter import ttk

from theme import theme  # type: ignore


class EditableComboBox(ttk.Combobox):
    """An editable combobox with the same small API used by plotter fields."""

    def __init__(self, parent:tk.Frame, placeholder:str, **kw) -> None:
        values:list[str] = list(kw.pop('values', []))
        self.placeholder:str = placeholder
        self.var:tk.StringVar = tk.StringVar()
        super().__init__(parent, textvariable=self.var, values=values, state='normal', **kw)
        theme.register(self)

        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)
        self.put_placeholder()

    def put_placeholder(self) -> None:
        if not self.get():
            self.set_text(self.placeholder, True)

    def set_text(self, text, placeholder_style:bool = True) -> None:
        self.var.set(text)
        self.configure(style='Placeholder.TCombobox' if placeholder_style else 'TCombobox')

    def set_menu(self, values:list[str]) -> None:
        self.configure(values=values)

    def set_default_style(self) -> None:
        self.configure(style='TCombobox')

    def set_error_style(self, error:bool = True) -> None:
        style:str = 'Error.TCombobox' if error else 'TCombobox'
        ttk.Style(self).configure('Error.TCombobox', foreground='red')
        self.configure(style=style)

    def focus_in(self, _event = None) -> None:
        self.set_default_style()
        if self.get() == self.placeholder:
            self.var.set('')

    def focus_out(self, _event = None) -> None:
        if not self.get():
            self.put_placeholder()

    def hide_list(self) -> None:
        self.event_generate('<Escape>')
