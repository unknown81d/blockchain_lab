import itertools
import hashlib
import json

class NonceFinder():
    """
    Класс NonceFinder используется для поиска nonce (число, которое используется в криптографии) 
    для заданного блока данных, которые удовлетворяют условию сложности.
    """
    def __init__(self, data, difficulty):
        """
        Конструктор класса NonceFinder.
        
        Аргументы:
        data -- словарь, содержащий данные, для которых нужно найти nonce.
        difficulty -- целое число, определяющее сложность поиска nonce.
        """
        self.data = data
        self.difficulty = difficulty
        
    def to_long(self, x):
        """
        Метод to_long используется для преобразования строки в целое число.
        
        Аргументы:
        x -- строка, которую нужно преобразовать.
        
        Возвращает:
        Целое число, полученное из строки x.
        """
        return sum(ord(b) << (8*i) for i, b in enumerate(x))

    def combine(self, nonce):
        """
        Метод combine используется для объединения данных и nonce.
        
        Аргументы:
        nonce -- целое число, которое нужно объединить с данными.
        
        Возвращает:
        Строку, полученную из объединения данных и nonce.
        """
        self.data[0]["nonce"] = nonce
        return str(self.data)

    def verify_pow(self, nonce):
        """
        Метод verify_pow используется для проверки, удовлетворяет ли nonce условию сложности.
        
        Аргументы:
        nonce -- целое число, которое нужно проверить.
        
        Возвращает:
        True, если nonce удовлетворяет условию сложности, иначе False.
        """
        h = hashlib.md5(self.combine(nonce).encode()).hexdigest()
        return self.to_long(list(h)) % (1 << self.difficulty) == 0

    def create_pow(self):
        """
        Метод create_pow используется для создания nonce, который удовлетворяет условию сложности.
        
        Возвращает:
        Целое число, которое удовлетворяет условию сложности.
        """
        for nonce in itertools.count(0):
            if self.verify_pow(nonce):
                return nonce
            
    def print_pow(self, nonce):
        """
        Метод print_pow используется для вывода данных и хеша, полученного из объединения данных и nonce.
        
        Аргументы:
        nonce -- целое число, которое нужно объединить с данными и вывести.
        
        Возвращает:
        Строку, содержащую данные и хеш, полученный из объединения данных и nonce.
        """
        return str(self.combine(nonce))+' '+str(hashlib.md5(self.combine(nonce).encode()).hexdigest())
    
    def hash(self):
        """
        Метод hash используется для получения хеша, полученного из объединения данных и nonce.
        
        Возвращает:
        Хеш, полученный из объединения данных и nonce.
        """
        return str(hashlib.md5(self.combine(self.create_pow()).encode()).hexdigest())
            
