import tkinter as tk
import os.path
from tkinter import messagebox
import pandas as pd


class GUI:
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.title("ELEC 390")

        # create a label
        self.label = tk.Label(self.window, text="Enter your CSV", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        # text box
        self.info = tk.Text(self.window, height=3, font=('Arial', 16))
        self.info.pack(padx=10, pady=10)

        # submit button
        self.btn = tk.Button(self.window, text="submit", command=self.submit)
        self.btn.place(x=225, y=200, height=50, width=50)

        # clear button
        self.clear_btn = tk.Button(self.window, text="clear", command=self.clear)
        self.clear_btn.place(x=225, y=300, height=50, width=50)

        # closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    # define submit
    def submit(self):
        path = self.info.get()
        # check path
        if not os.path.exists(path):
            messagebox.showinfo("File does not exist")
            return
        # read csv file
        # path = ?
        # data = pd.read_csv(path)
        # then do the rest of step7

    # define clear
    def clear(self):
        self.info.delete('1.0', tk.END)

    # define closing
    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="do you really want to quit?"):
            self.window.destroy()



GUI()