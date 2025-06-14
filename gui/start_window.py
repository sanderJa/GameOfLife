import tkinter as tk
from tkinter import ttk

from gui.main_window import MainWindow
from gui.templates_window import TemplateSelectorWindow
from logic.rules import Rules


class StartWindow:
    """
   Okno startowe do konfiguracji początkowych parametrów gry.
    """

    def __init__(self, master):
        """
        Inicjalizuje startowe okno gry.
        :param master: root
        """
        self.master = master
        self.master.title("Start - Gra w Życie")
        self.master.geometry("600x500")
        self.master.configure(bg="#f0f0f0")
        self.master.resizable(False, False)



        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10))
        style.configure("TButton", padding=6, font=("Segoe UI", 10))
        style.configure("TLabelframe", background="#ffffff", font=("Segoe UI", 11, "bold"))
        style.configure("TLabelframe.Label", background="#ffffff")

        self._build_rules_board()
        self._build_rules()
        self._build_buttons()


    def _build_rules_board(self):
        """
            Tworzy interfejs do konfiguracji planszy gry.
        """
        # Zmienna space jest dla wyrównania wszytkich elementów
        space = "                            "

        title = ttk.Label(self.master, text="Gra w Życie – Konfiguracja", font=("Segoe UI", 18, "bold"),
                          background="#f0f0f0")
        title.pack(pady=20)

        self.container = ttk.Frame(self.master, padding=20)
        self.container.pack(expand=True)

        board_frame = ttk.Labelframe(self.container, text="Plansza", padding=15)
        board_frame.pack(fill="x", pady=10)

        ttk.Label(board_frame, text=space + "Szerokość:").grid(row=0, column=0, sticky="n", padx=5, pady=5)
        self.entry_width = ttk.Entry(board_frame)
        self.entry_width.insert(0, "30")
        self.entry_width.grid(row=0, column=1, pady=5)

        ttk.Label(board_frame, text=space + "Wysokość:").grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.entry_height = ttk.Entry(board_frame)
        self.entry_height.insert(0, "30")
        self.entry_height.grid(row=1, column=1, pady=5)



    def _build_rules(self):
        """
           Tworzy interfejs do konfiguracji zasad gry.
        """
        rules_frame = ttk.Labelframe(self.container, text="Zasady życia", padding=15)
        rules_frame.pack(fill="x", pady=10)

        ttk.Label(rules_frame, text="Przeżycie (np. 2 3):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_survive = ttk.Entry(rules_frame)
        self.entry_survive.insert(0, "2 3")
        self.entry_survive.grid(row=0, column=1, pady=5)

        ttk.Label(rules_frame, text="Narodziny (np. 3):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_birth = ttk.Entry(rules_frame)
        self.entry_birth.insert(0, "3")
        self.entry_birth.grid(row=1, column=1, pady=5)

        ttk.Label(rules_frame, text="Max wiek (-1 = nieśmiertelne):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_age = ttk.Entry(rules_frame)
        self.entry_age.insert(0, "10")
        self.entry_age.grid(row=2, column=1, pady=5)


    def _build_buttons(self):
        """
            Tworzy przyciski sterujące aplikacją.
        """
        button_frame = ttk.Frame(self.container)
        button_frame.pack(pady=20)

        self.btn_random_rules = ttk.Button(button_frame, text="Losowe zasady", command=self.set_random_rules)
        self.btn_random_rules.grid(row=0, column=0, padx=10)

        self.btn_templates = ttk.Button(button_frame, text="Szablony", command=self.open_templates)
        self.btn_templates.grid(row=0, column=1, padx=10)

        self.btn_start = ttk.Button(button_frame, text="Start", command=self.start_game)
        self.btn_start.grid(row=0, column=2, padx=10)


    def open_templates(self):
        """Otwiera okno wyboru szablonu i ustawia dane w polach."""
        popup = tk.Toplevel(self.master)
        TemplateSelectorWindow(popup, self.open_main_window_with_template)

    def open_main_window_with_template(self, template):
        """Zamknij StartWindow i otwórz MainWindow z wybranym szablonem."""
        self.master.destroy()

        grid = template.grid
        rules = template.rules
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        root = tk.Tk()
        MainWindow(root, width, height, rules, initial_grid=grid)
        root.mainloop()

    def set_random_rules(self):
        """Ustawia losowe zasady gry w polach tekstowych."""
        rules = Rules.generate_random()
        self.entry_survive.delete(0, tk.END)
        self.entry_survive.insert(0, ' '.join(map(str, rules.survive)))
        self.entry_birth.delete(0, tk.END)
        self.entry_birth.insert(0, ' '.join(map(str, rules.birth)))
        self.entry_age.delete(0, tk.END)
        self.entry_age.insert(0, str(rules.age))

    def parse_rules(self):
        """Parsuje tekst z pola zasad do obiektu Rules."""
        try:
            age = int(self.entry_age.get())
            survive = list(map(int, self.entry_survive.get().strip().split()))
            birth = list(map(int, self.entry_birth.get().strip().split()))
            return Rules(birth, survive, age)
        except:
            return Rules([3], [2, 3], 10)

    def start_game(self):
        """Uruchamia główne okno gry z podanymi parametrami."""
        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
        except:
            width, height = 30, 30

        rules = self.parse_rules()
        self.master.destroy()

        root = tk.Tk()
        MainWindow(root, width, height, rules)
        root.mainloop()
