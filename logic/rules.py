import random

class Rules:
    """
    Klasa reprezentująca zasady gry w życie.
    Określa warunki przetrwania i narodzin komórek.
    """
    def __init__(self, birth, survive,age):
        """Inicjalizuje zasady gry.
        :param birth: lista liczby sąsiadów powodujących narodziny
        :param survive: lista liczby sąsiadów powodujących przetrwanie
        """
        self.birth = set(birth)
        self.survive = set(survive)
        self.age = age

    def should_live(self, alive, neighbors):
        """Określa, czy komórka powinna być żywa w następnym kroku.
        :param alive: czy komórka jest aktualnie żywa
        :param neighbors: liczba żywych sąsiadów
        :return: True jeśli komórka ma być żywa, False w przeciwnym razie
        """
        if alive:
            return neighbors in self.survive
        else:
            return neighbors in self.birth

    @staticmethod
    def generate_random():
        """Generuje losowe zasady gry.
        :return: instancja Rules z losowymi wartościami
        """
        birth = [i for i in range(1,9) if random.choice([0, 0, 1])]
        survive = [i for i in range(1,9) if random.choice([0, 0, 1])]
        age = random.choice(list(range(-1,10)))

        if not birth:
            birth =[random.choice(list(range(1,9)))]
        if not survive:
            survive = [random.choice(list(range(1,9)))]
        if not age:
            age = random.choice(list(range(1,10)))

        return Rules(birth, survive,age if age else 10)