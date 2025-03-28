import json
import time
import psutil
import win32api
import win32con
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.font as tkFont


SETTINGS_FILE = "program_settings.json"


class ScreenRes:
    @staticmethod
    def get_max_fps():
        """Hämtar den högsta tillgängliga FPS för huvudskärmen."""
        mode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
        return mode.DisplayFrequency

    @staticmethod
    def set(width=None, height=None, depth=32):
        """Ändrar skärmupplösningen och sätter FPS till max."""
        refresh_rate = ScreenRes.get_max_fps()

        if width and height:
            print(f"Ställer in upplösning till {width}x{height} ({depth}-bit, {refresh_rate} Hz)")

            mode = win32api.EnumDisplaySettings()
            mode.PelsWidth = width
            mode.PelsHeight = height
            mode.BitsPerPel = depth
            mode.DisplayFrequency = refresh_rate

            result = win32api.ChangeDisplaySettings(mode, 0)
            if result != 0:
                print(f"⚠️ Fel vid upplösningsändring: {result}")
        else:
            print("Återställer standardupplösning")
            win32api.ChangeDisplaySettings(None, 0)

    @staticmethod
    def get():
        """Hämtar aktuell upplösning."""
        user32 = win32api.GetSystemMetrics
        return user32(0), user32(1)

    @staticmethod
    def get_sub_resolutions():
        """Genererar relevanta subupplösningar baserat på huvudskärmens upplösning."""
        width, height = ScreenRes.get()
        resolutions = [
            (width, height),
            (width // 2, height // 2),
            (width // 2, height),
            (width, height // 2),
            (width // 4 * 3, height // 4 * 3),
            (width // 4, height // 4),
            (1920, 1440),  # Added resolution
            (1600, 1200),  # Added resolution
            (1280, 1024),  # Added resolution
            (1024, 768)    # Added resolution
        ]
        # Filter out too small resolutions and sort by width in descending order
        return [f"{w} x {h}" for w, h in sorted(resolutions, reverse=True) if w >= 800 and h >= 600]


def load_settings():
    """Laddar programinställningar från JSON-filen och sparar standardupplösningen om den saknas."""
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    if "default" not in settings:
        width, height = ScreenRes.get()
        settings["default"] = {
            "resolution": [width, height],
            "fps": ScreenRes.get_max_fps()
        }
        save_settings(settings)

    return settings


def save_settings(settings):
    """Sparar programinställningar till JSON-filen."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def is_process_running(process_name):
    """Kollar om en viss process körs."""
    for process in psutil.process_iter(attrs=["name"]):
        if process.info["name"].lower() == process_name.lower():
            return True
    return False


def monitor_processes():
    """Övervakar angivna program och ändrar upplösningen/FPS vid start och stopp."""
    settings = load_settings()
    default_res = settings["default"]["resolution"]
    default_fps = settings["default"]["fps"]

    active_programs = {}  # Spårar vilka program som körs

    print(f"Övervakar följande program: {', '.join(settings.keys())}")

    while True:
        for program, config in settings.items():
            if program == "default":
                continue  # Hoppa över standardinställningen

            running = is_process_running(program)

            if running and program not in active_programs:
                print(f"{program} startat! Byter till {config['resolution']} @ {ScreenRes.get_max_fps()} Hz")
                ScreenRes.set(*config["resolution"])
                active_programs[program] = True

            elif not running and program in active_programs:
                print(f"{program} stängt! Återställer till {default_res} @ {default_fps} Hz")
                ScreenRes.set(*default_res)  # Återställ till första upplösningen
                del active_programs[program]

        time.sleep(2)





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


if __name__ == "__main__":
    while True:
        choice = input("1. Lägg till program \n2. Starta övervakning\nVal: ")
        if choice == "1":
            add_program_gui()
        elif choice == "2":
            monitor_processes()
        else:
            print("Ogiltigt val, försök igen.")

