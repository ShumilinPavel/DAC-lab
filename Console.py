# Программный модуль для демонстрации дискреционной модели доступа
class Console:
    def __init__(self, dac):
        # Объект класса DAC
        self.dac = dac
        # Статус пользователя
        self.is_logged_in = False

    # Запуск цикла обработки команд пользователя
    def run(self):
        while True:
            while not self.is_logged_in:
                self.login()
            print('Жду ваших указаний >', end=' ')
            command = input()
            # Маршуртизация команд
            if command == 'quit':
                self.logout()
            elif command == 'read':
                self.execute_read()
            elif command == 'write':
                self.execute_write()
            elif command == 'grant':
                self.execute_grant()

    # Идентификация пользователя
    def login(self):
        print('User:', end=' ')
        user = input()
        if user in self.dac.users:
            self.user = user
            self.is_logged_in = True
            print('Идентификация прошла успешно, добро пожаловать в систему')
            self.print_permissions()
        else:
            print('Ошибка идентификации. Такого пользователя нет в системе')

    # Отображение прав доступа идентифицированного пользователя к объектам
    def print_permissions(self):
        print('Перечень Ваших прав:')
        for file in self.dac.matrix[self.user]:
            permissions_printed_format = self.convert_permissions_to_printed_format(self.dac.matrix[self.user][file])
            permissions_str = ', '.join(permissions_printed_format)
            print('{0:<20}{1}'.format(file + ':', permissions_str))

    # Преобразование внутреннго представления прав доступа в формат для печати
    @staticmethod
    def convert_permissions_to_printed_format(s):
        perms = []
        for perm_encoded in s:
            if perm_encoded == 'r':
                perms.append('Чтение')
            elif perm_encoded == 'w':
                perms.append('Запись')
            elif perm_encoded == 'g':
                perms.append('Передача прав')
        if len(perms) == 0:
            perms.append('Запрет')
        elif len(perms) == 3:
            perms = ['Полные права']
        return perms

    # Завершения сеанса идентифицированного пользователя
    def logout(self):
        print('Работа пользователя {0} завершена. До свидания.'.format(self.user))
        self.is_logged_in = False

    # Проверка введеных пользователем данных на корректность
    def validate_user_data(self, data):
        if 'file' in data.keys() and data['file'] not in self.dac.files:
            print('Такого файла не существует')
            return False
        if 'permission' in data.keys() and data['permission'] not in ['read', 'write', 'grant']:
            print('Такого права доступа не существует')
            return False
        if 'user' in data.keys() and data['user'] not in self.dac.users:
            print('Такого пользователя не существует')
            return False
        return True

    # Чтение объекта
    def execute_read(self):
        print('Над каким объектом производится операция?', end=' ')
        file = input()
        if not self.validate_user_data({'file': file}):
            return
        if 'r' in self.dac.matrix[self.user][file]:
            print('Операция прошла успешно')
        else:
            print('Отказ в выполнении операции. У Вас нет прав для ее осуществления')

    # Изменение объекта
    def execute_write(self):
        print('Над каким объектом производится операция?', end=' ')
        file = input()
        if not self.validate_user_data({'file': file}):
            return
        if 'w' in self.dac.matrix[self.user][file]:
            print('Операция прошла успешно')
        else:
            print('Отказ в выполнении операции. У Вас нет прав для ее осуществления')

    # Предоставление прав на объект другому пользователю
    def execute_grant(self):
        print('Право на какой объект передается?', end=' ')
        file = input()
        print('Какое право передается?', end=' ')
        permission = input()
        print('Какому пользователю передается право?', end=' ')
        user = input()
        if not self.validate_user_data({'file': file, 'permission': permission, 'user': user}):
            return
        if 'g' in self.dac.matrix[self.user][file]:
            perm_encoded = self.convert_permission_to_encoded_format(permission)
            # Изменение матрицы доступа
            self.dac.matrix[user][file].add(perm_encoded)
            print('Операция прошла успешно')
        else:
            print('Отказ в выполнении операции. У Вас нет прав для ее осуществления')

    # Преобразование введенной команды во внутренее представление права доступа
    @staticmethod
    def convert_permission_to_encoded_format(permission):
        if permission == 'read':
            return 'r'
        elif permission == 'write':
            return 'w'
        elif permission == 'grant':
            return 'g'
        Exception('Command not recognised')
