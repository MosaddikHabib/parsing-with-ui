import tkinter as tk
from tkinter import ttk, Canvas, TOP, LEFT, CENTER, font
from PIL import Image, ImageTk
import threading
import serial
import re
import json


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1920x1080")
        self.title("hostMate | RajIT | made for RMCH")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#222D20')

        label = tk.Label(self, text="", font=("Helvetica", 16), bg='#222D20', fg='white')
        label.pack(side="top", fill="x", pady=65)

        image_path = "res/rajIT Solution Ltd EDITED.png"
        main_image = Image.open(image_path)
        resized_image = main_image.resize((300, 75))
        self.image = ImageTk.PhotoImage(resized_image)

        label_logo_image = tk.Label(self, image=self.image, bg='#222D20')
        label_logo_image.pack(side="top", pady=30)

        input_text_username = tk.StringVar()
        userName = tk.Entry(self, width=30, textvariable=input_text_username, font=("Inter", 12), justify=LEFT, bg="white", fg="black")
        userName.pack(side=TOP, pady=10, ipady=5)
        userName.insert(0, "User name")

        input_text_password = tk.StringVar()
        userPass = tk.Entry(self, width=30, textvariable=input_text_password, show="*", font=("Inter", 12), justify=LEFT, bg="#FFFFFF", fg="black")
        userPass.pack(side=TOP, pady=10, ipady=5)
        userPass.insert(0, "Password")

        def on_enter_username(event):
            if userName.get() == "User name":
                userName.delete(0, "end")
                userName.config(fg="black")

        def on_leave_username(event):
            if userName.get() == "":
                userName.insert(0, "User name")
                userName.config(fg="gray")

        def on_enter_password(event):
            if userPass.get() == "Password":
                userPass.delete(0, "end")
                userPass.config(fg="black", show="*")

        def on_leave_password(event):
            if userPass.get() == "":
                userPass.insert(0, "Password")
                userPass.config(fg="gray", show="")

        userName.bind("<FocusIn>", on_enter_username)
        userName.bind("<FocusOut>", on_leave_username)
        userName.config(fg="gray")

        userPass.bind("<FocusIn>", on_enter_password)
        userPass.bind("<FocusOut>", on_leave_password)
        userPass.config(fg="gray", show="")

        def login():
            username = input_text_username.get()
            password = input_text_password.get()
            if (username == "a" and password == "a") or (username == "rmch" and password == "RMCH") or (username == "ITadmin" and password == "rajIT"):
                controller.show_frame("PageOne")
            else:
                label_error.config(text="Insert the Correct Constrain")


        login_image_path = "res/figma-login-BTN.png"
        btn_image = Image.open(login_image_path)
        resized_image_btn = btn_image.resize((150,42))
        self.button_image = ImageTk.PhotoImage(resized_image_btn)

        btn_login = tk.Button(self, image=self.button_image, command=login, borderwidth=0, bg='#222D20', activebackground='#222D20')
        btn_login.image = btn_image  # Keep a reference to avoid garbage collection
        btn_login.pack(pady=10)

        label_error = tk.Label(self, text="", font=("Inter", 12), bg='#222D20', fg='white')
        label_error.pack(pady=10)

        # Temp button
        button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"), font=("Inter", 12, "bold"), bg='#AD9309', fg='white')
        button2.pack(pady=5)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#222D20')

        label = tk.Label(self, text="", font=("Helvetica", 16), bg='#222D20', fg='white')
        label.pack(side="top", fill="x", pady=10)

        self.canvas = Canvas(self, bg='#FFFFFF', height=500, width=1400)
        self.canvas.pack(pady=20)

        button = ttk.Button(self, text="Go to the Start Page", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=5)

        self.serial_port = 'COM13'
        self.baud_rate = 9600

        # Start serial monitoring in a separate thread
        self.monitor_thread = threading.Thread(target=self.monitor_serial_port)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def monitor_serial_port(self):
        ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        while True:
            data = ser.read_until(b'\x04').decode('latin-1').strip()
            if data:
                parsed_data = self.parse_astm(data)
                self.display_data(parsed_data)

    def parse_astm(self, data):
        sample_id_match = re.search(r'O\|\d+\|\d+\^([\w\d]+)\s*\^', data)
        sample_id = sample_id_match.group(1) if sample_id_match else None

        # datetime_match = re.search(r'\|\|(\d{8})(\d{6})\|', data)
        # datetime_str = datetime_match.group(1) + datetime_match.group(2) if datetime_match else None

        test_results = re.findall(r'R\|\d+\|\^\^\^(\d+)/\|([\d\.]+)\|([\w/]+)', data)
        results = [{"test_no": res[0], "result_with_unit": f"{res[1]} {res[2]}"} for res in test_results]

        # return {"sample_id": sample_id, "datetime": datetime_str, "results": results}
        return {"sample_id": sample_id, "results": results}

    def display_data(self, parsed_data):
        self.canvas.delete("all")
        y = 20
        for result in parsed_data['results']:
            self.canvas.create_text(10, y, anchor="nw", text=f"{result['test_no']}: {result['result_with_unit']}", fill="white")
            y += 20


class PageTwo (tk.Frame):
    def __init__(self, parent, controller):
        super ().__init__ (parent)
        self.controller = controller
        self.configure (bg='#222D20')

        label_bold_font = font.Font (family="Inter", size=25, weight="bold")
        label = tk.Label (self, text="Communication Parameter", font=label_bold_font, bg='#222D20', fg='#FFFFFF')
        label.pack (pady=20)

        style = ttk.Style ()
        style.configure ("Green.TFrame", background="#222D20")  # Change the background color to match the frame

        frame = ttk.Frame (self, width=300, height=100, padding="10", style="Green.TFrame")
        frame.pack_propagate (False)  # Prevent the frame from resizing to fit its content
        frame.pack (padx=10, pady=10)

        # COM - Port - Selection Sector----------------------------------------
        com_port_button_image = "res/COM Port.png"
        img_open = Image.open (com_port_button_image)
        res_com_port_img = img_open.resize ((100, 30))
        self.comImg = ImageTk.PhotoImage (res_com_port_img)

        image_label = tk.Label (frame, image=self.comImg, bg="#222D20")
        image_label.grid (row=0, column=0, padx=(0, 5), pady=5, sticky="ew")

        # Create the input field
        com_port_input = ttk.Entry (frame, width=35, font=('Inter', 16))
        com_port_input.grid (row=0, column=1, padx=(5, 0), pady=5)


        # Baudrate selection-----------------------------------------------
        baud_rate_button_image = "res/Baud Rate.png"
        img_open = Image.open (baud_rate_button_image)
        res_baud_rate_img = img_open.resize ((100, 30))
        self.baudRateImg = ImageTk.PhotoImage (res_baud_rate_img)

        image_label = tk.Label (frame, image=self.baudRateImg, bg="#222D20")
        image_label.grid (row=1, column=0, padx=(0, 5), pady=5, sticky="ew")

        # Create the combobox for baud rate selection
        baud_rate_options = ["9600", "19200", "38400", "57600"]
        baud_rate_combobox = ttk.Combobox (frame, values=baud_rate_options, font=('Inter', 16), state="readonly",width=34)
        baud_rate_combobox.grid (row=1, column=1, padx=(5, 0), pady=5)
        baud_rate_combobox.current (0)  # Set default selection to the first item

        # Increase the font size of the dropdown list
        self.option_add ('*TCombobox*Listbox.font', ('Inter', 16))

        # create the combobox for dataBits selection--------------------------------
        dataBits_button_image = 'res/dataBits.png'
        img_open = Image.open (dataBits_button_image)
        dataBits_resize_img = img_open.resize ((100, 30))
        self.dataBitsImg = ImageTk.PhotoImage (dataBits_resize_img)

        image_label = tk.Label (frame, image=self.dataBitsImg, bg="#222D20")
        image_label.grid (row=2, column=0, padx=(0, 5), pady=5, sticky="ew")

        # Create the combobox for dataBit selection
        dataBit_options = ["8", "7"]
        dataBit_combobox = ttk.Combobox (frame, values=dataBit_options, font=('Inter', 16), state="readonly",
                                           width=34)
        dataBit_combobox.grid (row=2, column=1, padx=(5, 0), pady=5)
        dataBit_combobox.current (0)  # Set default selection to the first item

        # create the combobox for parityBit selection--------------------------------
        parityBit_image = 'res/ParityBits.png'
        img_open = Image.open (parityBit_image)
        parityBit_resize_img = img_open.resize ((100, 30))
        self.parityBitImg = ImageTk.PhotoImage (parityBit_resize_img)

        image_label = tk.Label (frame, image=self.parityBitImg, bg="#222D20")
        image_label.grid (row=3, column=0, padx=(0, 5), pady=5, sticky="ew")

        # Create the combobox for parityBit selection
        parityBit_options = ["EVEN", "ODD", "NONE"]
        parityBit_combobox = ttk.Combobox (frame, values=parityBit_options, font=('Inter', 16), state="readonly",
                                         width=34)
        parityBit_combobox.grid (row=3, column=1, padx=(5, 0), pady=5)
        parityBit_combobox.current (0)  # Set default selection to the first item


        # to go to the start page___________________________________________________
        button = ttk.Button (self, text="Go to the Start Page",
                             command=lambda: controller.show_frame ("StartPage"))
        button.pack (pady=5)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
