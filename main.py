import tkinter as tk
from tkinter import ttk, CENTER, TOP, LEFT
# import ttkbootstrap as ttk
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the window size and title
        self.geometry("1920x1080")
        self.title("Multi-Page Tkinter App")

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

class RoundButton(tk.Canvas):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, width=200, height=50, bg='#222D20', highlightthickness=0)
        self.command = command
        self.text = text
        self.radius = 10  # Radius for rounded corners

        # Draw rounded rectangle
        self.create_oval(0, 0, 2*self.radius, 2*self.radius, outline='#AD9309', fill='#AD9309')
        self.create_oval(200-2*self.radius, 0, 200, 2*self.radius, outline='#AD9309', fill='#AD9309')
        self.create_oval(0, 50-2*self.radius, 2*self.radius, 50, outline='#AD9309', fill='#AD9309')
        self.create_oval(200-2*self.radius, 50-2*self.radius, 200, 50, outline='#AD9309', fill='#AD9309')
        self.create_rectangle(self.radius, 0, 200-self.radius, 50, outline='#AD9309', fill='#AD9309')
        self.create_rectangle(0, self.radius, 200, 50-self.radius, outline='#AD9309', fill='#AD9309')

        # Add text
        self.create_text(100, 25, text=text, fill='white', font=("Inter", 12, "bold"))

        self.bind("<Button-1>", lambda e: command())

    def set_text(self, new_text):
        self.text = new_text
        self.create_text(100, 25, text=new_text, fill='white', font=("Inter", 12, "bold"))

    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, width=200, height=50, bg='#222D20', highlightthickness=0)
        self.command = command
        self.text = text
        self.radius = 25  # Radius for rounded corners

        self.create_oval(0, 0, 50, 50, outline='#AD9309', fill='#AD9309')
        self.create_oval(150, 0, 200, 50, outline='#AD9309', fill='#AD9309')
        self.create_rectangle(25, 0, 175, 50, outline='#AD9309', fill='#AD9309')
        self.create_text(100, 25, text=text, fill='white', font=("Inter", 12, "bold"))

        self.bind("<Button-1>", lambda e: command())

    def set_text(self, new_text):
        self.text = new_text
        self.create_text(100, 25, text=new_text, fill='white', font=("Inter", 12, "bold"))

class RoundEntry(tk.Canvas):
    def __init__(self, parent, textvariable, **kwargs):
        super().__init__(parent, width=480, height=50, bg='#222D20', highlightthickness=0)
        self.textvariable = textvariable

        self.create_oval(0, 0, 50, 50, outline='#AD9309', fill='white')
        self.create_oval(430, 0, 480, 50, outline='#AD9309', fill='white')
        self.create_rectangle(25, 0, 455, 50, outline='#AD9309', fill='white')

        self.entry = tk.Entry(self, textvariable=textvariable, bd=0, font=("Inter", 12), justify=LEFT, **kwargs)
        self.create_window(240, 25, window=self.entry, width=440, height=40)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#222D20')

        label = tk.Label(self, text="Start Page", font=("Helvetica", 16), bg='#222D20', fg='white')
        label.pack(side="top", fill="x", pady=10)

        image_path = "res/l01.png"
        main_image = Image.open(image_path)
        resized_image = main_image.resize((300, 170))
        self.image = ImageTk.PhotoImage(resized_image)

        label_logo_image = tk.Label(self, image=self.image, bg='#222D20')
        label_logo_image.pack(side="top", pady=20)

        input_text_username = tk.StringVar()
        userName = RoundEntry(self, textvariable=input_text_username)
        userName.pack(side=TOP, pady=10)

        input_text_password = tk.StringVar()
        userPass = RoundEntry(self, textvariable=input_text_password, show="*")
        userPass.pack(side=TOP, pady=10)

        btn_login = RoundButton(self, text="Log In", command=lambda: controller.show_frame("PageOne"))
        btn_login.pack(pady=10)

        button1 = RoundButton(self, text="Go to Page One", command=lambda: controller.show_frame("PageOne"))
        button1.pack(pady=5)

        button2 = RoundButton(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"))
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
        self.configure(bg='#222D20')

        label = tk.Label(self, text="Page Two", font=("Helvetica", 16), bg='#222D20', fg='white')
        label.pack(side="top", fill="x", pady=10)

        button = ttk.Button(self, text="Go to the Start Page",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=5)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
