import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from tkinter import filedialog
import joblib
import dill as pickle
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
import requests
from tkinter import StringVar
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import os
import numpy as np

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.wm_title(self, "APP")
        self.geometry("1000x800")
        self.title("ELEC 390 - Project")
        self.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (CSV, LiveData, Instructions):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(CSV)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class CSV(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label = tk.Label(self, text="Start Page")
        # label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="LIVE",
                            command=lambda: controller.show_frame(LiveData))
        # button.pack()
        button.place(x=225, y=300, height=50, width=50)

        # create label
        self.label = tk.Label(self, text="To start the app, please choose start", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        # start button
        self.btn = ttk.Button(self, text="Start", command=self.start)
        self.btn.place(x=225, y=200, height=50, width=50)
        
        tk.Label(self, text="Choose Live to use live data from Phyphox",
                              font=('Arial', 18)).pack()

        # create label
        self.label = tk.Label(self, text="Please choose Instructions to view the instruction",
                              font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        # text button
        self.textbtn = ttk.Button(self, text="Instructions", command=lambda: controller.show_frame(Instructions))
        self.textbtn.place(x=215, y=400, height=50, width=75)
        # ttk.Button(self, text="Live", command=self.open_window).place(x=215, y=300, height=50, width=70)

    # def open_window(self):
    #     window = LiveData(self)
    #     window.grab_set()

    # define read path
    def file_path(self):
        file_path = filedialog.askopenfilename()
        return file_path
    def plot(self, labels, data):
        colour = []
        for x in labels:
            if x == 1:
                colour.append("blue")
            else:
                colour.append("red")
        x = range(len(labels))
        fig1, ax1 = plt.subplots(figsize=(5, 5), dpi=100)
        ax1.scatter(x, data.iloc[-len(labels):, 1], linewidth=1, c=colour, s=1)
        ax1.scatter(x, data.iloc[-len(labels):, 2], linewidth=1, c=colour, s=1)
        ax1.scatter(x, data.iloc[-len(labels):, 3], linewidth=1, c=colour, s=1)
        canvas = FigureCanvasTkAgg(fig1, master=self)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().place(x=350, y=200, height=350, width=500)
        toolbar = NavigationToolbar2Tk(canvas, self, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    # define start
    def start(self):
        # define input
        input_path = self.file_path()
        # check
        if not input_path:
            return
        data = pd.read_csv(input_path)
        # print(data)
        prediction = model.predict(preprocessing_features(data).features)
        prob = model.predict_proba(preprocessing_features(data).features)
        self.plot(prediction, data)
        data = data.drop(range(499), axis=0)
        data["prediction"] = prediction
        data.to_csv(input_path[:-4] + "_prediction.csv", index=False)
        # print(prob)
        # fig, ax = plt.subplots(figsize=(10,10))
        # ax.plot(prediction, linewidth=5)
        # plt.show()

    # define closing
    def on_closing(self):
        # if messagebox.askyesno(title="Quit?", message="do you really want to quit?"):
        self.destroy()

    # def message(self):
    #     window = Instructions(self)
    #     window.grab_set()
        # messagebox.showinfo("Message", "this app will accept an input file in CSV format "
        #                                "and generate a CSV file as the output"
        #                                "in the plot red represents walking and blue is jumping")


class LiveData(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Current Activity:")
        label.pack()
        self.var = StringVar()
        self.var.set('NO DATA')
        l = tk.Label(self, textvariable=self.var)
        l.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                             command=self.home)
        button1.pack()
        self.f, (self.ax, self.ay, self.az) = plt.subplots(3, 1)
        # self.plot = PauseAnimation(self.f, self.ax, self.ay, self.az, "192.168.50.110:8080")
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        ttk.Button(self,
                       text='Start',
                       command=self.Start).pack()
        self.label = ttk.Label(self, text="IP Address")
        self.entry = ttk.Entry(self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.label.pack()
        self.entry.pack()
    def Start(self):
        self.plot = AnimationGraph(self.f, self.ax, self.ay, self.az, self.entry.get(), self.var, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        ttk.Button(self, text="Pause/Play",
                             command=lambda: self.plot.toggle_pause()).pack()
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    def home(self):
        if(not self.plot.paused):
            self.plot.toggle_pause()
        self.controller.show_frame(CSV)
        
class Instructions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Instructions")
        label.pack(pady=10, padx=10)
        l = tk.Label(self, text="This app will accept an input file in CSV format "
                                       "and generate a CSV file as the output"
                                       "in the plot red represents walking and blue is jumping.\n"
                                       "If you press live, you can use the model on live data. "
                                       "you need to have Phypox open and running (also allow remote access) \n"
                                       "finally type in the IP address Phyphox gives you (xxx.xxx.xxx.xxx:xxxx) "
                                       "and press start.")
        l.pack()
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(CSV))
        button1.pack()

class AnimationGraph:
    def __init__(self, fig, ax, ay, az, addr, var, root):
        self.X = []
        self.Y = []
        self.Z = []
        self.time = []
        self.fig = fig
        self.ax = ax
        self.ay = ay
        self.az = az
        self.addr = addr
        self.Xpart = []
        self.Ypart = []
        self.Zpart = []
        self.timepart = []
        self.flag = 0
        self.var = var
        self.root = root
        self.ax.plot(1, 1, linewidth=1, color="red")
        self.ay.plot(1, 1, linewidth=1, color="blue")
        self.az.plot(1, 1, linewidth=1, color="green")
        self.animation = animation.FuncAnimation(
            self.fig, self.update, frames=200, interval=50)
        self.paused = False

        # self.fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused

    def update(self, i):
        if not self.paused:
            attributes = 'accX&accY&accZ&acc_time'
            r = requests.get("http://"+self.addr+"/get?" + attributes)
            json = r.json()
            if (len(json)):
                t = json["buffer"]["acc_time"]["buffer"][0]
                accx = json["buffer"]["accX"]["buffer"][0]
                accy = json["buffer"]["accY"]["buffer"][0]
                accz = json["buffer"]["accZ"]["buffer"][0]

                if (int(t) % 5 == 0 and not self.flag):
                    flag = 1
                    data = pd.DataFrame(columns=["time", "x", "y", "z", "acc"])
                    data["time"] = self.timepart
                    data["x"] = self.Xpart
                    data["y"] = self.Ypart
                    data["z"] = self.Zpart
                    self.Xpart = []
                    self.Ypart = []
                    self.Zpart = []
                    self.timepart = []
                    # print(data)
                    if(len(data)>10):
                        features = preprocessing_features_bonus(data).features
                        # print(features)
                        prediction = model.predict(features)
                        if(round(prediction.mean(), 0)):
                            print(prediction.mean())
                            self.var.set("Jumping")
                            self.root.update_idletasks()
                        else:
                            print(prediction.mean())
                            self.var.set("Walking")
                            self.root.update_idletasks()

                elif (int(t) % 5 != 0):
                    self.flag = 0
                self.X.append(accx)
                self.Y.append(accy)
                self.Z.append(accz)
                self.time.append(t)
                self.Xpart.append(accx)
                self.Ypart.append(accy)
                self.Zpart.append(accz)
                self.timepart.append(t)

            else:
                return
            self.ax.clear()
            self.ay.clear()
            self.az.clear()
            self.ax.plot(self.time, self.X, linewidth=1, color="red")
            self.ay.plot(self.time, self.Y, linewidth=1, color="blue")
            self.az.plot(self.time, self.Z, linewidth=1, color="green")
        else:
            return

model = joblib.load('log_reg_model.pkl')
with open(os.getcwd()+'\\preprocessing_features.pkl', 'rb') as file:
    preprocessing_features = pickle.load(file)
with open(os.getcwd()+'\\preprocessing_features_bonus.pkl', 'rb') as file:
    preprocessing_features_bonus = pickle.load(file)
gui = GUI()
gui.mainloop()
os.exit(0)