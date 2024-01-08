import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def load_gif():
    filepath = filedialog.askopenfilename(filetypes=[("GIF Files", "*.gif")])
    if not filepath:
        return

    try:
        gif = Image.open(filepath)
        frames = []
        i = 0
        while True:
            frames.append(gif.copy())
            i += 1
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    except Exception as e:
        textbox.delete('1.0', tk.END)
        textbox.insert(tk.END, f"Error: {e}\n")
        return

    textbox.delete('1.0', tk.END)
    textbox.insert(tk.END, f"Loaded GIF with {len(frames)} frames.\n")

    # Store the frames for later use
    root.frames = frames

def export_frames():
    if not hasattr(root, 'frames') or not root.frames:
        messagebox.showerror("Error", "No GIF loaded or no frames to export.")
        return

    format = export_format_var.get().lower()
    if not os.path.exists('frames'):
        os.makedirs('frames')

    for i, frame in enumerate(root.frames):
        frame_filename = f"frames/{i + 1}.{format}"
        frame.save(frame_filename, format.upper())
        textbox.insert(tk.END, f"Exported {frame_filename}\n")

# Create the main window
root = tk.Tk()
root.title("GIF Frame Extractor")

# Create a frame for the layout
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Load GIF button
load_gif_button = tk.Button(frame, text="Load GIF", command=load_gif)
load_gif_button.pack(fill='x')

# Textbox for messages or frame list
textbox = tk.Text(frame, height=10, width=50)
textbox.pack()

# Export format dropdown
export_format_var = tk.StringVar(frame)
export_format_var.set("PNG")  # default value
export_formats = ["PNG", "JPEG", "BMP", "TIFF"]
export_format_menu = tk.OptionMenu(frame, export_format_var, *export_formats)
export_format_menu.pack()

# Export button
export_button = tk.Button(frame, text="Export Frames", command=export_frames)
export_button.pack(fill='x')

# Run the application
root.mainloop()
