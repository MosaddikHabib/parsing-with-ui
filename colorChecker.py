import customtkinter as ctk
from tkinter import colorchooser
import pyperclip  # To copy text to clipboard

def pick_color():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code[1]:
        hex_code = color_code[1]
        rgb_code = color_code[0]
        color_label.configure(fg_color=hex_code)
        hex_label.configure(text=f"Hex: {hex_code}")
        rgb_label.configure(text=f"RGB: {rgb_code}")

def show_color():
    input_value = color_input.get()
    if input_value.startswith('#') and len(input_value) == 7:
        hex_code = input_value
        color_label.configure(fg_color=hex_code)
        hex_label.configure(text=f"Hex: {hex_code}")
        rgb_label.configure(text="Invalid RGB")
    elif input_value.startswith('rgb(') and input_value.endswith(')'):
        try:
            rgb_code = tuple(map(int, input_value[4:-1].split(',')))
            color_label.configure(fg_color='#%02x%02x%02x' % rgb_code)
            hex_label.configure(text="Invalid Hex")
            rgb_label.configure(text=f"RGB: {rgb_code}")
        except ValueError:
            color_label.configure(fg_color="white")
            hex_label.configure(text="Invalid Hex")
            rgb_label.configure(text="Invalid RGB")
    else:
        color_label.configure(fg_color="white")
        hex_label.configure(text="Invalid Hex")
        rgb_label.configure(text="Invalid RGB")

def copy_to_clipboard(event):
    # Get the text of the label that triggered the event
    text_to_copy = event.widget.cget("text")
    if text_to_copy.startswith("Hex: "):
        text_to_copy = text_to_copy[5:]
    elif text_to_copy.startswith("RGB: "):
        text_to_copy = text_to_copy[5:]

    # Copy text to clipboard
    pyperclip.copy(text_to_copy)

# Create the main window
root = ctk.CTk()
root.title("Color Picker")
root.geometry("250x400")  # Set window size to 600x400
root.resizable(False, False)
ctk.set_appearance_mode("dark")  # Set dark mode
ctk.set_default_color_theme("dark-blue")  # Set color theme

# Create widgets
pick_button = ctk.CTkButton(root, text="Pick a Color", command=pick_color)
pick_button.pack(pady=20)

color_label = ctk.CTkLabel(root, text="", width=200, height=75, fg_color="white", corner_radius=10)
color_label.pack(pady=20)

# Input field for hex or RGB code
color_input = ctk.CTkEntry(root, width=100)
color_input.pack(pady=10)

# Button to show color from input
show_button = ctk.CTkButton(root, text="Show Color", command=show_color)
show_button.pack(pady=10)

hex_label = ctk.CTkLabel(root, text="Hex: ")
hex_label.pack(pady=10)

# Bind click event to copy hex color
hex_label.bind("<Button-1>", copy_to_clipboard)

rgb_label = ctk.CTkLabel(root, text="RGB: ")
rgb_label.pack(pady=10)

# Bind click event to copy RGB color
rgb_label.bind("<Button-1>", copy_to_clipboard)

# Run the main loop
root.mainloop()