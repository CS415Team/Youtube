import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os




class mainwindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #window settings
        self.title('Youtube Analyzer')    #set title
        self.geometry("1000x800")         #set the size
        #self.resizable(0, 0)              #fix the size

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for Fr in (StatsFrame, SearchFrame):
            frame_name = Fr.__name__
            frame = Fr(parent=container, controller=self)
            self.frames[frame_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StatsFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()


class StatsFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="stats page")
        label.pack(side="top", fill="x", pady=10)

        StatsButton1 = tk.Button(self, text="Stats", command=lambda: controller.show_frame("StatsFrame"))
        SearchButton1 = tk.Button(self, text="Search", command=lambda: controller.show_frame("SearchFrame"))
        
        StatsButton1.config(height = 1, width = 10)
        StatsButton1.place(x = 1, y = 1)
        
        SearchButton1.config(heigh = 1, width = 10)
        SearchButton1.place(x = 100, y = 1)





class SearchFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="search page")
        label.pack(side="top", fill="x", pady=10)

        StatsButton2 = tk.Button(self, text="Stats", command=lambda: controller.show_frame("StatsFrame"))
        SearchButton2 = tk.Button(self, text="Search", command=lambda: controller.show_frame("SearchFrame"))

        StatsButton2.config(height = 1, width = 10)
        StatsButton2.place(x = 1, y = 1)
        
        SearchButton2.config(heigh = 1, width = 10)
        SearchButton2.place(x = 100, y = 1)

#mainwindow.mainloop()

if __name__ == "__main__":
    app = mainwindow()
    app.mainloop()



#thoughts for organization of the interface
#Each of the different pieces will be presented in a different window.
#i.e. if you want to do search, you click on the search tab and then
#the search features appear on the screen only. 
#if you want to see the aggrigated statistics, click on the stats tab etc...
