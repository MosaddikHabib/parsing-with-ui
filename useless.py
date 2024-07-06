import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json


# Connect to SQLite database
def connect_to_database():
    try:
        connection = sqlite3.connect('habib04.db')
        print("Connection OK !!!!!!")
        return connection
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None


connection = connect_to_database()


class ASTMApp:
    def __init__(self, parent):
        self.parent = parent

        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.search_label = ttk.Label(self.frame, text="Search Sample ID:")
        self.search_label.pack(pady=5)

        self.search_entry = ttk.Entry(self.frame)
        self.search_entry.pack(pady=5)

        self.search_button = ttk.Button(self.frame, text="Search", command=self.search_data)
        self.search_button.pack(pady=5)

        self.load_button = ttk.Button(self.frame, text="Load All Data", command=self.load_data)
        self.load_button.pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("sample_id", "test_no", "result_with_unit"), show="headings")
        self.tree.heading("sample_id", text="Sample ID")
        self.tree.heading("test_no", text="Test No")
        self.tree.heading("result_with_unit", text="Result with Unit")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_data(self):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM astm_data")
            records = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())  # Clear existing data

            for record in records:
                sample_id = record[1]
                json_data = record[2]
                parsed_data = json.loads(json_data)
                for result in parsed_data['results']:
                    self.tree.insert("", tk.END, values=(sample_id, result['test_no'], result['result_with_unit']))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    def search_data(self):
        sample_id = self.search_entry.get().strip()
        if not sample_id:
            messagebox.showwarning("Input Error", "Please enter a Sample ID to search.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM astm_data WHERE sample_id = ?", (sample_id,))
            records = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())  # Clear existing data

            if records:
                for record in records:
                    json_data = record[2]
                    parsed_data = json.loads(json_data)
                    for result in parsed_data['results']:
                        self.tree.insert("", tk.END, values=(sample_id, result['test_no'], result['result_with_unit']))
            else:
                messagebox.showinfo("No Results", f"No data found for Sample ID: {sample_id}")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Page One", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button.pack()

        # Your existing settings and exit button
        settings_button = ttk.Button(self, text="Settings")
        settings_button.pack(side=tk.LEFT, padx=10, pady=10)

        exit_button = ttk.Button(self, text="Exit",
                                 command=lambda: controller.quit())
        exit_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Integrate ASTMApp into PageOne
        self.astm_app = ASTMApp(self)

    def get_astm_app(self):
        return self.astm_app


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Page Two", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button.pack()


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageOne, PageTwo):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageOne")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def quit(self):
        if connection:
            connection.close()
        self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.geometry("800x600")
    app.title("Tkinter Application")
    app.mainloop()
