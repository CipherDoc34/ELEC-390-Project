import tkinter as tk
import os.path
from tkinter import messagebox
import pandas as pd
from tkinter import filedialog


class GUI:
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.title("ELEC 390")

        # text box
        # self.info = tk.Text(self.window, height=3, font=('Arial', 16))
        # self.info.pack(padx=10, pady=10)

        # create label
        self.label = tk.Label(self.window, text="To start the APP, please choose start", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        # start button
        self.btn = tk.Button(self.window, text="start", command=self.start)
        self.btn.place(x=225, y=200, height=50, width=50)

        # clear button
        # self.clear_btn = tk.Button(self.window, text="clear", command=self.clear)
        # self.clear_btn.place(x=225, y=300, height=50, width=50)

        # closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)


        # create label
        self.label = tk.Label(self.window, text="Please choose instr to view the instruction", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        # text button
        self.textbtn = tk.Button(self.window, text="instr", command=self.message)
        self.textbtn.place(x=225, y=400, height=50, width=50)

        self.window.mainloop()

    # define read path
    def file_path(self):
        file_path = filedialog.askopenfilename()
        return file_path

    # define start
    def start(self):
        # define input
        input_path = self.file_path()
        # check
        if not input_path:
            return
        data = pd.read_csv(input_path)
        print(data)
        # path = self.info.get()
        # # check path
        # if not os.path.exists(path):
        #     messagebox.showinfo("File does not exist")
        #     return
        # # read csv file
        # # path = ?
        # # data = pd.read_csv(path)
        # # then do the rest of step7

    # define clear
    # def clear(self):
    #     self.info.delete('1.0', tk.END)

    # define closing
    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="do you really want to quit?"):
            self.window.destroy()

    # define text
    def message(self):
        messagebox.showinfo("Message", "this app will accept an input file in CSV format "
                                       "and generate a CSV file as the output")



GUI()