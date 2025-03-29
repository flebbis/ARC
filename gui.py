import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.font as tkFont
from Settings import load_settings, save_settings
from ScreenRes import ScreenRes

def add_program_gui():
    """GUI for adding a new program."""

    def browse_program():
        filename = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if filename:
            program_var.set(filename.split("/")[-1])
            root.destroy()
            resolution_selection_gui(program_var.get())

    root = tk.Tk()
    root.title("Add a program")
    root.configure(bg="#1d1b20")

    # Center the window on the screen
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    root.lift()  # Bring the window to the front
    root.focus_force()  # Focus on the window
    root.attributes("-topmost", True)  # Ensure the window is on top

    program_var = tk.StringVar()

    # Load JetBrains Mono font
    font_path = "JetBrainsMono-Regular.ttf"
    jetbrains_mono = tkFont.Font(family="JetBrains Mono", size=16, name="JetBrainsMono")
    root.option_add("*Font", jetbrains_mono)

    style = ttk.Style()
    style.configure("TButton", font=jetbrains_mono, padding=10, relief="flat", background="#1d1b20", foreground="#1d1b20")
    style.map("TButton", background=[("active", "#3e3b40")])
    style.configure("Rounded.TButton", borderwidth=1, relief="solid", bordercolor="#3e3b40", focusthickness=3, focuscolor="none", padding=10, background="#1d1b20", foreground="#1d1b20")
    style.layout("Rounded.TButton", [
        ("Button.border", {"children": [("Button.padding", {"children": [("Button.label", {"sticky": "nswe"})], "sticky": "nswe"})], "sticky": "nswe"})])
    style.configure("Rounded.TButton", borderwidth=1, relief="solid", bordercolor="#3e3b40", focusthickness=3, focuscolor="none", padding=10, background="#1d1b20", foreground="#1d1b20")

    tk.Label(root, text="Add a program", fg="#FAFAFA", bg="#1d1b20", font=jetbrains_mono).pack(pady=20, expand=True)
    ttk.Button(root, text="Browse", command=browse_program, style="Rounded.TButton").pack(pady=10, expand=True)

    root.mainloop()

def resolution_selection_gui(program):
    """GUI for selecting resolution for the program."""

    def save_program():
        resolution = resolution_var.get()

        if not resolution:
            return

        width, height = map(int, resolution.split(" x "))
        settings = load_settings()
        settings[program] = {"resolution": [width, height]}
        save_settings(settings)
        root.destroy()

    root = tk.Tk()
    root.title("Select Resolution")
    root.configure(bg="#1d1b20")

    # Center the window on the screen
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    root.lift()  # Bring the window to the front
    root.focus_force()  # Focus on the window
    root.attributes("-topmost", True)  # Ensure the window is on top

    resolution_var = tk.StringVar()

    # Load JetBrains Mono font
    font_path = "JetBrainsMono-Regular.ttf"
    jetbrains_mono = tkFont.Font(family="JetBrains Mono", size=16, name="JetBrainsMono")
    root.option_add("*Font", jetbrains_mono)

    style = ttk.Style()
    style.configure("TButton", font=jetbrains_mono, padding=10, relief="flat", background="#1d1b20", foreground="#1d1b20")
    style.map("TButton", background=[("active", "#3e3b40")])
    style.configure("Rounded.TButton", borderwidth=1, relief="solid", bordercolor="#3e3b40", focusthickness=3, focuscolor="none", padding=10, background="#1d1b20", foreground="#1d1b20")
    style.layout("Rounded.TButton", [
        ("Button.border", {"children": [("Button.padding", {"children": [("Button.label", {"sticky": "nswe"})], "sticky": "nswe"})], "sticky": "nswe"})])
    style.configure("Rounded.TButton", borderwidth=1, relief="solid", bordercolor="#3e3b40", focusthickness=3, focuscolor="none", padding=10, background="#1d1b20", foreground="#1d1b20")

    tk.Label(root, text="Select Resolution", fg="#FAFAFA", bg="#1d1b20", font=jetbrains_mono).pack(pady=20, expand=True)
    tk.Label(root, text=f"Program: {program}", fg="#FAFAFA", bg="#1d1b20", font=jetbrains_mono).pack(pady=10, expand=True)

    tk.Label(root, text="Target Resolution", fg="#FAFAFA", bg="#1d1b20", font=jetbrains_mono).pack(pady=20, expand=True)
    resolutions = ScreenRes.get_sub_resolutions()  # Get relevant sub-resolutions
    ttk.Combobox(root, textvariable=resolution_var, values=resolutions, font=jetbrains_mono).pack(pady=10, expand=True)

    ttk.Button(root, text="Save", command=save_program, style="Rounded.TButton").pack(pady=20, expand=True)
    root.mainloop()