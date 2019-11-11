hesh_table = ['--'] * 1000     # создаем массив, нашу будущуу хеш таблицу


def hesh_func(key_word):   # хуш-функция
    string = ''  # строка с переводом букв в числа
    for i in key_word:
        string += str(ord(i))
    summa = 0   # сумма одно, двух, трех - значных чисел
    while len(string) != 0:
        summa += int(string[:3])    # суммируем значения
        string = string[3:]  # режем строку на три символа
    return summa % 1000


def add_in_table(key_word, data):
    if '--' not in hesh_table:
        return 'Таблица заполненна'
    index = hesh_func(key_word)
    if hesh_table[index] == '--':
        hesh_table[index] = [(key_word, data)]
        # print('Исходные данные - ', key_word, ';\nИндекс - ', index, ';\nДанные по этому ключу - ', data, '\n====================')
        print(hesh_table)
        return key_word, data, index, 1, True
    else:   # если случилась коллизия, добавляем в список по заданному элементу
        hesh_table[index].append((key_word, data))  # добавляем в список новый элемент
        return key_word, data, index, len(hesh_table[index]), True


def find_in_table(key_word):
    # нормальный поиск, в плане одного ключа
    # index = hesh_func(key_word)
    # for i in enumerate(hesh_table[index]):
    #     if i[1][0] == key_word:
    #         return 'Ключ - ' + str(key_word), 'Значение - ' + str(i[1][1]), 'Первичный ключ - ' + str(index), 'Вторичный ключ - ' + str(i[0])
    # ненормальный поиск
    if hesh_table[hesh_func(key_word)] == '--':
        return -1
    else:
        return hesh_table[hesh_func(key_word)]


if __name__ == '__main__':
    print(hesh_func('фыф'))
    # pass
