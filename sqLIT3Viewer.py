import sqlite3
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import ttk


# Connect to the SQLite database
def connect_db(db_name):
    return sqlite3.connect (db_name)


# Fetch data from the database
def fetch_data(conn, table_name):
    cursor = conn.cursor ()
    cursor.execute (f"SELECT * FROM {table_name}")
    return cursor.fetchall (), [description[0] for description in cursor.description]


# Create the main application window
class DatabaseViewer (ttkb.Window):
    def __init__(self, db_name, table_name):
        super ().__init__ (themename="darkly")  # Set theme to darkly
        self.title ("SQLite Database Viewer")
        self.geometry ("800x600")

        # Connect to the database and fetch data
        self.conn = connect_db (db_name)
        self.data, self.columns = fetch_data (self.conn, table_name)

        # Set the font and style for the Treeview
        style = ttk.Style (self)
        style.configure ("Treeview.Heading", font=("Arial", 14))
        style.configure ("Treeview", font=("Arial", 12))

        # Create the Treeview widget
        self.tree = ttk.Treeview (self, columns=self.columns, show='headings', bootstyle=SUCCESS)
        for col in self.columns:
            self.tree.heading (col, text=col)

        # Insert data into the Treeview
        for row in self.data:
            self.tree.insert ("", END, values=row)

        # Pack the Treeview widget
        self.tree.pack (expand=True, fill='both')


# Main function to run the application
def main():
    db_name = 'habib04.db'  # Replace with your database file name
    table_name = 'astm_data'  # Replace with your table name
    app = DatabaseViewer (db_name, table_name)  # Initialize the application
    app.mainloop ()


if __name__ == "__main__":
    main ()
