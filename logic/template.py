import json
import os

from logic.rules import Rules


class Template:
    """
    Klasa reprezentująca szablon (template) gry.
    Zawiera rozmiar, stan planszy i zasady.
    """

    def __init__(self, name, grid, rules):
        """
        Inicjalizuje szablon gry.
        :param name: nazwa szablonu
        :param grid: plansza
        :param rules: zasady gry (Rules)
        """
        self.name = name
        self.grid = grid
        self.rules = rules

    def to_dict(self):
        """Zwraca dane szablonu jako słownik."""
        return {
            "name": self.name,
            "grid": self.grid,
            "rules": {
                "birth": list(self.rules.birth),
                "survive": list(self.rules.survive),
                "age": self.rules.age,
            }
        }

    @staticmethod
    def from_dict(data):
        """Tworzy instancję szablonu z danych słownikowych."""
        return Template(
            data["name"],
            data["grid"],
            Rules(data["rules"]["birth"], data["rules"]["survive"], data["rules"]["age"]),

        )

    @staticmethod
    def save_template(template, directory="./resources/templates/"):
        """Zapisuje szablon do foldera 'templates'. Jeśli plik już istnieje, zgłasza wyjątek."""
        safe_name = "".join(c for c in template.name if c.isalnum() or c in "_- ").strip()
        if not safe_name:
            raise ValueError("Nieprawidłowa nazwa szablonu.")

        filename = os.path.join(directory, "template_" + safe_name + ".json")

        if os.path.exists(filename):
            raise FileExistsError(f"Plik '{filename}' już istnieje. Wybierz inną nazwę.")

        os.makedirs(directory, exist_ok=True)  # Upewnia się, że katalog istnieje
        with open(filename, mode="w", encoding="utf-8") as f:
            json.dump(template.to_dict(), f, indent=2)

    @staticmethod
    def load_templates(directory="./resources/templates"):
        """
        Wczytuje wszystkie szablony z plików JSON w folderze.
        Zwraca listę krotek: (nazwa_szablonu, Template)
        """
        templates = []
        if not os.path.exists(directory):
            print(f"Folder nie istnieje: {directory}")
            return templates

        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    clean_name = filename
                    if clean_name.startswith("template_"):
                        clean_name = clean_name[len("template_"):]
                    if clean_name.endswith(".json"):
                        clean_name = clean_name[:-len(".json")]

                    if isinstance(data, list):
                        for i, d in enumerate(data):
                            templates.append((f"{clean_name} [{i}]", Template.from_dict(d)))
                    elif isinstance(data, dict):
                        templates.append((clean_name, Template.from_dict(data)))

                except Exception as e:
                    print(f"Błąd wczytywania {filename}: {e}")
        return templates
