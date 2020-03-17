from random import randrange


# Discretionary access control
class DAC:
    def __init__(self):
        # Идентификаторы пользователей
        self.users = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Mallory', 'Kesha']
        # Объекты
        self.files = ['readme.txt', 'magick', 'storage']
        # Идентификатор администратора, обладающего полными правами
        self.admin = self.users[len(self.users) - 1]  # Kesha
        # Матрица доступа
        self.matrix = self.generate_dac_matrix()

    # Генерация матрицы со случайными правами доступа
    def generate_dac_matrix(self):
        dac_matrix = dict()
        for user in self.users:
            dac_matrix[user] = dict()
            for file in self.files:
                # Администратор обладает всеми правами
                if user == self.admin:
                    dac_matrix[self.admin][file] = {'r', 'w', 'g'}
                else:
                    dac_matrix[user][file] = self.generate_random_subset({'r', 'w', 'g'})
        return dac_matrix

    # Случайное множество прав
    @staticmethod
    def generate_random_subset(s):
        return set(filter(lambda x: randrange(2), s))
