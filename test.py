import graphviz
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # для грапхвиза, его надо скачать

marker = False


class Graph:    # рисовалка графа, именно самой его картинки в меню
    g = graphviz.Graph(format='png')
    counter = -1
    dict_of_nodes = {}

    def reformat(self):  # подбираем букву по коуyтеру
        self.counter += 1
        return chr(ord('A') + self.counter)

    def reformat_for_invis(self):  # подбираем букву по коуyтеру
        return chr(ord('a') + self.counter)

    def sorts(self, x):
        return x.find('label')

    def add_node(self, value, parent):  # добавление в граф(картинка)
        code_of_node = self.reformat()
        if parent is not None and float(value) >= float(parent):
            self.g.node(self.reformat_for_invis(), '', style='invis')
        self.g.node(code_of_node, value)
        self.dict_of_nodes.update({code_of_node: value})
        code_of_parent = '0'    # код перента
        for i in self.dict_of_nodes.items():
            if i[1] == parent and i[0] != code_of_node:
                temp1 = 0  # кол-во дочерей у перента
                for j in self.g.body:   # проверяем, есть ли у узла 2 сына, если есть то идем искать дальше
                    if j.find(i[0] + ' --') > -1 and j.find('invis') == -1:
                        temp1 += 1
                        if temp1 == 2:
                            break
                else:
                    code_of_parent = i[0]
        else:
            if parent is None:
                return
            if float(value) <= float(parent):
                for i in enumerate(self.g.body):
                    if i[1].find(code_of_parent + ' -- ') > -1 and i[1].find('invis') > -1:
                        self.g.body[i[0]] = '\t' + code_of_parent + ' -- ' + code_of_node
                        self.g.body = sorted(self.g.body, key=self.sorts)
                        break
                else:
                    self.g.edge(code_of_parent, code_of_node)
                    self.g.node(self.reformat_for_invis(), '', style='invis')
                    self.g.edge(code_of_parent, self.reformat_for_invis(), style='invis', weight='10')
            else:
                # self.g.node(self.reformat_for_invis(), '', style='invis')
                self.g.edge(code_of_parent, self.reformat_for_invis(), style='invis', weight='10')
                self.g.edge(code_of_parent, code_of_node)

        self.clear_graph()
        self.g.render('test-output/round-table.gv')     # переписываем граф

    def print_graph(self):  # вывод графа вообще
        self.g.render('test-output/round-table.gv')

    def clear_graph(self):  # для вывода более менее красиво графа
        for i in self.g.body:
            if i.find(' [label="" style=invis]') > -1:  # нашли инвизный узел
                for j in self.g.body:
                    if j.find(' -- ' + i[1] + ' [style=invis weight=10]') > -1:  # ищем ребро к инвизному узлу
                        break
                else:   # если не нашли ребро, то удаляем узел
                    self.g.body.remove(i)


class BinaryTree:   # само бинарное дерево
    g = Graph()
    where = 0

    def __init__(self, value):  # конструктор
        self.value = value  # основное значение
        self.left_child = None  # левый сосу... сынок
        self.right_child = None  # правый сынок

    def insert_node(self, value):  # добавление в дерево
        if value < self.value and self.left_child:
            self.left_child.insert_node(value)
        elif value < self.value:
            self.left_child = BinaryTree(value)
            self.g.add_node(str(value), str(self.value))
        elif value >= self.value and self.right_child:
            self.right_child.insert_node(value)
        else:
            self.right_child = BinaryTree(value)
            self.g.add_node(str(value), str(self.value))

    def pre_order(self, ls):  # Предварительный обход (сверху вниз)
        # print(self.value)     # вывод всего дерева, не нужно для фраемворка
        ls.append(self.value)

        if self.left_child:
            self.left_child.pre_order(ls)

        if self.right_child:
            self.right_child.pre_order(ls)

        return ls

    def in_order(self, ls):  # симметричный обход (снизу вверх)
        if self.left_child:
            self.left_child.in_order(ls)

        ls.append(self.value)
        # print(self.value)

        if self.right_child:
            self.right_child.in_order(ls)

        return ls

    def post_order(self, ls):  # обход в обратном порядке (с низу вверх по рядам)
        if self.left_child:
            self.left_child.post_order(ls)

        if self.right_child:
            self.right_child.post_order(ls)

        ls.append(self.value)
        # print(self.value)
        return ls

    def find_minimum_value(self):  # нужно для поиска минимального значения при коннекте к перенту после удаления
        if self.left_child:
            return self.left_child.find_minimum_value()
        else:
            return self.value

    def find_dublicate(self, value):  # поиск по дереву, для того чтоб не вставлять одинаковые значения
        if value < self.value and self.left_child:
            return self.left_child.find_dublicate(value)
        if value > self.value and self.right_child:
            return self.right_child.find_dublicate(value)
        return value == self.value

    def find_node(self, value, where):  # поиск по дереву, для того чтоб не вставлять одинаковые значения
        if self.value == where:  # ищем элемент Б, попутно чекая какие узлы мы проходим, если проходим A то флажок ставим на тру
            global marker
            marker = True
        if value < self.value and self.left_child:
            return self.left_child.find_node(value, where)
        if value > self.value and self.right_child:
            return self.right_child.find_node(value, where)
        return value == self.value

    def test_find(self, where, what):   # функция задачка, поиск элемента в ветке A (where) элемента B (what)
        if self.find_node(where, where) is False:   # проверяем есть ли A вообще
            return 'Элемента A не найдено', [1, 0, 0, 1]
        if self.find_node(what, where) is False:   # проверяем есть ли B вообще
            return 'Элемента B не найдено', [1, 0, 0, 1]
        global marker      # обращаемся к глоабльной переменной флажку
        marker = False  # ставим её фалс, тип элемент по умолчанию не найден
        self.where = where
        self.find_node(what, where)  # ищем элемент Б, попутно чекая какие узлы мы проходим, если проходим A то флажок ставим на тру
        if marker:
            return 'Элемент присутствует в данной ветке', [0, 1, 0, 1]  # если нашли выводим зеленый цвет и надпись
        else:
            return 'Элемент отсутствует в данной ветке', [1, 0, 0, 1]  # если не нашли выводим красный цвет и надпись


if __name__ == '__main__':  # сюда не зайдет , так как это не скрипт по умолчанию
    b = BinaryTree(1)
    b.insert_node(2)
    b.insert_node(3)
    b.insert_node(4)
    b.insert_node(1.5)
    b.insert_node(1.4)
    b.insert_node(1.6)
    print(b.pre_order([]))
    print(b.test_find(1.5, 4))

