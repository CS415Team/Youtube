import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os


x = 0
y = 0
m_win = tk.Tk()
m_win.geometry("500x500")

file = None
valid_box = tk.Text(m_win, height=2, width=50)
valid_box.pack()
valid_box.insert(tk.END, "Upload or start analysis please.")