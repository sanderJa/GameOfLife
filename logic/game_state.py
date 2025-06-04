from logic.board import Board

class GameState:
    """
    Klasa łącząca planszę gry i zasady. Przechowuje bieżący stan gry.
    """
    def __init__(self, rows, cols, rules):
        """Inicjalizuje stan gry.
        :param rows: liczba wierszy planszy
        :param cols: liczba kolumn planszy
        :param rules: zasady gry (Rules)
        """
        self.board = Board(rows, cols)
        self.rules = rules


    def step(self):
        """Wykonuje jeden krok symulacji."""
        self.board.step(self.rules)

    def reset(self):
        """Resetuje planszę gry."""
        self.board.reset()

    def randomize(self, prob=0.2):
        """Losowo ustawia komórki na planszy."""
        self.board.randomize(prob)

    def toggle_cell(self, y, x):
        """Przełącza stan komórki."""
        self.board.toggle_cell(y, x)

    def apply_rules(self, rules):
        """Zastępuje zasady gry nowymi."""
        self.rules = rules


