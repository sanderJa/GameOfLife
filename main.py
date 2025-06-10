import tkinter as tk
from gui.start_window import StartWindow

def main():
    """Plik main uruchamia cały program."""
    root = tk.Tk()
    app = StartWindow(root)
    root.mainloop()

if __name__ == "__main__":
     main()
