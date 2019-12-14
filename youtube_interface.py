import tkinter as tk
import numpy as np
import neo4j
#import psycopg2
#import os
#import sys
import matplotlib.pyplot as plt 
from pexpect import pxssh
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from neo4j import GraphDatabase 



class mainwindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #window settings
        self.title('Youtube Analyzer')    #set title
        self.geometry("1000x800")         #set the size
        self.resizable(0, 0)              #fix the size

        global rds_connection
        global graph_connection

        #test 
        rds_connection = 0
        graph_connection = 0

        #ssh setup

        #ssh_conn = pxssh.pxssh()
        #hostname = raw_input('')
        #username = 
 


        


        #initial window setup
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for frame_option in (StatsFrame, RangeFrame, TopKFrame, SubgraphFrame, PageRankFrame):
            frame_name = frame_option.__name__
            
            frame = frame_option(parent=container, controller=self)
            
            self.frames[frame_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.display_frame("StatsFrame")

    def display_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()


class StatsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background='grey')

        #frame label
        stats_frame_label = tk.Label(self,background='grey', text="Statistics")
        stats_frame_label.place(x=700, y=5)
        stats_frame_label.config(font=("Courier", 30))



        #tab buttons
        StatsButton1 = tk.Button(self, text="Stats",highlightbackground='grey', command=lambda: controller.display_frame("StatsFrame"))
        StatsButton1.config(height = 1, width = 8)
        StatsButton1.place(x = 1, y = 1)
        
        RangeButton1 = tk.Button(self, text="Range",highlightbackground='grey', command=lambda: controller.display_frame("RangeFrame"))
        RangeButton1.config(height = 1, width = 8)
        RangeButton1.place(x = 100, y = 1)

        TopKButton1 = tk.Button(self, text="Top K",highlightbackground='grey', command=lambda: controller.display_frame("TopKFrame"))    
        TopKButton1.config(height = 1, width = 8)
        TopKButton1.place(x = 200, y = 1)

        SubgraphButton1 = tk.Button(self, text="Subgraph",highlightbackground='grey', command=lambda: controller.display_frame("SubgraphFrame"))    
        SubgraphButton1.config(height = 1, width = 8)
        SubgraphButton1.place(x = 300, y = 1)

        PageRankButton1 = tk.Button(self, text="PageRank",highlightbackground='grey', command=lambda: controller.display_frame("PageRankFrame"))    
        PageRankButton1.config(height = 1, width = 8)
        PageRankButton1.place(x = 400, y = 1)

        #degree distribution frame
        degree_distribution_frame = Frame(self, height=400, width=400, bd=2, relief=GROOVE)
        degree_distribution_frame.place(x = 30, y = 45)

        #categorized statistics frame
        categorized_statistics_frame = Frame(self, height=400, width=350, bd=2, relief=GROOVE)
        categorized_statistics_frame.place(x = 560, y = 45)

        #average degree output box frame
        average_degree_frame = Frame(self, height=40, width=95, bd=2, relief=GROOVE)
        average_degree_frame.place(x = 145, y = 145)
        
        #maximum degree output box frame
        maximum_degree_frame = Frame(self, height=40, width=95, bd=2, relief=GROOVE)
        maximum_degree_frame.place(x = 145, y = 215)

        #minimum degree output box frame
        minimum_degree_frame = Frame(self, height=40, width=95, bd=2, relief=GROOVE)
        minimum_degree_frame.place(x = 145, y = 285)


        #degree distribution ******************************************************
        
        #main label
        degree_distribution_label = tk.Label(self, text="Degree Distribution")
        degree_distribution_label.place(x = 130, y = 50)

        def in_degree_button_action():
            x_names = ['0-100','101-200','201-300','301-400','401-500','501-600']
            y = [6,7,8,9,10,11]
            x = [1,2,3,4,5,6]
            plt.bar(x, y, label="In Degree")
            plt.xlabel('Video Age')
            plt.ylabel('counts')
            plt.xticks(x, x_names)
            plt.title('In Degree Distribution')
            plt.legend()
            plt.show()
        def out_degree_button_action():
            x_names = ['0-100','101-200','201-300','301-400','401-500','501-600']
            y = [6,7,8,9,10,11]
            x = [1,2,3,4,5,6]
            plt.bar(x, y, label="Out Degree")
            plt.xlabel('Video Age')
            plt.ylabel('counts')
            plt.xticks(x, x_names)
            plt.title('Out Degree Distribution')
            plt.legend()
            plt.show()

        #in degree button
        in_degree_button = tk.Button(self, text="In Degree",  command=lambda: in_degree_button_action())    
        in_degree_button.config(height = 1, width = 8)
        in_degree_button.place(x = 100, y = 85)

        #out degree button
        out_degree_button = tk.Button(self, text="Out Degree",  command=lambda: out_degree_button_action())    
        out_degree_button.config(height = 1, width = 8)
        out_degree_button.place(x = 200, y = 85)

        #average degree label
        average_degree_label = tk.Label(self, text="average degree")
        average_degree_label.place(x = 140, y = 120)

        #average degree output box
        average_degree_output = tk.Text(self,bd = 2, height = 1, width = 10)
        average_degree_output.place(x = 150, y = 150)
        
        uri = "bolt://localhost:7687"
        user = "neo4j"
        passw = "cpts415"

        _driver = GraphDatabase.driver(uri, auth=(user, passw))

        #Average In Degree of all Videos
        query2 = 'MATCH (video:Video)<-[r]-(video1:Video)\nWITH count(r) as num\nRETURN avg(num) as avgIN;'

        with _driver.session() as session:
            with session.begin_transaction() as tx:
                results1 = (tx.run(query2))
            session.close()

        average_degree_output.delete(1.0, tk.END)
        average_degree_output.insert(tk.END, results1)


        #maximum degree label
        maximum_degree_label = tk.Label(self, text="maximum degree")
        maximum_degree_label.place(x = 140, y = 190)

        #maximum degree output box
        maximum_degree_output = tk.Text(self,bd = 2, height = 1, width = 10)
        maximum_degree_output.place(x = 150, y = 220)

        uri = "bolt://localhost:7687"
        user = "neo4j"
        passw = "cpts415"

        _driver = GraphDatabase.driver(uri, auth=(user, passw))

        #Max In Degree of all Videos
        query3 = 'MATCH (video:Video)<-[r]-(video1:Video)\nWITH count(r) as num\nRETURN max(num) as maxIN;'

        with _driver.session() as session:
            with session.begin_transaction() as tx:
                results2 = (tx.run(query3))
            session.close()

        maximum_degree_output.delete(1.0, tk.END)
        maximum_degree_output.insert(tk.END, results2)

        #minimum degree label
        minimum_degree_label = tk.Label(self, text="minimum degree")
        minimum_degree_label.place(x = 140, y = 260)

        #minimum degree output box
        minimum_degree_output = tk.Text(self,bd = 2, height = 1, width = 10)
        minimum_degree_output.place(x = 150, y = 290)

        uri = "bolt://localhost:7687"
        user = "neo4j"
        passw = "cpts415"

        _driver = GraphDatabase.driver(uri, auth=(user, passw))

        #Min In Degree of all Videos
        query4 = 'MATCH (video:Video)<-[r]-(video1:Video)\nWITH count(r) as num\nRETURN min(num) as minIN;'

        with _driver.session() as session:
            with session.begin_transaction() as tx:
                results4 = (tx.run(query4))
            session.close()

        minimum_degree_output.delete(1.0, tk.END)
        minimum_degree_output.insert(tk.END, results4)

        
        

        
        #categorized statistics ***************************************************

        #main label
        categorized_statistics_label = tk.Label(self, text="Categorized Statistics")
        categorized_statistics_label.place(x = 650, y = 50)

        def plotmaker(type_plot):
            if(type_plot == "age"):
                x_names = ['0-100','101-200','201-300','301-400','401-500','501-600']
                y = [6,7,8,9,10,11]
                x = [1,2,3,4,5,6]
                plt.bar(x, y, label="Age totals")
                plt.xlabel('Video Age')
                plt.ylabel('counts')
                plt.xticks(x, x_names)
                plt.title('Distribution of Video Age')
            elif(type_plot == "category"):
                x_names = ['0-100','101-200','201-300','301-400','401-500','501-600']
                y = [6,7,8,9,10,11]
                x = [1,2,3,4,5,6]
                plt.bar(x, y, label="Category totals")
                plt.xlabel('Categories')
                plt.ylabel('counts')
                plt.xticks(x, x_names)
                plt.title('Distribution of Categories')
            elif(type_plot == "length"):
                x_names = ['0-100','101-200','201-300','301-400','401-500','501-600']
                y = [6,7,8,9,10,11]
                x = [1,2,3,4,5,6]
                plt.bar(x, y, label="Length Totals")
                plt.xlabel('Length')
                plt.ylabel('counts')
                plt.xticks(x, x_names)
                plt.title('Distribution of Length')
            elif(type_plot == "views"):
                x_names = ['0-100','101-200','201-300','301-400','401-500','501-600']
                y = [6,7,8,9,10,11]
                x = [1,2,3,4,5,6]
                plt.bar(x, y, label="View totals")
                plt.xlabel('Views')
                plt.ylabel('counts')
                plt.xticks(x, x_names)
                plt.title('Distribution of Views')
            elif(type_plot == "rate"):
                x_names = ['0-100','101-200','201-300','301-400','401-500','501-600']
                y = [6,7,8,9,10,11]
                x = [1,2,3,4,5,6]
                plt.bar(x, y, label="Rate totals")
                plt.xlabel('Rate')
                plt.ylabel('counts')
                plt.xticks(x, x_names)
                plt.title("Distribution of Rate")
            elif(type_plot == "ratings"):
                x_names = ['0-100','101-200','201-300','301-400','401-500','501-600']
                y = [6,7,8,9,10,11]
                x = [1,2,3,4,5,6]
                plt.bar(x, y, label="Ratings totals")
                plt.xlabel('Ratings')
                plt.ylabel('counts')
                plt.xticks(x, x_names)
                plt.title('Distribution of Ratings')
            elif(type_plot == "comments"):
                x_names = ['0-100','101-200','201-300','301-400','401-500','501-600']
                y = [6,7,8,9,10,11]
                x = [1,2,3,4,5,6]
                plt.bar(x, y, label="Comments totals")
                plt.xlabel('Comments')
                plt.ylabel('counts')
                plt.xticks(x, x_names)
                plt.title('Distribution of Comments')

            plt.legend()
            plt.show()

        def age_plot_button_action():
            plotmaker("age")

        def category_plot_button_action():
            plotmaker("category")

        def length_plot_button_action():
            plotmaker("length")

        def views_plot_button_action():
            plotmaker("views")

        def rate_plot_button_action():
            plotmaker("rate")

        def ratings_plot_button_action():
            plotmaker("ratings")
        
        def comments_plot_button_action():
            plotmaker("comments")

        #Launch age plot label
        launch_age_plot_label = tk.Label(self, text="Launch Age Plot            ->")
        launch_age_plot_label.place(x = 575, y = 85)

        #age plot button
        age_plot_button = tk.Button(self, text="Age",  command=lambda: age_plot_button_action())    
        age_plot_button.config(height = 1, width = 8)
        age_plot_button.place(x = 750, y = 85)

        #Launch category plot label
        launch_category_plot_label = tk.Label(self, text="Launch Category Plot   ->")
        launch_category_plot_label.place(x = 575, y = 115)

        #category plot button
        category_plot_button = tk.Button(self, text="Category",  command=lambda: category_plot_button_action())    
        category_plot_button.config(height = 1, width = 8)
        category_plot_button.place(x = 750, y = 115)

        #Launch length plot label
        launch_length_plot_label = tk.Label(self, text="Launch length Plot        ->")
        launch_length_plot_label.place(x = 575, y = 145)

        #length plot button
        length_plot_button = tk.Button(self, text="Length",  command=lambda: length_plot_button_action())    
        length_plot_button.config(height = 1, width = 8)
        length_plot_button.place(x = 750, y = 145)

        #Launch views plot label
        launch_views_plot_label = tk.Label(self, text="Launch Views Plot         ->")
        launch_views_plot_label.place(x = 575, y = 175)

        #views plot button
        views_plot_button = tk.Button(self, text="Views",  command=lambda: views_plot_button_action())    
        views_plot_button.config(height = 1, width = 8)
        views_plot_button.place(x = 750, y = 175)

        #Launch rate plot label
        launch_rate_plot_label = tk.Label(self, text="Launch Rate Plot           ->")
        launch_rate_plot_label.place(x = 575, y = 205)

        #rate plot button
        rate_plot_button = tk.Button(self, text="Rate",  command=lambda: rate_plot_button_action())    
        rate_plot_button.config(height = 1, width = 8)
        rate_plot_button.place(x = 750, y = 205)

        #Launch ratings plot label
        launch_ratings_plot_label = tk.Label(self, text="Launch Ratings Plot      ->")
        launch_ratings_plot_label.place(x = 575, y = 235)

        #ratings plot button
        ratings_plot_button = tk.Button(self, text="Ratings",  command=lambda: ratings_plot_button_action())    
        ratings_plot_button.config(height = 1, width = 8)
        ratings_plot_button.place(x = 750, y = 235)

        #Launch comments plot label
        launch_comments_plot_label = tk.Label(self, text="Launch Comments Plot ->")
        launch_comments_plot_label.place(x = 575, y = 265)

        #comments plot button
        comments_plot_button = tk.Button(self, text="Comments",  command=lambda: comments_plot_button_action())    
        comments_plot_button.config(height = 1, width = 8)
        comments_plot_button.place(x = 750, y = 265)


class RangeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background='grey')

        #frame label
        Range_frame_label = tk.Label(self,background='grey', text="Range Search")
        Range_frame_label.place(x=700, y=5)
        Range_frame_label.config(font=("Courier", 30))



        #tab buttons
        StatsButton2 = tk.Button(self, text="Stats",highlightbackground='grey', command=lambda: controller.display_frame("StatsFrame"))
        StatsButton2.config(height = 1, width = 8)
        StatsButton2.place(x = 1, y = 1)
        
        RangeButton2 = tk.Button(self, text="Range",highlightbackground='grey', command=lambda: controller.display_frame("RangeFrame"))
        RangeButton2.config(height = 1, width = 8)
        RangeButton2.place(x = 100, y = 1)

        TopKButton2 = tk.Button(self, text="Top K",highlightbackground='grey', command=lambda: controller.display_frame("TopKFrame"))    
        TopKButton2.config(height = 1, width = 8)
        TopKButton2.place(x = 200, y = 1)

        SubgraphButton2 = tk.Button(self, text="Subgraph",highlightbackground='grey', command=lambda: controller.display_frame("SubgraphFrame"))    
        SubgraphButton2.config(height = 1, width = 8)
        SubgraphButton2.place(x = 300, y = 1)

        PageRankButton2 = tk.Button(self, text="PageRank",highlightbackground='grey', command=lambda: controller.display_frame("PageRankFrame"))    
        PageRankButton2.config(height = 1, width = 8)
        PageRankButton2.place(x = 400, y = 1)

        #range query frame
        range_query_frame = Frame(self, height=700, width=600, bd=2, relief=GROOVE)
        range_query_frame.place(x = 200, y = 45)

        #output box frame
        range_output_box_frame = Frame(self, height=400, width=305, bd=2, relief=GROOVE)
        range_output_box_frame.place(x = 355, y = 285)

        #range query input 1 t1 label
        range_query_input_1_label = tk.Label(self, text="t1")
        range_query_input_1_label.place(x = 410, y = 75)

        #range query input 1 t1
        range_query_input_1 = tk.Entry(self, width = 4)
        range_query_input_1.place(x = 400, y = 100)

        #range query input 2 t2 label
        range_query_input_2_label = tk.Label(self, text="t2")
        range_query_input_2_label.place(x = 580, y = 75)

        #range query input 2 t2
        range_query_input_2 = tk.Entry(self, width = 4)
        range_query_input_2.place(x = 570, y = 100)

        #range query input 3 x label
        range_query_input_3_label = tk.Label(self, text="x")
        range_query_input_3_label.place(x = 413, y = 135)

        #range query input 3 x
        range_query_input_3 = tk.Entry(self, width = 4)
        range_query_input_3.place(x = 400, y = 160)

        #range query input 4 y label
        range_query_input_4_label = tk.Label(self, text="y")
        range_query_input_4_label.place(x = 583, y = 135)

        #range query input 4 y
        range_query_input_4 = tk.Entry(self, width = 4)
        range_query_input_4.place(x = 570, y = 160)

        #range query category box label
        range_query_category_input_label = tk.Label(self, text="Category")
        range_query_category_input_label.place(x = 475, y = 190)

        #range query category box
        range_query_category_input = tk.Entry(self, width = 15)
        range_query_category_input.place(x = 435, y = 220)

        #range query output box label
        range_query_output_label = tk.Label(self, text="Output Range")
        range_query_output_label.place(x = 460, y = 260)

        #range query output box
        range_query_output = tk.Text(self,bd = 2, height = 25, width = 40)
        range_query_output.place(x = 360, y = 290)
        
        #video length search button action function
        def video_length_search_button_action():
            pass

        #video size search button action function
        def video_size_search_button_action():
            pass

        #video length search button
        video_length_search_button = tk.Button(self, text="Length", command=lambda: video_length_search_button_action())
        video_length_search_button.config(height = 1, width = 6)
        video_length_search_button.place(x = 370, y = 700)

        #video physical size search button
        video_size_search_button = tk.Button(self, text="Size", command=lambda: video_size_search_button_action())
        video_size_search_button.config(height = 1, width = 6)
        video_size_search_button.place(x = 570, y = 700)
        

class TopKFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background='grey')
        
        #frame label
        top_k_frame_label = tk.Label(self,background='grey', text="Top K Search")
        top_k_frame_label.place(x=700, y=5)
        top_k_frame_label.config(font=("Courier", 30))



        #tab buttons
        StatsButton3 = tk.Button(self, text="Stats",highlightbackground='grey', command=lambda: controller.display_frame("StatsFrame"))
        StatsButton3.config(height = 1, width = 8)
        StatsButton3.place(x = 1, y = 1)
        
        RangeButton3 = tk.Button(self, text="Range",highlightbackground='grey', command=lambda: controller.display_frame("RangeFrame"))
        RangeButton3.config(height = 1, width = 8)
        RangeButton3.place(x = 100, y = 1)

        TopKButton3 = tk.Button(self, text="Top K",highlightbackground='grey', command=lambda: controller.display_frame("TopKFrame"))    
        TopKButton3.config(height = 1, width = 8)
        TopKButton3.place(x = 200, y = 1)

        SubgraphButton3 = tk.Button(self, text="Subgraph",highlightbackground='grey', command=lambda: controller.display_frame("SubgraphFrame"))    
        SubgraphButton3.config(height = 1, width = 8)
        SubgraphButton3.place(x = 300, y = 1)

        PageRankButton3 = tk.Button(self, text="PageRank",highlightbackground='grey', command=lambda: controller.display_frame("PageRankFrame"))    
        PageRankButton3.config(height = 1, width = 8)
        PageRankButton3.place(x = 400, y = 1)

        #top k query frame
        top_k_query_frame = Frame(self, height=700, width=600, bd=2, relief=GROOVE)
        top_k_query_frame.place(x = 200, y = 45)

        #output box frame
        top_k_output_box_frame = Frame(self, height=400, width=305, bd=2, relief=GROOVE)
        top_k_output_box_frame.place(x = 355, y = 285)

        #input for k value label
        top_k_value_label = tk.Label(self, text="K")
        top_k_value_label.place(x = 500, y = 75)

        #input for k value
        top_k_value = tk.Entry(self, width = 4)
        top_k_value.place(x = 485, y = 100)

        def top_k_categories_button_action():
            pass

        def top_k_ratings_button_action():
            pass

        def top_k_popularity_button_action():
            pass

        #top k categories button
        top_k_categories_button = tk.Button(self, text="Categories", command=lambda: top_k_categories_button_action())
        top_k_categories_button.config(height = 1, width = 7)
        top_k_categories_button.place(x = 465, y = 135)

        #top k ratings button
        top_k_ratings_button = tk.Button(self, text="Ratings", command=lambda: top_k_ratings_button_action())
        top_k_ratings_button.config(height = 1, width = 7)
        top_k_ratings_button.place(x = 465, y = 170)

        #top k popularity button
        top_k_popularity_button = tk.Button(self, text="Popularity", command=lambda: top_k_popularity_button_action())
        top_k_popularity_button.config(height = 1, width = 7)
        top_k_popularity_button.place(x = 465, y = 205)

        #top k query output box label
        top_k_output_label = tk.Label(self, text="Output Top K")
        top_k_output_label.place(x = 460, y = 260)

        #top k query output box
        top_k_output = tk.Text(self,bd = 2, height = 25, width = 40)
        top_k_output.place(x = 360, y = 290)

        
class SubgraphFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background='grey')
        
        #frame label
        subgraph_frame_label = tk.Label(self,background='grey', text="Subgraph")
        subgraph_frame_label.place(x=700, y=5)
        subgraph_frame_label.config(font=("Courier", 30))



        #tab buttons
        StatsButton4 = tk.Button(self, text="Stats",highlightbackground='grey', command=lambda: controller.display_frame("StatsFrame"))
        StatsButton4.config(height = 1, width = 8)
        StatsButton4.place(x = 1, y = 1)
        
        RangeButton4 = tk.Button(self, text="Range",highlightbackground='grey', command=lambda: controller.display_frame("RangeFrame"))
        RangeButton4.config(height = 1, width = 8)
        RangeButton4.place(x = 100, y = 1)

        TopKButton4 = tk.Button(self, text="Top K",highlightbackground='grey', command=lambda: controller.display_frame("TopKFrame"))    
        TopKButton4.config(height = 1, width = 8)
        TopKButton4.place(x = 200, y = 1)

        SubgraphButton4 = tk.Button(self, text="Subgraph",highlightbackground='grey', command=lambda: controller.display_frame("SubgraphFrame"))    
        SubgraphButton4.config(height = 1, width = 8)
        SubgraphButton4.place(x = 300, y = 1)

        PageRankButton4 = tk.Button(self, text="PageRank",highlightbackground='grey', command=lambda: controller.display_frame("PageRankFrame"))    
        PageRankButton4.config(height = 1, width = 8)
        PageRankButton4.place(x = 400, y = 1)

        #///////not sure how to continue with this one yet, ask team/steve

        #subgraph query frame
        subgraph_query_frame = Frame(self, height=700, width=600, bd=2, relief=GROOVE)
        subgraph_query_frame.place(x = 200, y = 45)


class PageRankFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background='grey')
        
        #frame label
        PageRank_frame_label = tk.Label(self,background='grey', text="PageRank")
        PageRank_frame_label.place(x=700, y=5)
        PageRank_frame_label.config(font=("Courier", 30))



        #tab buttons
        StatsButton5 = tk.Button(self, text="Stats",highlightbackground='grey', command=lambda: controller.display_frame("StatsFrame"))
        StatsButton5.config(height = 1, width = 8)
        StatsButton5.place(x = 1, y = 1)
        
        RangeButton5 = tk.Button(self, text="Range",highlightbackground='grey', command=lambda: controller.display_frame("RangeFrame"))
        RangeButton5.config(height = 1, width = 8)
        RangeButton5.place(x = 100, y = 1)

        TopKButton5 = tk.Button(self, text="Top K",highlightbackground='grey', command=lambda: controller.display_frame("TopKFrame"))    
        TopKButton5.config(height = 1, width = 8)
        TopKButton5.place(x = 200, y = 1)

        SubgraphButton5 = tk.Button(self, text="Subgraph",highlightbackground='grey', command=lambda: controller.display_frame("SubgraphFrame"))    
        SubgraphButton5.config(height = 1, width = 8)
        SubgraphButton5.place(x = 300, y = 1)

        PageRankButton5 = tk.Button(self, text="PageRank",highlightbackground='grey', command=lambda: controller.display_frame("PageRankFrame"))    
        PageRankButton5.config(height = 1, width = 8)
        PageRankButton5.place(x = 400, y = 1)

        #pagerank query frame
        pagerank_query_frame = Frame(self, height=700, width=600, bd=2, relief=GROOVE)
        pagerank_query_frame.place(x = 200, y = 45)

        #output box frame
        pagerank_output_box_frame = Frame(self, height=400, width=305, bd=2, relief=GROOVE)
        pagerank_output_box_frame.place(x = 355, y = 285)

        #input for k value label
        pagerank_value_label = tk.Label(self, text="K")
        pagerank_value_label.place(x = 500, y = 75)

        #input for k value
        pagerank_value = tk.Entry(self, width = 4)
        pagerank_value.place(x = 485, y = 100)

        #pagerank query output box
        pagerank_output = tk.Text(self,bd = 2, height = 25, width = 40)
        pagerank_output.place(x = 360, y = 290)


        def pagerank_button_action():
            uri = "bolt://localhost:7687"
            user = "neo4j"
            passw = "cpts415"

            _driver = GraphDatabase.driver(uri, auth=(user, passw))

            k = pagerank_value.get()
            query1 = 'CALL algo.pageRank.stream(\'Video\', NULL, {iterations:20, dampingFactor:0.85})\nYIELD nodeId, score\nRETURN algo.asNode(nodeId).id AS page, score\nORDER BY score DESC LIMIT ' + k + ';'

            with _driver.session() as session:
                with session.begin_transaction() as tx:
                    results = (tx.run(query1))
                session.close()

            col1 = []
            col2 = []

            for i in results:
                col1.append(i[0])
                col2.append(i[1])

            col1 = np.array(col1)
            col2 = np.array(col2)
            l = col1.shape[0]
        
            col1 = col1.reshape((l,1))
            col2 = col2.reshape((l,1))
        
            newdf = np.hstack((col1, col2))
            pagerank_output.delete(1.0, tk.END)
            pagerank_output.insert(tk.END, newdf)



        #pagerank button
        pagerank_button = tk.Button(self, text="Pagerank", command=lambda: pagerank_button_action())
        pagerank_button.config(height = 1, width = 7)
        pagerank_button.place(x = 465, y = 170)

        #pagerank query output box label
        pagerank_output_label = tk.Label(self, text="Output Pagerank")
        pagerank_output_label.place(x = 460, y = 260)

        

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


