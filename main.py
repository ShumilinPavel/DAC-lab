from DAC import *
from Console import *

# Вариант 21: 7 субъетков, 3 объекта
# S = {чтение (r), запись (w), передача прав (g)}


if __name__ == '__main__':
    dac = DAC()
    console = Console(dac)
    console.run()
