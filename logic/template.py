import json
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
            Rules(data["rules"]["birth"], data["rules"]["survive"],data["rules"]["age"]),

        )

    @staticmethod
    def save_template(template, directory="resources/templates/"):
        """Zapisuje szablon do foldera 'templates'."""
        safe_name = "".join(c for c in template.name if c.isalnum() or c in "_- ").strip()
        if not safe_name:
            raise ValueError("Nieprawidłowa nazwa szablonu.")
        filename = directory+"template_"+safe_name+".json"
        with open(filename,mode="wt") as f:
            json.dump(template.to_dict(), f, indent=2)

    @staticmethod
    def load_templates(filename="resources/templates/templates"):
        """Wczytuje listę szablonów z foldera 'templates'."""
        try:
            with open(filename) as f:
                data = json.load(f)
            return [Template.from_dict(d) for d in data]
        except:
            return []