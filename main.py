# Md. Mosaddik Habib >> From 25th June
import tkinter as tk
from tkinter import ttk, Canvas, TOP, LEFT, CENTER, font, messagebox
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
        userName = tk.Entry(self, width=30, textvariable=input_text_username, font=("Inter", 12), justify=LEFT,
                             bg="white", fg="black")
        userName.pack(side=TOP, pady=10, ipady=5)
        userName.insert(0, "User name")

        input_text_password = tk.StringVar()
        userPass = tk.Entry(self, width=30, textvariable=input_text_password, show="*", font=("Inter", 12),
                             justify=LEFT, bg="#FFFFFF", fg="black")
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
            if (username == "a" and password == "a") or (username == "rmch" and password == "RMCH"):
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

        self.canvas = tk.Canvas(self, bg='#FFFFFF', height=500, width=1400)
        self.canvas.pack(pady=20)

        button = ttk.Button(self, text="Go to the Start Page", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=5)

        self.serial_port = None
        self.baud_rate = None
        self.data_bits = None
        self.parity = None
        self.stop_bits = None

        # Delay starting the serial monitoring thread
        self.after(1000, self.start_serial_monitoring)

    def start_serial_monitoring(self):
        # Get the parameters from the controller
        params = self.controller.serial_params
        self.serial_port = params["com_port"]
        self.baud_rate = int(params["baud_rate"])
        self.data_bits = int(params["data_bits"])
        self.parity = params["parity"]
        self.stop_bits = int(params["stop_bits"])

        # Convert parity string to serial module constant
        parity_dict = {"EVEN": serial.PARITY_EVEN, "ODD": serial.PARITY_ODD, "NONE": serial.PARITY_NONE}
        self.parity = parity_dict[self.parity]

        self.monitor_thread = threading.Thread(target=self.monitor_serial_port)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def monitor_serial_port(self):
        ser = serial.Serial(
            port=self.serial_port,
            baudrate=self.baud_rate,
            bytesize=self.data_bits,
            parity=self.parity,
            stopbits=self.stop_bits,
            timeout=1
        )
        while True:
            data = ser.read_until(b'\x04').decode('latin-1').strip()
            if data:
                parsed_data = self.parse_astm(data)
                self.display_data(parsed_data)

    def parse_astm(self, data):
        sample_id_match = re.search(r'O\|\d+\|\d+\^([\w\d]+)\s*\^', data)
        sample_id = sample_id_match.group(1) if sample_id_match else None

        test_results = re.findall(r'R\|\d+\|\^\^\^(\d+)/\|([\d\.]+)\|([\w/]+)', data)
        results = [{"test_no": res[0], "result_with_unit": f"{res[1]} {res[2]}"} for res in test_results]

        return {"sample_id": sample_id, "results": results}

    def display_data(self, parsed_data):
        self.canvas.delete ("all")
        y = 20
        for result in parsed_data['results']:
            self.canvas.create_text (10, y, anchor="nw", text=f"{result['test_no']}: {result['result_with_unit']}", fill="black")
            y += 20


# additional classes to save parameters====================================================================
def load_serial_params():
    try:
        with open("serial_params.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Default parameters if file is not found or corrupted
        return {
            "com_port": "COM13",
            "baud_rate": "9600",
            "data_bits": "8",
            "parity": "NONE",
            "stop_bits": "1"
        }


def save_serial_params(params):
    with open("serial_params.json", "w") as f:
        json.dump(params, f)


# active start Page --------
class Controller(tk.Tk):
    def __init__(self):
        super().__init__()

        self.serial_params = load_serial_params()

        self.title("Serial Communication Monitor")
        self.geometry("1000x500")
        self.resizable(True, True)

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

    def update_serial_params(self, params):
        self.serial_params.update(params)
        save_serial_params(self.serial_params)
# ==============================


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#222D20')

        label_bold_font = font.Font(family="Inter", size=25, weight="bold")
        label = tk.Label(self, text="Communication Parameter", font=label_bold_font, bg='#222D20', fg='#FFFFFF')
        label.pack(pady=20)

        style = ttk.Style ()
        style.configure ("Green.TFrame", background="#222D20")
        style.configure ("StartPage.TButton", background='#AD9309', foreground='white', font=("Inter", 12, "bold"))
        style.configure ("PageTwoBack.TButton", font=("Inter", 12, "bold"), background='#0A717E', foreground='black')
        style.configure ("PageTwoSave.TButton", background='#FF5733', foreground='black', font=("Inter", 12, "bold"))

        frame = ttk.Frame(self, width=300, height=100, padding="10", style="Green.TFrame")
        frame.pack_propagate(False)
        frame.pack(padx=10, pady=10)

        # COM - Port - Selection Sector
        com_port_button_image = "res/COM Port.png"
        img_open = Image.open(com_port_button_image)
        res_com_port_img = img_open.resize((100, 30))
        self.comImg = ImageTk.PhotoImage(res_com_port_img)

        image_label = tk.Label(frame, image=self.comImg, bg="#222D20")
        image_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")

        self.com_port_input = ttk.Entry(frame, width=35, font=('Inter', 16))
        self.com_port_input.grid(row=0, column=1, padx=(5, 0), pady=5)
        self.com_port_input.insert(0, controller.serial_params["com_port"])

        # Baudrate selection
        baud_rate_button_image = "res/Baud Rate.png"
        img_open = Image.open(baud_rate_button_image)
        res_baud_rate_img = img_open.resize((100, 30))
        self.baudRateImg = ImageTk.PhotoImage(res_baud_rate_img)

        image_label = tk.Label(frame, image=self.baudRateImg, bg="#222D20")
        image_label.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="ew")

        baud_rate_options = ["1200","2400","4800","9600", "19200", "38400", "57600"]
        self.baud_rate_combobox = ttk.Combobox(frame, values=baud_rate_options, font=('Inter', 16), state="readonly", width=34)
        self.baud_rate_combobox.grid(row=1, column=1, padx=(5, 0), pady=5)
        self.baud_rate_combobox.set(controller.serial_params["baud_rate"])

        self.option_add('*TCombobox*Listbox.font', ('Inter', 16))

        # Data Bits selection
        dataBits_button_image = 'res/dataBits.png'
        img_open = Image.open(dataBits_button_image)
        dataBits_resize_img = img_open.resize((100, 30))
        self.dataBitsImg = ImageTk.PhotoImage(dataBits_resize_img)

        image_label = tk.Label(frame, image=self.dataBitsImg, bg="#222D20")
        image_label.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="ew")

        dataBit_options = ["8", "7"]
        self.dataBit_combobox = ttk.Combobox(frame, values=dataBit_options, font=('Inter', 16), state="readonly", width=34)
        self.dataBit_combobox.grid(row=2, column=1, padx=(5, 0), pady=5)
        self.dataBit_combobox.set(controller.serial_params["data_bits"])

        # Parity Bits selection
        parityBit_image = 'res/ParityBits.png'
        img_open = Image.open(parityBit_image)
        parityBit_resize_img = img_open.resize((100, 30))
        self.parityBitImg = ImageTk.PhotoImage(parityBit_resize_img)

        image_label = tk.Label(frame, image=self.parityBitImg, bg="#222D20")
        image_label.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="ew")

        parityBit_options = ["EVEN", "ODD", "NONE"]
        self.parityBit_combobox = ttk.Combobox(frame, values=parityBit_options, font=('Inter', 16), state="readonly", width=34)
        self.parityBit_combobox.grid(row=3, column=1, padx=(5, 0), pady=5)
        self.parityBit_combobox.set(controller.serial_params["parity"])

        # Stop Bits selection
        stopBit_image = 'res/stopBit.png'
        img_open = Image.open(stopBit_image)
        stopBit_resize_img = img_open.resize((100, 30))
        self.stopBitImg = ImageTk.PhotoImage(stopBit_resize_img)

        image_label = tk.Label(frame, image=self.stopBitImg, bg="#222D20")
        image_label.grid(row=4, column=0, padx=(0, 5), pady=5, sticky="ew")

        stopBit_options = ["1", "2"]
        self.stopBit_combobox = ttk.Combobox(frame, values=stopBit_options, font=('Inter', 16), state="readonly", width=34)
        self.stopBit_combobox.grid(row=4, column=1, padx=(5, 0), pady=5)
        self.stopBit_combobox.set(controller.serial_params["stop_bits"])


        # Save and Back buttons----------------------------------------
        button_frame = ttk.Frame(self, style="Green.TFrame")
        button_frame.pack(pady=10)

        save_button = ttk.Button (button_frame, text="Save", command=self.save_params, style="PageTwoSave.TButton")
        save_button.pack (side=tk.LEFT, padx=5, pady=10)

        back_button = ttk.Button (button_frame, text="Back", command=lambda: controller.show_frame ("PageOne"),
                                  style="PageTwoBack.TButton")
        back_button.pack (side=tk.LEFT, padx=5, pady=10)

        # Button to go to the start page
        button = ttk.Button(self, text="Go to the Start Page", command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=5)

    def save_params(self):
        params = {
            "com_port": self.com_port_input.get(),
            "baud_rate": self.baud_rate_combobox.get(),
            "data_bits": self.dataBit_combobox.get(),
            "parity": self.parityBit_combobox.get(),
            "stop_bits": self.stopBit_combobox.get()
        }
        self.controller.update_serial_params(params)
        messagebox.showinfo("Info", "Communication parameters saved successfully.")


if __name__ == "__main__":
    app = Controller()
    app.mainloop()

