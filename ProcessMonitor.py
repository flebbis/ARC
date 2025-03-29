import time
import psutil
from ScreenRes import ScreenRes
from Settings import load_settings

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