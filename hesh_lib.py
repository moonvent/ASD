hesh_table = ['--'] * 5     # создаем массив, нашу будущуу хеш таблицу


def hesh_func(value):   # хуш-функция
    return (ord(value[0]) + ord(value[-1])) * len(value) % len(hesh_table)


def add_in_table(value, data):
    if '--' not in hesh_table:
        return 'Таблица заполненна'
    key = hesh_func(value)  # берем ключ
    if hesh_table[key] == '--':     # если место по ключу пустое, суем туда
        hesh_table[key] = (value, data) # суем значение
        return value, data, key, key, True
    else:   # если случилась коллизия, генерируем новый индекс для вставки в массив
        j = 1
        while True:
            if hesh_table[(key + j) % len(hesh_table)] == '--':		# формула для решений коллизий
                hesh_table[(key + j) % len(hesh_table)] = (value, data)
                return value, data, key, (key + j) % len(hesh_table), True
            else:
                if j == len(hesh_table):
                    return 'Элемент некуда сувать'
                else:
                    j += 1


def find_in_table(value):
    index = hesh_func(value)
    if hesh_table[index][0] == value:  # если ключ равен индексу
        return 'Ключ - ' + str(value), 'Значение - ' + str(hesh_table[index][1]), 'Первичный ключ - ' + str(index), 'Вторичный ключ - ' + str(index)
    j = 1
    while True:
        if hesh_table[(index + j) % len(hesh_table)][0] == value:
            return 'Ключ - ' + str(value), 'Значение - ' + str(hesh_table[(index + j) % len(hesh_table)][1]), 'Первичный ключ - ' + str(index), 'Вторичный ключ - ' + str(index + j % len(hesh_table))
        else:
            if j == len(hesh_table):
                return -1
            else:
                j += 1


if __name__ == '__main__':
    pass
