import sys
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

def getpass():
    """
    generic tkinter method to show popup for password input
    :return:
    """
    root = tk.Tk()
    root.withdraw()
    return simpledialog.askstring("IronVeil", "Enter password:", show='*')

def show_message(type: str, message: str) -> None:
    """
    generick tkinter method to show message popup
    :param type: message type { E, S }
    :param message: message text
    :return:
    """
    root = tk.Tk()
    root.withdraw()
    if type == 'S':
        messagebox.showinfo('Success',message)
    elif type == 'E':
        messagebox.showerror('Error', message)

def open_settings():
    sys.exit(1)