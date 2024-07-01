import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading


class TerminalView (tk.Frame):
    def __init__(self, parent, script_path):
        super ().__init__ (parent)
        self.pack (fill=tk.BOTH, expand=True)

        # Create a scrolled text widget
        self.terminal_output = scrolledtext.ScrolledText (self, wrap=tk.WORD)
        self.terminal_output.pack (fill=tk.BOTH, expand=True)

        # Start the script in a separate thread
        self.script_thread = threading.Thread (target=self.run_script, args=(script_path,))
        self.script_thread.start ()

    def run_script(self, script_path):
        process = subprocess.Popen (
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Read the script output line by line
        for line in process.stdout:
            self.terminal_output.insert (tk.END, line)
            self.terminal_output.see (tk.END)

        for line in process.stderr:
            self.terminal_output.insert (tk.END, line)
            self.terminal_output.see (tk.END)

        process.stdout.close ()
        process.stderr.close ()
        process.wait ()


class Application (tk.Tk):
    def __init__(self, script_path):
        super ().__init__ ()
        self.title ("Tkinter Terminal View")
        self.geometry ("800x600")

        # Add the terminal view to the application
        self.terminal_view = TerminalView (self, script_path)


if __name__ == "__main__":
    script_path = "H:\Z pythonProject\Host Mate\parsing-with-ui\main.py"
    app = Application (script_path)
    app.mainloop ()
