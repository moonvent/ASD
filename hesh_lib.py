hesh_table = ['--'] * 5     # создаем массив, нашу будущуу хеш таблицу


def hesh_func(value):   # хуш-функция
    summa = 0
    for i in enumerate(value):
        if i[0] % 2 == 0:
            summa += ord(i[1])
    else:
        return (summa * len(value)) % len(hesh_table)


def add_in_table(value, data):
    if '--' not in hesh_table:
        return 'Таблица заполненна'
    key = hesh_func(value)
    if hesh_table[key] == '--':
        hesh_table[key] = (value, data)
        # print('Исходные данные - ', value, ';\nИндекс - ', key, ';\nДанные по этому ключу - ', data, '\n====================')
        return value, data, key, key, True
    else:   # если случилась коллизия, генерируем новый индекс для вставки в массив
        j = 1
        while True:
            if hesh_table[(key + pow(j, 2)) % len(hesh_table)] == '--':
                # print('Исходные данные - ',  value, ';\nИндекс - ', (key + pow(j, 2)) % len(hesh_table), ';\nДанные по этому ключу - ', data, '\n====================')
                hesh_table[(key + pow(j, 2)) % len(hesh_table)] = (value, data)
                return value, data, key, (key + pow(j, 2)) % len(hesh_table), True
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
        if hesh_table[(index + pow(j, 2)) % len(hesh_table)][0] == value:
            return 'Ключ - ' + str(value), 'Значение - ' + str(hesh_table[(index + pow(j, 2)) % len(hesh_table)][1]), 'Первичный ключ - ' + str(index), 'Вторичный ключ - ' + str(index + pow(j, 2) % len(hesh_table))
        else:
            if j == len(hesh_table):
                return -1
            else:
                j += 1


if __name__ == '__main__':
    add_in_table('Василий Царь', '20 гривень')
    # print(hesh_table)
    add_in_table('Василий Пуп', '30 гривень')
    # print(hesh_table)
    add_in_table('Никита', '40 гривень')
    input()
    # print(hesh_table)
    # add_in_table('Василий Царь')
    # print(hesh_table)
    # add_in_table('Василий Царь')
    # print(hesh_table)
    # add_in_table('Василий Царь')
    # print(hesh_table)
    # pass
