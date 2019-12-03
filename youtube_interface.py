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

        #tab buttons
        StatsButton1 = tk.Button(self, text="Stats", command=lambda: controller.show_frame("StatsFrame"))
        StatsButton1.config(height = 1, width = 10)
        StatsButton1.place(x = 1, y = 1)
        
        SearchButton1 = tk.Button(self, text="Search", command=lambda: controller.show_frame("SearchFrame"))
        SearchButton1.config(height = 1, width = 10)
        SearchButton1.place(x = 100, y = 1)

        SettingsButton1 = tk.Button(self, text="Settings", command=lambda: controller.show_frame("SettingsFrame"))    
        SettingsButton1.config(height = 1, width = 10)
        SettingsButton1.place(x = 200, y = 1)

        
        #degree distribution **************************************************
        
        #main label
        degree_distribution_label = tk.Label(self, text="Degree Distribution")
        degree_distribution_label.place(x = 90, y = 50)

        #in degree button
        #//create button for just opening a matplotlib graph
        in_degree_button = tk.Button(self, text="In Degree")    
        in_degree_button.config(height = 1, width = 9)
        in_degree_button.place(x = 60, y = 85)

        #out degree button
        out_degree_button = tk.Button(self, text="Out Degree")    
        out_degree_button.config(height = 1, width = 10)
        out_degree_button.place(x = 160, y = 85)

        #average degree label
        average_degree_label = tk.Label(self, text="average degree")
        average_degree_label.place(x = 100, y = 120)


        #average degree output box
        average_degree_output = tk.Text(self,bd = 2, height = 1, width = 10)
        average_degree_output.place(x = 110, y = 150)
        
        #maximum degree label
        maximum_degree_label = tk.Label(self, text="maximum degree")
        maximum_degree_label.place(x = 100, y = 190)

        #maximum degree output box
        maximum_degree_output = tk.Text(self,bd = 2, height = 1, width = 10)
        maximum_degree_output.place(x = 110, y = 220)

        #minimum degree label
        minimum_degree_label = tk.Label(self, text="minimum degree")
        minimum_degree_label.place(x = 100, y = 260)

        #minimum degree output box
        minimum_degree_output = tk.Text(self,bd = 2, height = 1, width = 10)
        minimum_degree_output.place(x = 110, y = 290)
        

        #categorized statistics ***********************************************

        #main label
        categorized_statistics_label = tk.Label(self, text="Categorized Statistics")
        categorized_statistics_label.place(x = 320, y = 50)

        #///////not sure how to continue with this one yet, ask team/steve


class SearchFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="search page")
        label.pack(side="top", fill="x", pady=10)

        #tab buttons
        StatsButton2 = tk.Button(self, text="Stats", command=lambda: controller.show_frame("StatsFrame"))
        StatsButton2.config(height = 1, width = 10)
        StatsButton2.place(x = 1, y = 1)
       
        SearchButton2 = tk.Button(self, text="Search", command=lambda: controller.show_frame("SearchFrame"))
        SearchButton2.config(height = 1, width = 10)
        SearchButton2.place(x = 100, y = 1)
        
        SettingsButton2 = tk.Button(self, text="Settings", command=lambda: controller.show_frame("SettingsFrame"))
        SettingsButton2.config(height = 1, width = 10)
        SettingsButton2.place(x = 200, y = 1)


        # Range query **************************************************

        #range query label
        range_query_label = tk.Label(self, text="Range Query")
        range_query_label.place(x = 75, y = 50)

        #range query input 1 t1
        range_query_input_1 = tk.Entry(self, width = 4)
        range_query_input_1.place(x = 50, y = 100)

        range_query_input_1_label = tk.Label(self, text="t1")
        range_query_input_1_label.place(x = 60, y = 75)

        #range query input 2 t2
        range_query_input_2 = tk.Entry(self, width = 4)
        range_query_input_2.place(x = 150, y = 100)

        range_query_input_2_label = tk.Label(self, text="t2")
        range_query_input_2_label.place(x = 160, y = 75)

        #range query input 3 x
        range_query_input_3 = tk.Entry(self, width = 4)
        range_query_input_3.place(x = 50, y = 160)

        range_query_input_3_label = tk.Label(self, text="x")
        range_query_input_3_label.place(x = 60, y = 135)

        #range query input 4 y
        range_query_input_4 = tk.Entry(self, width = 4)
        range_query_input_4.place(x = 150, y = 160)

        range_query_input_4_label = tk.Label(self, text="y")
        range_query_input_4_label.place(x = 160, y = 135)


        #range query category box
        range_query_category_input = tk.Entry(self, width = 15)
        range_query_category_input.place(x = 50, y = 220)

        range_query_category_input_label = tk.Label(self, text="Category")
        range_query_category_input_label.place(x = 80, y = 190)

        #range query output box
        range_query_output = tk.Text(self,bd = 2, height = 4, width = 20)
        range_query_output.place(x = 50, y = 290)
        
        range_query_output_label = tk.Label(self, text="Output Range")
        range_query_output_label.place(x = 75, y = 260)
        
        #scrollbar
        range_query_output_scrollbar = tk.Scrollbar(self)
        range_query_output_scrollbar.place(x = 215, y = 290)
        range_query_output_scrollbar.config(command=range_query_output.yview)
        range_query_output.config(yscrollcommand=range_query_output_scrollbar.set)

        #video length search button
        video_length_search_button = tk.Button(self, text="Length")
        video_length_search_button.config(height = 1, width = 6)
        video_length_search_button.place(x = 50, y = 370)


        #video physical size search button
        video_length_search_button = tk.Button(self, text="Size")
        video_length_search_button.config(height = 1, width = 4)
        video_length_search_button.place(x = 150, y = 370)
        
        
        #top k queries *******************************************************

        #range query label
        top_k_label = tk.Label(self, text="Top K search")
        top_k_label.place(x = 300, y = 50)

        #input for k value
        top_k_value = tk.Entry(self, width = 4)
        top_k_value.place(x = 320, y = 100)

        top_k_value_label = tk.Label(self, text="K")
        top_k_value_label.place(x = 335, y = 75)

        #top k categories button
        top_k_categories_button = tk.Button(self, text="Categories")
        top_k_categories_button.config(height = 1, width = 10)
        top_k_categories_button.place(x = 300, y = 135)

        #top k ratings button
        top_k_ratings_button = tk.Button(self, text="Ratings")
        top_k_ratings_button.config(height = 1, width = 7)
        top_k_ratings_button.place(x = 310, y = 170)

        #top k popularity button
        top_k_popularity_button = tk.Button(self, text="Popularity")
        top_k_popularity_button.config(height = 1, width = 10)
        top_k_popularity_button.place(x = 300, y = 205)

        #range query output box
        top_k_output = tk.Text(self,bd = 2, height = 4, width = 20)
        top_k_output.place(x = 270, y = 290)
        
        top_k_output_label = tk.Label(self, text="Output Top K")
        top_k_output_label.place(x = 300, y = 260)
        
        #scrollbar
        top_k_output_scrollbar = tk.Scrollbar(self)
        top_k_output_scrollbar.place(x = 425, y = 290)
        top_k_output_scrollbar.config(command=top_k_output.yview)
        top_k_output.config(yscrollcommand=top_k_output_scrollbar.set)


        #subgraph patterns**********************************************

        #///////not sure how to continue with this one yet, ask team/steve

        #subgraph patterns label
        subgraph_patterns_label = tk.Label(self, text="Subgraph Patterns")
        subgraph_patterns_label.place(x = 550, y = 50)

        
        
        
        #pagerank **********************************************

        #pagerank label
        pagerank_label = tk.Label(self, text="PageRank")
        pagerank_label.place(x = 810, y = 50)

        #input for k value
        pagerank_k_value = tk.Entry(self, width = 4)
        pagerank_k_value.place(x = 820, y = 100)

        pagerank_k_value_label = tk.Label(self, text="K")
        pagerank_k_value_label.place(x = 835, y = 75)

        #pagerank run button
        pagerank_run_button = tk.Button(self, text="PageRank")
        pagerank_run_button.config(height = 1, width = 8)
        pagerank_run_button.place(x = 805, y = 135)

        #pagerank output label
        pagerank_output_label = tk.Label(self, text="PageRank Results")
        pagerank_output_label.place(x = 785, y = 190)

        #pagerank output box
        pagerank_output = tk.Text(self,bd = 2, height = 4, width = 20)
        pagerank_output.place(x = 780, y = 220)
        
        
        
        #scrollbar
        pagerank_output_scrollbar = tk.Scrollbar(self)
        pagerank_output_scrollbar.place(x = 935, y = 220)
        pagerank_output_scrollbar.config(command=pagerank_output.yview)
        pagerank_output.config(yscrollcommand=pagerank_output_scrollbar.set)






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
        
        SearchButton3.config(height = 1, width = 10)
        SearchButton3.place(x = 100, y = 1)

        SettingsButton3.config(height = 1, width = 10)
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

 

#3. output text box for categorized statistics with labels
#4. output text box for degree distribution with label
#5. output box for pagerank list with label
#6. subraph patterns in search page
