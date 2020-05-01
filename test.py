import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import ttk

class Main:
    def __init__(self, master):
        global conf_window
        conf_window = None
        self.master = master
        self.master.title("Mac Fan Control")
        self.master.geometry("300x300+700+500")
        self.button1 = ttk.Button(self.master, text="Click me!", command=self.open_conf)
        self.button1.pack(anchor="se")
    def open_conf(self):
        global conf_window
        if not conf_window:
            conf_window = Conf_Window(self.master)
        else:
            conf_window.focus()

class Conf_Window(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.group(master)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<FocusIn>", self.set_focus)
        self.title("Conf Window")
        self.geometry("375x300+300+500")

        self.labels_frame = ttk.Frame(self)
        # self.labels_frame['pady'] = 5
        #self.labels_frame['padx'] = 10
        #self.labels_frame['width'] = 290
        #self.labels_frame['borderwidth'] = 2
        self.labels_frame.grid(row=0, column=0, sticky="N")

        self.low_temp_label = ttk.Label(self.labels_frame, text="Low\nTemp")
        self.low_temp_label.grid(row=0, column=0, sticky="W")
        self.rpm_label = ttk.Label(self.labels_frame, text="RPM")
        self.rpm_label.grid(row=0, column=1, sticky="N")
        self.high_temp_label = ttk.Label(self.labels_frame, text="High\nTemp")
        self.high_temp_label.grid(row=0, column=2, sticky="E")

        self.values_frame = ttk.Frame(self)
        self.values_frame.grid(row=1, column=0, sticky="N")

        self.conf_frame = ttk.Frame(self)
        self.conf_frame.grid(row=2, column=0, sticky="N")

        self.save_conf_button = ttk.Button(self.conf_frame, text="Save Config", command=lambda: print("Needs work.."))
        self.save_conf_button.grid(row=0, column=0, sticky="SW")
        self.load_conf_button = ttk.Button(self.conf_frame, text="Load Config", command=self.load_conf)
        self.load_conf_button.grid(row=0, column=1, sticky="SE")


    def load_conf(self):
        conf_file = askopenfilename(filetypes=[("Config files", "*.csv"), ("All files", "*.*")])
        try:
            if conf_file == () or conf_file == "":
                print("Canceled file selection.")
                pass
            elif conf_file.endswith("csv"):
                print(conf_file.split("/")[-1])
                messagebox.showinfo(title="Config Loaded", message="Configuration loaded successfully")
            else:
                raise AttributeError("Wrong file type.")
        except AttributeError as file_error:
            print(f"File Error: {file_error}\nInvalid file: {conf_file}")
            messagebox.showerror(title="Config Error", message="Invalid configuration file!")
            conf_file = None
    def set_focus(self, event):
        self.master.focus()
        # self.focus() this was an AWFUL mistake
    def on_closing(self):
        global conf_window
        conf_window = None
        self.destroy()

root = tk.Tk()
main = Main(root)
root.mainloop()
