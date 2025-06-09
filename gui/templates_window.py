import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic.template import Template


class TemplateSelectorWindow:
    def __init__(self, master, on_template_selected):
        """
        Okno wyboru szablonu.
        :param master: root
        """
        self.master = master
        self.master.title("Wybór szablonu")

        self.templates_dir = "./resources/templates"
        self.templates = Template.load_templates()
        self.selected_template = None
        self.on_template_selected = on_template_selected

        self._build_interface()

    def _build_interface(self):
        """Tworzy GUI."""
        frame = ttk.Frame(self.master)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        list_frame = ttk.Frame(frame)
        list_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        listbox_container = ttk.Frame(list_frame)
        listbox_container.pack()

        scrollbar = tk.Scrollbar(listbox_container, orient=tk.VERTICAL)

        self.listbox = tk.Listbox(
            listbox_container,
            height=15,
            width=30,
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar.config(command=self.listbox.yview)

        for name, _ in self.templates:
            self.listbox.insert(tk.END, name)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.preview_frame = ttk.Frame(frame)
        self.preview_frame.grid(row=0, column=1, sticky="nsew")

        self.label_birth = ttk.Label(self.preview_frame, background="#dcdad5", text="Narodziny: -")
        self.label_birth.pack(anchor="w")
        self.label_survive = ttk.Label(self.preview_frame, background="#dcdad5", text="Przeżycie: -")
        self.label_survive.pack(anchor="w")
        self.label_age = ttk.Label(self.preview_frame, background="#dcdad5", text="Wiek: -")
        self.label_age.pack(anchor="w")

        self.canvas = tk.Canvas(self.preview_frame, width=300, height=300, bg="white")
        self.canvas.pack(pady=10)

        self.select_button = ttk.Button(self.preview_frame, text="Wybierz szablon", command=self.confirm_selection)
        self.select_button.pack(fill="x")
        self.delete_button = ttk.Button(self.preview_frame, text="Usuń szablon", command=self.delete_template)
        self.delete_button.pack(fill="x", pady=(5, 0))

    def on_select(self, event):
        """Obsługuje wybór szablonu z listy."""
        idx = self.listbox.curselection()
        if not idx:
            return
        _, template = self.templates[idx[0]]
        self.selected_template = template
        self._update_preview(template)

    def _update_preview(self, template):
        """Aktualizuje podgląd zasad i planszy."""
        self.label_birth.config(text=f"Narodziny: {' '.join(map(str, template.rules.birth))}")
        self.label_survive.config(text=f"Przeżycie: {' '.join(map(str, template.rules.survive))}")
        self.label_age.config(text=f"Wiek: {template.rules.age}")

        self.canvas.delete("all")
        grid = template.grid
        rows = len(grid)
        cols = len(grid[0]) if rows else 0
        cell_size = min(10, 300 // max(rows, cols, 1))

        for y in range(rows):
            for x in range(cols):
                if grid[y][x]:
                    x1 = x * cell_size
                    y1 = y * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")

    def confirm_selection(self):
        """Zatwierdza wybór szablonu i otwiera główne okno gry z szablonem."""
        if self.selected_template:
            self.master.destroy()
            self.on_template_selected(self.selected_template)

    def delete_template(self):
        """Usuwa wybrany szablon po potwierdzeniu."""
        idx = self.listbox.curselection()
        if not idx:
            messagebox.showwarning("Brak wyboru", "Najpierw wybierz szablon do usunięcia.")
            return

        name, _ = self.templates[idx[0]]
        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć szablon '{name}'?")
        if confirm:
            filename = os.path.join(self.templates_dir, f"template_{name}.json")
            try:
                os.remove(filename)
                del self.templates[idx[0]]
                self.listbox.delete(idx)
                self.selected_template = None
                self._clear_preview()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się usunąć pliku:\n{e}")

    def _clear_preview(self):
        self.label_birth.config(text="Narodziny: -")
        self.label_survive.config(text="Przeżycie: -")
        self.label_age.config(text="Wiek: -")
        self.canvas.delete("all")

