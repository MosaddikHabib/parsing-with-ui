import customtkinter as ctk
from tkinter import colorchooser

def pick_color():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code[1]:
        hex_code = color_code[1]
        rgb_code = color_code[0]
        color_label.configure(fg_color=hex_code)
        hex_label.configure(text=f"Hex: {hex_code}")
        rgb_label.configure(text=f"RGB: {rgb_code}")

# Create the main window
root = ctk.CTk()
root.title("Color Picker")
root.geometry("600x400")  # Set window size to 600x400
ctk.set_appearance_mode("dark")  # Set dark mode
ctk.set_default_color_theme("dark-blue")  # Set color theme

# Create widgets
pick_button = ctk.CTkButton(root, text="Pick a Color", command=pick_color)
pick_button.pack(pady=20)

color_label = ctk.CTkLabel(root, text="", width=400, height=200, fg_color="white", corner_radius=10)
color_label.pack(pady=20)

hex_label = ctk.CTkLabel(root, text="Hex: ")
hex_label.pack(pady=10)

rgb_label = ctk.CTkLabel(root, text="RGB: ")
rgb_label.pack(pady=10)

# Run the main loop
root.mainloop()
