import json
import os
import hashlib
from nonce_finder import NonceFinder

class Block():
    """Это класс Block, который представляет блок в блокчейне. 
    В классе есть методы для создания нового блока, получения номера последнего блока, 
    проверки целостности цепочки блоков и получения хэша последнего блока."""
    def __init__(self, name, amount,to_whom_name, nonce = 0, prewiew_hash = '00000000000000000000000000000000'):
        """Инициализирует объект Block с заданным именем, суммой, получателем и опциональными параметрами nonce и prewiew_hash."""
        self.name = name
        self.amount = amount
        self.to_whom_name = to_whom_name
        self.nonce = nonce
        self.prewiew_hash = prewiew_hash
        self.standart_path = 'C:\\Users\\Artyom\\OneDrive\\Рабочий стол\\ИНФВЦЭ 9\\lab9\\src\\blockchain\\books\\'
        
    def get_last_block(self):
        """Возвращает номер последнего блока в блокчейне."""
        #получаем список файлов
        files = os.listdir(self.standart_path)
        files_2 = []
        for file in files:
            #перебираем добавляя в новый список лишь имена файлов
            files_2.append(int(file.split('.')[0]))
        #берем максимальное из них, это и будет посдений файл
        last_file = max(files_2)
        return last_file
    
    def data_creator(self):
        """Создает частично заполненные данные с ключевой информацией. Эти данные включают параметр nonce в поле preview_hash, который будет уточнен."""
        #Создаем данные полупустышки, здесь есть ключевая информация, но параметр nonce в preview_hash будут уточняться

        data = [
        {'nonce':self.nonce}, 
        {'from':self.name, 'amount':self.amount,'to_whom':self.to_whom_name},
        {'prewiew_hash':self.prewiew_hash}
        ]
        return data

    def get_last_block_hash(self, filename):
        """Возвращает хэш данных последнего блока в блокчейне."""
        #берем хеш данных последнего файла в папке
        last_file_data = json.load(open(self.standart_path + str(int(filename) - 1) + '.txt'))

        return NonceFinder(last_file_data[0], 4).hash()
    
    def block_creater(self):
        """Создает новый блок в блокчейне, генерирует данные и вычисляет хэш с использованием класса NonceFinder."""
        
        try:
            last_file = self.get_last_block()
        except ValueError:
            print("[+] Создан первый блок")
            last_file = 0
        filename = str(int(last_file) + 1)
        if last_file == 0:
            data = self.data_creator()
            block_hash = NonceFinder(data, 4).hash()
        else:
            data = self.data_creator()
            data[2]['prewiew_hash'] = self.get_last_block_hash(filename)
            block_hash = NonceFinder(data, 4).hash()
        result_dump_data = [data, block_hash]
        with open(self.standart_path + str(filename) + '.txt','w') as fp:
            json.dump(result_dump_data, fp, indent = 4, ensure_ascii = False)
            
    def blockchain_checker(self):
        """Проверяет целостность блокчейна, сравнивая хэш каждого блока с хэшем предыдущего блока."""
        
        files = os.listdir(self.standart_path)
        try:
            for file in files[1:]:
                checked_file = self.standart_path + file
                #Беру хеш предыдущего файла из файфа начиная со второго.
                checked_from_block_prewiew_hash= json.load(open(checked_file))[0][2]['prewiew_hash']
                checked_prewiew_file = str(int (file.split('.')[0])-1) + ".txt"
                just_right_hash_data = json.load(open(self.standart_path + checked_prewiew_file))[0]
                realy_hash_prewiew_block = NonceFinder(just_right_hash_data, 4).hash()
                if checked_from_block_prewiew_hash == realy_hash_prewiew_block:
                    print('[+] Блок ' + checked_prewiew_file + ' верен')
                else:
                    print('[-] В блоке ' + checked_prewiew_file + ' допущена ошибка!')
        except TypeError:
            print('[+] Для начала проверки цепочки блоков, создайте больше блоков!')
            