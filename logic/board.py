import copy
import random


class Board:
    """
    Klasa reprezentująca planszę gry i jej stan.
    Przechowuje komórki i wiek komórek.
    """
    def __init__(self, rows, cols,initial_grid):
        """Inicjalizuje pustą planszę.
        :param rows: liczba wierszy
        :param cols: liczba kolumn
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[0]*cols for _ in range(rows)] if not initial_grid else initial_grid
        self.age_grid = copy.deepcopy(self.grid)


    def reset(self):
        """Resetuje planszę do stanu początkowego."""
        self.grid = [[0]*self.cols for _ in range(self.rows)]
        self.age_grid = [[0]*self.cols for _ in range(self.rows)]

    def toggle_cell(self, y, x):
        """Zamienia stan komórki na przeciwny.
        :param y: wiersz
        :param x: kolumna
        """
        self.grid[y][x] = 1 - self.grid[y][x]
        self.age_grid[y][x] = 1 if self.grid[y][x] else 0

    def step(self, rules):
        """Wykonuje jeden krok symulacji.
        :param rules: zasady gry
        """
        new_grid = [[0]*self.cols for _ in range(self.rows)]
        new_age = [[0]*self.cols for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.cols):
                neighbors = self.get_neighbors(y, x)
                if self.grid[y][x]:
                    if neighbors in rules.survive and (rules.age == -1 or self.age_grid[y][x] < rules.age):
                        new_grid[y][x] = 1
                        new_age[y][x] = self.age_grid[y][x] + 1
                else:
                    if neighbors in rules.birth:
                        new_grid[y][x] = 1
                        new_age[y][x] = 1

        self.grid = new_grid
        self.age_grid = new_age

    def get_neighbors(self, y, x):
        """Zwraca liczbę żywych sąsiadów komórki.
        :param y: wiersz
        :param x: kolumna
        :return: liczba sąsiadów
        """
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny = (y + dy) % self.rows
                nx = (x + dx) % self.cols
                count += self.grid[ny][nx]
        return count

    def randomize(self, prob=0.2):
        """Losowo wypełnia planszę komórkami.
        :param prob: prawdopodobieństwo żywej komórki
        """
        for y in range(self.rows):
            for x in range(self.cols):
                self.grid[y][x] = 1 if random.random() < prob else 0
                self.age_grid[y][x] = 1 if self.grid[y][x] else 0