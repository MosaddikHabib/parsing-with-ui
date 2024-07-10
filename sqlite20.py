import sqlite3
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox, simpledialog


# Connect to the SQLite database
def connect_db(db_name):
    return sqlite3.connect(db_name)


# Fetch data from the database
def fetch_data(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall(), [description[0] for description in cursor.description]


# Update data in the database
def update_data(conn, table_name, row_id, updates):
    cursor = conn.cursor()
    set_clause = ", ".join([f"{col} = ?" for col in updates.keys()])
    values = list(updates.values()) + [row_id]
    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = ?", values)
    conn.commit()


# Create the main application window
class DatabaseViewer(ttkb.Window):
    def __init__(self, db_name, table_name):
        super().__init__(themename="darkly")  # Set theme to darkly
        self.title("SQLite Database Viewer")
        self.geometry("800x600")

        # Connect to the database and fetch data
        self.conn = connect_db(db_name)
        self.table_name = table_name
        self.data, self.columns = fetch_data(self.conn, table_name)

        # Set the font and style for the Treeview
        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Arial", 14))
        style.configure("Treeview", font=("Arial", 12))

        # Create the Treeview widget
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings', bootstyle=SUCCESS)
        for col in self.columns:
            self.tree.heading(col, text=col)

        # Insert data into the Treeview
        for row in self.data:
            self.tree.insert("", END, values=row)

        # Pack the Treeview widget
        self.tree.pack(expand=True, fill='both')

        # Add edit button
        edit_button = ttkb.Button(self, text="Edit", command=self.edit_record, bootstyle=PRIMARY)
        edit_button.pack(pady=10)

    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        item = self.tree.item(selected_item)
        current_values = item['values']
        updates = {}

        for i, column in enumerate(self.columns):
            new_value = simpledialog.askstring("Edit", f"Edit {column}:", initialvalue=current_values[i])
            if new_value:
                updates[column] = new_value

        if updates:
            row_id = current_values[0]
            update_data(self.conn, self.table_name, row_id, updates)

            # Refresh the Treeview
            self.tree.item(selected_item, values=[updates.get(col, current_values[i]) for i, col in enumerate(self.columns)])


# Main function to run the application
def main():
    db_name = 'habib07.db'  # Replace with your database file name
    table_name = 'astm_data'  # Replace with your table name
    app = DatabaseViewer(db_name, table_name)  # Initialize the application
    app.mainloop()


if __name__ == "__main__":
    main()
