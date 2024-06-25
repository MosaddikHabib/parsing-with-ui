import tkinter as tk
from tkinter import ttk, CENTER, TOP, LEFT
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the window size and title
        self.geometry("1920x1080")
        # self.geometry("600x450")

        self.title("hostMate | RajIT | made for RMCH")

        # Create a container for all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Configure the grid to expand
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold the different frames
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

        # image_path = "res/l01.png"
        # main_image = Image.open(image_path)
        # resized_image = main_image.resize((300, 170))
        # self.image = ImageTk.PhotoImage(resized_image)
        #
        image_path = "res/rajIT Solution Ltd EDITED.png"
        main_image = Image.open(image_path)
        resized_image = main_image.resize ((300, 75))
        self.image = ImageTk.PhotoImage(resized_image)

        # image_path = "res/logo 1logo.png"
        # main_image = Image.open(image_path)
        # resized_image = main_image.resize ((300, 100))
        # self.image = ImageTk.PhotoImage(resized_image)

        label_logo_image = tk.Label(self, image=self.image, bg='#222D20')
        label_logo_image.pack(side="top", pady=30)

        input_text_username = tk.StringVar()
        userName = tk.Entry(self, width=30, textvariable=input_text_username, font=("Inter", 12), justify=LEFT, bg="#D9D9D9", fg="black")
        userName.pack(side=TOP, pady=10, ipady=5)

        input_text_password = tk.StringVar()
        userPass = tk.Entry(self, width=30, textvariable=input_text_password, show="*", font=("Inter", 12), justify=LEFT, bg="#D9D9D9", fg="black")
        userPass.pack(side=TOP, pady=10, ipady=5)

        btn_login = tk.Button(self, text="Log In", width=8, command=lambda: controller.show_frame("PageOne"), font=("Inter", 12, "bold"), bg='#AD9309', fg='white')
        btn_login.pack(pady=10)

        label = tk.Label (self, text="Insert the Correct Constrain", font=("Inter", 12), bg='#222D20', fg='white')
        label.pack (pady=65)

        # button1 = tk.Button(self, text="Go to Page One", command=lambda: controller.show_frame("PageOne"), font=("Inter", 12, "bold"), bg='#AD9309', fg='white')
        # button1.pack(pady=5)
        #
        button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"), font=("Inter", 12, "bold"), bg='#AD9309', fg='white')
        button2.pack(pady=5)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#222D20')

        label = tk.Label(self, text="Page One", font=("Helvetica", 16), bg='#222D20', fg='white')
        label.pack(side="top", fill="x", pady=10)

        button = ttk.Button(self, text="Go to the Start Page",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=5)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#A22F20')

        # label = tk.Label(self, text="Page Two", font=("Helvetica", 16), bg='#222D20', fg='white')
        label = tk.Label(self, text="Page Two", font=("Helvetica", 16))
        label.pack()
        # label.pack(side="top", fill="x", pady=10)


        button = ttk.Button(self, text="Go to the Start Page",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=5)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
