import tkinter as tk
from tkinter import ttk

from logic.game_state import GameState
from logic.rules import Rules
from logic.template import Template


class MainWindow:
    """
    Główne okno gry – wyświetla planszę, kontrolki i obsługuje grę.
    """

    def __init__(self, master, width, height, rules, initial_grid=None):
        """Inicjalizuje główne okno gry.
                :param master: root
                :param width: szerokość planszy
                :param height: wysokość planszy
                :param rules: zasady gry (Rules)
                """
        self.master = master
        self.master.title("Gra w Życie")
        self.cell_size = 20
        self.delay = 200
        self.running = False
        self.drag_mode = None

        # screen_width = self.master.winfo_screenwidth()
        # screen_height = self.master.winfo_screenheight()
        # x = (screen_width - self.master.winfo_reqwidth()) // 2
        # y = (screen_height - self.master.winfo_reqheight()) // 2
        # self.master.geometry(f"-{x}-{y}")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("TButton", padding=6, font=("Segoe UI", 10))
        style.configure("TLabelframe", background="#f0f0f0", font=("Segoe UI", 11, "bold"))
        style.configure("TLabelframe.Label", background="#f0f0f0")
        style.configure("TFrame", background="#f0f0f0")

        self.state = GameState(height, width, rules, initial_grid)

        self._build_interface(width, height)
        self.update_canvas()
        self.centred_window()

    def _build_interface(self, width, height):
        """Buduje cały interfejs użytkownika."""

        title_label = ttk.Label(self.master, text="Gra w Życie", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=(10, 0))

        self.frame = ttk.Frame(self.master)
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)

        self._create_rules_section()
        self._create_buttons_section()
        self._create_template_section()
        self._create_exit_section()

        canvas_frame = ttk.Frame(self.master, relief="sunken")
        canvas_frame.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(canvas_frame, width=width * self.cell_size, height=height * self.cell_size, bg="white")
        self.canvas.pack()

        self.cells = [[self.canvas.create_rectangle(
            x * self.cell_size, y * self.cell_size,
            (x + 1) * self.cell_size, (y + 1) * self.cell_size,
            fill="white", outline="gray"
        ) for x in range(width)] for y in range(height)]

        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

    def _create_rules_section(self):
        """Tworzy sekcję zasad gry."""
        section = ttk.LabelFrame(self.frame, text="Zasady gry")
        section.pack(fill="x")

        ttk.Label(section, text="Przeżycie:").grid(row=0, column=0, sticky="w")
        self.entry_survive = ttk.Entry(section, width=15)
        self.entry_survive.insert(0, ' '.join(map(str, self.state.rules.survive)))
        self.entry_survive.grid(row=0, column=1)

        ttk.Label(section, text="Narodziny:").grid(row=1, column=0, sticky="w")
        self.entry_birth = ttk.Entry(section, width=15)
        self.entry_birth.insert(0, ' '.join(map(str, self.state.rules.birth)))
        self.entry_birth.grid(row=1, column=1)

        ttk.Label(section, text="Wiek:").grid(row=2, column=0, sticky="w")
        self.entry_age = ttk.Entry(section, width=15)
        self.entry_age.insert(0, str(self.state.rules.age))
        self.entry_age.grid(row=2, column=1)

        ttk.Button(section, text="Zachowaj zasady", command=self.apply_rules).grid(row=3, column=0, columnspan=2,
                                                                                   pady=(8, 2), sticky="ew")
        ttk.Button(section, text="Losowe zasady", command=self.randomize_rules).grid(row=4, column=0, columnspan=2,
                                                                                     pady=(2, 2), sticky="ew")

    def _create_buttons_section(self):
        """Tworzy sekcję przycisków sterujących grą."""
        section = ttk.LabelFrame(self.frame, text="Sterowanie")
        section.pack(fill="x")

        self.btn_start = ttk.Button(section, text="Start", command=self.toggle_run)
        self.btn_start.pack(fill="x")

        ttk.Button(section, text="Krok", command=self.step).pack(fill="x", pady=(2, 0))
        ttk.Button(section, text="Reset", command=self.reset).pack(fill="x", pady=(2, 0))
        ttk.Button(section, text="Losowe pole", command=self.randomize).pack(fill="x", pady=(2, 5))

        ttk.Label(section, text="Szybkość (ms):").pack(anchor="w")
        self.scale_delay = tk.Scale(
            section,
            from_=5,
            to=1000,
            orient=tk.HORIZONTAL,
            resolution=5,
            length=150,
            command=self.update_delay
        )
        self.scale_delay.set(self.delay)
        self.scale_delay.pack(fill="x", pady=(0, 5))

    def update_delay(self, value):
        """Aktualizuje opóźnienie animacji na podstawie suwaka."""
        self.delay = int(value)

    def _create_template_section(self):
        """Tworzy sekcję z szablonami i powrotem do startu."""
        self.template_section = ttk.LabelFrame(self.frame, text="Szablony")
        self.template_section.pack(fill="x")

        self.btn_save_template = ttk.Button(self.template_section, text="Zapisz szablon", command=self.save_template)
        self.btn_save_template.pack(fill="x", pady=(2, 2))

    def _create_exit_section(self):
        """Tworzy sekcję z szablonami i powrotem do startu."""
        section = ttk.LabelFrame(self.frame, text="Powrót")
        section.pack(fill="x")

        ttk.Button(section, text="Powrót do startu", command=self.back_to_start).pack(fill="x", pady=(2, 2))

    def update_canvas(self):
        """Aktualizuje kolory komórek na podstawie stanu planszy."""
        for y in range(self.state.board.rows):
            for x in range(self.state.board.cols):
                val = self.state.board.grid[y][x]
                age = self.state.board.age_grid[y][x]
                if val:
                    if self.state.rules.age == -1:
                        color = "black"
                    else:
                        shade = int(255 - min(age, self.state.rules.age) * (255 / self.state.rules.age))
                        color = f"#{shade:02x}{shade:02x}{shade:02x}"
                else:
                    color = "white"
                self.canvas.itemconfig(self.cells[y][x], fill=color)

    def toggle_cell(self, y, x):
        """Przełącza stan komórki."""
        self.state.toggle_cell(y, x)
        self.update_canvas()

    def on_mouse_down(self, event):
        """Określa tryb przeciągania na podstawie kliknięcia."""
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.drag_mode = "deactivate" if self.state.board.grid[y][x] else "activate"
        self.toggle_cell(y, x)

    def on_mouse_drag(self, event):
        """Przeciąganie myszą w celu aktywacji/dezaktywacji komórek."""
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if 0 <= y < self.state.board.rows and 0 <= x < self.state.board.cols:
            val = self.state.board.grid[y][x]
            if (self.drag_mode == "activate" and val == 0) or (self.drag_mode == "deactivate" and val == 1):
                self.toggle_cell(y, x)

    def toggle_run(self):
        """Startuje lub zatrzymuje animację."""
        self.running = not self.running
        self.btn_start.config(text="Stop" if self.running else "Start")
        if self.running:
            self.run_loop()

    def run_loop(self):
        """Pętla animacji."""
        if self.running:
            self.step()
            self.master.after(self.delay, self.run_loop)

    def step(self):
        """Wykonuje jeden krok symulacji."""
        self.state.step()
        self.update_canvas()

    def reset(self):
        """Czyści planszę."""
        self.running = False
        self.btn_start.config(text="Start")
        self.state.reset()
        self.update_canvas()

    def randomize(self):
        """Losuje układ komórek."""
        self.state.randomize(prob=0.2)
        self.update_canvas()

    def randomize_rules(self):
        """Losuje zasady gry."""
        self.state.rules = self.state.rules.generate_random()
        self.update_rules_entry()
        self.update_canvas()

    def apply_rules(self):
        """Zastosowuje zasady z panelu."""
        try:
            age = int(self.entry_age.get())
            survive = list(map(int, self.entry_survive.get().strip().split()))
            birth = list(map(int, self.entry_birth.get().strip().split()))
            self.state.apply_rules(Rules(birth, survive, age))
            self.update_canvas()
        except ValueError:
            pass

    def update_rules_entry(self):
        """Aktualizuje pola wejściowe zasad."""
        self.entry_birth.delete(0, tk.END)
        self.entry_birth.insert(0, ' '.join(map(str, self.state.rules.birth)))
        self.entry_survive.delete(0, tk.END)
        self.entry_survive.insert(0, ' '.join(map(str, self.state.rules.survive)))
        self.entry_age.delete(0, tk.END)
        self.entry_age.insert(0, self.state.rules.age)

    def save_template(self):
        """Zapisuje aktualny szablon."""
        label = ttk.Label(self.template_section, text="Nazwa:")
        label.pack(side=tk.LEFT)

        entry_nazwa = tk.Entry(self.template_section, width=15)
        entry_nazwa.pack(side=tk.RIGHT)
        entry_nazwa.focus()

        def save_with_name():
            Template.save_template(Template(entry_nazwa.get(), self.state.board.grid, self.state.rules))
            label.destroy()
            entry_nazwa.destroy()
            self.btn_save_template.config(text="Zapisz szablon", command=self.save_template)

        self.btn_save_template.config(text="Zachowaj nazwę", command=save_with_name)

    def back_to_start(self):
        """Przechodzi do okna startowego."""
        from gui.start_window import StartWindow
        self.master.destroy()
        root = tk.Tk()
        StartWindow(root)
        root.mainloop()

    def centred_window(self):
        self.master.update_idletasks()
        width_w = self.master.winfo_width()
        height_w = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width_w) // 2
        y = (screen_height - height_w) // 2
        self.master.geometry(f"{width_w}x{height_w}+{x}+{y}")
