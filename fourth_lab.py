hesh_table = [None] * 5     # создаем массив, нашу будущуу хеш таблицу


def hesh_func(value):   # хуш-функция
    summa = 0
    for i in enumerate(value):
        if i[0] % 2 == 0:
            summa += ord(i[1])
    else:
        return (summa * len(value)) % len(hesh_table)


def add_in_table(value):
    key = hesh_func(value)
    if hesh_table[key] is None:
        hesh_table[key] = value
    else:   # если случилась коллизия, генерируем новый индекс для вставки в массив
        j = 1
        while True:
            if hesh_table[key + pow(j, 2) % len(hesh_table)] is None:
                hesh_table[key + pow(j, 2) % len(hesh_table)] = value
                return
            else:
                j += 1


def find_in_table(value):
    index = hesh_func(value)
    if hesh_table[index] == value:  # если ключ равен индексу
        print('Индекс заданного элемента', index)
    else:   # если ключ и индекс не совпали, то по алгоритму ищме значение
        j = 1
        while True:
            if hesh_table[index + pow(j, 2) % len(hesh_table)] == value:
                print('Индекс заданного элемента', index + pow(j, 2) % len(hesh_table))
                return
            else:
                j += 1


if __name__ == '__main__':
    add_in_table('Василий Царь')
    print(hesh_table)
    add_in_table('Василий Пуп')
    print(hesh_table)
    add_in_table('Никита')
    print(hesh_table)
    add_in_table('Василий Царь')
    print(hesh_table)
    add_in_table('Василий Царь')
    print(hesh_table)
    add_in_table('Василий Царь')
    print(hesh_table)

    find_in_table('Василий Царь')
