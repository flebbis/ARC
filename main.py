import json
import time
import psutil
import win32api
import win32con
import tkinter as tk
from tkinter import filedialog, ttk

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
    """GUI för att lägga till ett nytt program."""

    def browse_program():
        filename = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if filename:
            program_var.set(filename.split("/")[-1])

    def save_program():
        program = program_var.get().strip()
        resolution = resolution_var.get()

        if not program or not resolution:
            return

        width, height = map(int, resolution.split(" x "))
        settings = load_settings()
        settings[program] = {"resolution": [width, height]}
        save_settings(settings)
        root.destroy()

    root = tk.Tk()
    root.title("Lägg till program")
    root.geometry("300x200+50+600")  # Position i nedre vänstra hörnet
    root.configure(bg="#222")

    program_var = tk.StringVar()
    resolution_var = tk.StringVar()

    tk.Label(root, text="Add a program", fg="white", bg="#222", font=("Courier", 12)).pack(pady=10)
    tk.Button(root, text="Browse", command=browse_program).pack()

    tk.Label(root, text="Target Resolution", fg="white", bg="#222", font=("Courier", 12)).pack(pady=10)
    resolutions = ["2560 x 1440", "1920 x 1080", "1280 x 720"]  # Exempelupplösningar
    ttk.Combobox(root, textvariable=resolution_var, values=resolutions).pack()

    tk.Button(root, text="Save", command=save_program).pack(pady=10)
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
