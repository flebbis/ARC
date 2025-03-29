import win32api
import win32con

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