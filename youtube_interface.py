import tkinter as tk
import psycopg2
from pexpect import pxssh
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
        self.resizable(0, 0)              #fix the size

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
#        self.connect_dbs


        self.frames = {}
        for Fr in (StatsFrame, SearchFrame, SettingsFrame):
            frame_name = Fr.__name__
            frame = Fr(parent=container, controller=self)
            self.frames[frame_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StatsFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

#    def connect_dbs():
#        conn = None
#        try:
            # connect to the rds database
#            print('Connecting to the rds db')
#            conn = psycopg2.connect(
#                host = 'testdb-rmiller1-instance.c9dhbkaqdlyx.us-east-1.rds.amazonaws.com',
#                port = 5432,
#                user = 'rmiller1',
#                password = 'testpassword',
#                database='testdb1rm'
#                )
            # creating a cursor
#            cur = conn.cursor()
        
            # test connection by getting databse version
#            print('rds database version:')
#            cur.execute('SELECT version()')
 
            # display the db version
#            db_version = cur.fetchone()
#            print(db_version)
#       
#           # close the communication with the PostgreSQL
#            #cur.close()
#        except (Exception, psycopg2.DatabaseError) as error:
#            print(error)
#        finally:
#            if conn is not None:
#                conn.close()
#                print('Database connection closed.')
 



class StatsFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="stats page")
        label.pack(side="top", fill="x", pady=10)

        StatsButton1 = tk.Button(self, text="Stats", command=lambda: controller.show_frame("StatsFrame"))
        SearchButton1 = tk.Button(self, text="Search", command=lambda: controller.show_frame("SearchFrame"))
        SettingsButton1 = tk.Button(self, text="Settings", command=lambda: controller.show_frame("SettingsFrame"))    


        StatsButton1.config(height = 1, width = 10)
        StatsButton1.place(x = 1, y = 1)
        
        SearchButton1.config(heigh = 1, width = 10)
        SearchButton1.place(x = 100, y = 1)

        SettingsButton1.config(heigh = 1, width = 10)
        SettingsButton1.place(x = 200, y = 1)


class SearchFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="search page")
        label.pack(side="top", fill="x", pady=10)

        #tab buttons
        StatsButton2 = tk.Button(self, text="Stats", command=lambda: controller.show_frame("StatsFrame"))
        SearchButton2 = tk.Button(self, text="Search", command=lambda: controller.show_frame("SearchFrame"))
        SettingsButton2 = tk.Button(self, text="Settings", command=lambda: controller.show_frame("SettingsFrame"))
        

        #range query label
        range_query_label = tk.Label(self, text="Range Query")
        range_query_label.place(x = 75, y = 50)

        #range query input 1
        range_query_input_1 = tk.Entry(self, width = 4)
        range_query_input_1.place(x = 50, y = 100)

        range_query_input_1_label = tk.Label(self, text="t1")
        range_query_input_1_label.place(x = 60, y = 75)

        #range query input 2
        range_query_input_2 = tk.Entry(self, width = 4)
        range_query_input_2.place(x = 150, y = 100)

        range_query_input_2_label = tk.Label(self, text="t2")
        range_query_input_2_label.place(x = 160, y = 75)


        #range query category box
        range_query_category_input = tk.Entry(self, width = 15)
        range_query_category_input.place(x = 50, y = 170)

        range_query_category_input_label = tk.Label(self, text="Category")
        range_query_category_input_label.place(x = 80, y = 140)

        #range query output box
        range_query_output = tk.Text(self,bd = 2, height = 4, width = 20)
        range_query_output.place(x = 50, y = 240)

        range_query_output_label = tk.Label(self, text="Output")
        range_query_output_label.place(x = 90, y = 210)
        
        #///add scroll bar
        
        

        StatsButton2.config(height = 1, width = 10)
        StatsButton2.place(x = 1, y = 1)
        
        SearchButton2.config(heigh = 1, width = 10)
        SearchButton2.place(x = 100, y = 1)

        SettingsButton2.config(heigh = 1, width = 10)
        SettingsButton2.place(x = 200, y = 1)




class SettingsFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="settings page")
        label.pack(side="top", fill="x", pady=10)

        StatsButton3 = tk.Button(self, text="Stats", command=lambda: controller.show_frame("StatsFrame"))
        SearchButton3 = tk.Button(self, text="Search", command=lambda: controller.show_frame("SearchFrame"))
        SettingsButton3 = tk.Button(self, text="Settings", command=lambda: controller.show_frame("SettingsFrame"))


        StatsButton3.config(height = 1, width = 10)
        StatsButton3.place(x = 1, y = 1)
        
        SearchButton3.config(heigh = 1, width = 10)
        SearchButton3.place(x = 100, y = 1)

        SettingsButton3.config(heigh = 1, width = 10)
        SettingsButton3.place(x = 200, y = 1)


if __name__ == "__main__":
    app = mainwindow()
    app.mainloop()




#how im thinking of connecting to the databases.
#hopefully if we get neo4j up and running on aws and is available to ssh into 
#using pexpect to ssh into
#send the commands from this app -> pexpect -> aws neo4j instance

#pxssh link https://www.pythonforbeginners.com/code-snippets-source-code/ssh-connection-with-python
#pexpect link from stackoverflow https://stackoverflow.com/questions/15096667/ssh-and-send-commands-in-tkinter
#github pexpect https://github.com/pexpect/pexpect


#todo list

#1. range queries: needs button, inputs for t1 and t2, 
# as well as input text for category X, and output text box
#2. top k inputs: needs input for k and a text box display, and button for enter
#3. output text box for categorized statistics with labels
#4. output text box for degree distribution with label
#5. output box for pagerank list with label

