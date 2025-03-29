from gui import add_program_gui
from ProcessMonitor import monitor_processes

if __name__ == "__main__":
    while True:
        choice = input("1. Lägg till program \n2. Starta övervakning\nVal: ")
        if choice == "1":
            add_program_gui()
        elif choice == "2":
            monitor_processes()
        else:
            print("Ogiltigt val, försök igen.")