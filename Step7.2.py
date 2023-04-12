import tkinter as tk
import os.path
from tkinter import messagebox
import pandas as pd
import numpy as np
from tkinter import filedialog
import joblib
import dill as pickle
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

class GUI:
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        self.window.geometry("1000x500")
        self.window.title("ELEC 390 - Project")

        # text box
        # self.info = tk.Text(self.window, height=3, font=('Arial', 16))
        # self.info.pack(padx=10, pady=10)

        # create label
        self.label = tk.Label(self.window, text="To start the app, please choose start", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        # start button
        self.btn = tk.Button(self.window, text="Start", command=self.start)
        self.btn.place(x=225, y=200, height=50, width=50)

        # clear button
        # self.clear_btn = tk.Button(self.window, text="clear", command=self.clear)
        # self.clear_btn.place(x=225, y=300, height=50, width=50)

        # closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)


        # create label
        self.label = tk.Label(self.window, text="Please choose Instructions to view the instruction", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        # text button
        self.textbtn = tk.Button(self.window, text="Instructions", command=self.message)
        self.textbtn.place(x=215, y=400, height=50, width=70)
        
        self.window.mainloop()

    # define read path
    def file_path(self):
        file_path = filedialog.askopenfilename()
        return file_path
    
    # def plot(self, y, data):
    #     fig, ax = plt.subplots(figsize=(5,5), dpi=100)
    #     ax.plot(y, linewidth=1)
    #     ax.plot(data.iloc[:,1], linewidth=1)
    #     ax.plot(data.iloc[:,2], linewidth=1)
    #     ax.plot(data.iloc[:,3], linewidth=1)
    #     self.canvas = FigureCanvasTkAgg(fig, master = self.window)
    #     self.canvas.draw()
        
    #     # placing the canvas on the Tkinter window
    #     self.canvas.get_tk_widget().place(x=350, y=150, height=350, width=500)
    def plot(self, labels, data):
        colour = []
        # for i in range(len(data) - len(labels)):
        #     colour.append("red")
        for x in labels:
            if x == 1:
                colour.append("blue")
            else:
                colour.append("red")
        print(labels)
        print(labels.dtype)
        x = range(len(labels))
        fig, ax = plt.subplots(figsize=(5,5), dpi=100)
        ax.scatter(x, data.iloc[-len(labels):,1], linewidth=1, c=colour, s=1)
        ax.scatter(x, data.iloc[-len(labels):,2], linewidth=1, c=colour, s=1)
        ax.scatter(x, data.iloc[-len(labels):,3], linewidth=1, c=colour, s=1)
        self.canvas = FigureCanvasTkAgg(fig, master = self.window)
        self.canvas.draw()
        
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().place(x=350, y=150, height=350, width=500)
            
    # define start
    def start(self):
        # define input
        input_path = self.file_path()
        # check
        if not input_path:
            return
        data = pd.read_csv(input_path)
        prediction = model.predict(preprocessing_features(data).features)
        prob = model.predict_proba(preprocessing_features(data).features)
        self.plot(prediction, data)
        print(prob)
        # fig, ax = plt.subplots(figsize=(10,10))
        # ax.plot(prediction, linewidth=5)
        # plt.show()


    # define closing
    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="do you really want to quit?"):
            self.window.destroy()

    # define text
    def message(self):
        messagebox.showinfo("Message", "this app will accept an input file in CSV format "
                                       "and generate a CSV file as the output"
                                       "in the plot red represents walking and blue is jumping")


model = joblib.load('E:\\Desktop\\390\\ELEC-390-Project\\log_reg_model.pkl')
with open('E:\\Desktop\\390\\ELEC-390-Project\\preprocessing_features.pkl', 'rb') as file:
    preprocessing_features = pickle.load(file)
GUI()