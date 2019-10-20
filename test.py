import chardet
import graphviz
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # для грапхвиза, его надо скачать


class Graph:
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

    def add_node(self, value, parent):
        code_of_node = self.reformat()
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
                self.g.node(self.reformat_for_invis(), '', style='invis')
                self.g.edge(code_of_parent, self.reformat_for_invis(), style='invis', weight='10')
                self.g.edge(code_of_parent, code_of_node)

        self.g.render('test-output/round-table.gv')

    def print_graph(self):
        self.g.render('test-output/round-table.gv', view=True)

    def task(self, value, parent):
        code_of_parent, code_of_son = '0', '0'
        for i in self.dict_of_nodes.items():
            if i[1] == parent:   # вот тут and code_of_parent == '0'
                code_of_parent = i[0]
            if i[1] == value:   # вот тут and code_of_son == '0'
                code_of_son = i[0]
            if code_of_parent != '0' and code_of_son != '0':
                break

        self.g.body.remove('\t' + code_of_son + ' [label=' + value + ']')   # удаляем узел удаляемого

        code_of_new_son = '0'
        for i in self.g.body:
            if i.find(code_of_son + ' --') > -1 and i.find('invis') == -1:    # нашли дочерние узлы у удаляемого
                code_of_new_son = i[6]
                self.g.body.remove(i)

        for i in enumerate(self.g.body):
            if i[1] == '\t' + code_of_parent + ' -- ' + code_of_son:
                self.g.body[i[0]] = '\t' + code_of_parent + ' -- ' + code_of_new_son

        for i in self.g.body:
            if i.find('\t' + code_of_son + ' --') > -1:
                self.g.body.remove(i)

        self.g.render('test-output/round-table.gv')


class BinaryTree:
    g = Graph()

    def __init__(self, value):  # конструктор
        self.value = value  # основное значение
        self.left_child = None  # левый сосу... сынок
        self.right_child = None  # правый сынок

    def insert_node(self, value):  # добавление в дерево
        if value <= self.value and self.left_child:
            self.left_child.insert_node(value)
        elif value <= self.value:
            self.left_child = BinaryTree(value)
            self.g.add_node(str(value), str(self.value))
        elif value > self.value and self.right_child:
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

    def remove_node(self, value, parent):  # удаление узла, с присвоение к его перенту его чайлдов
        if value < self.value and self.left_child:
            return self.left_child.remove_node(value, self)
        elif value < self.value:
            return False
        elif value > self.value and self.right_child:
            return self.right_child.remove_node(value, self)
        elif value > self.value:
            return False
        else:
            try:
                # global marks
                if self.left_child is None and self.right_child is None and self == parent.left_child:
                    return False
                    # parent.left_child = None
                    # self.clear_node()
                elif self.left_child is None and self.right_child is None and self == parent.right_child:
                    return False
                    # parent.right_child = None
                    # self.clear_node()
                elif self.left_child and self.right_child is None and self == parent.left_child:
                    parent.left_child = self.left_child
                    self.clear_node()
                elif self.left_child and self.right_child is None and self == parent.right_child:
                    parent.right_child = self.left_child
                    self.clear_node()
                elif self.right_child and self.left_child is None and self == parent.left_child:
                    parent.left_child = self.right_child
                    self.clear_node()
                elif self.right_child and self.left_child is None and self == parent.right_child:
                    parent.right_child = self.right_child
                    self.clear_node()
                else:
                    return False
                    # self.value = self.right_child.find_minimum_value()
                    # self.right_child.remove_node(self.value, self)
            except AttributeError:  # если пытается удалить корень
                return False
            else:
                self.g.task(str(value), str(parent.value))    # передаем в задачу родителя и сына,
                return True

    def find_minimum_value(self):  # нужно для поиска минимального значения при коннекте к перенту после удаления
        if self.left_child:
            return self.left_child.find_minimum_value()
        else:
            return self.value

    def clear_node(self):  # удаляем саму ноду + сыновей
        self.value = None
        self.left_child = None
        self.right_child = None

    def find_node(self, value):  # поиск по дереву, для того чтоб не вставлять одинаковые значения
        if value < self.value and self.left_child:
            return self.left_child.find_node(value)
        if value > self.value and self.right_child:
            return self.right_child.find_node(value)

        return value == self.value


if __name__ == '__main__':
    pass
    # b = BinaryTree(1)
    # b.g.add_node("1", None)
    # for i in range(10):
    #     b.insert_node(str(i))
    # b.insert_node('3')
    # b.insert_node('-1')
    # b.insert_node('2')
    # b.insert_node('4')
    # b.insert_node('3')
    # b.insert_node('6')
    # b.insert_node("2.5")
    # b.insert_node('3')
    # b.insert_node('4')
    # b.insert_node('4')
    # b.insert_node('3')
    # b.insert_node('-2')
    # b.insert_node('7')
    # b.insert_node('5')
    # b.insert_node('1')
    # b.insert_node('1')
    # print(b.pre_order([]))
    # b.remove_node('-1', None)
    # print(b.pre_order([]))
    # b.remove_node('1', None)
    # b.insert_node(float("2"))
    # b.insert_node(float("-1"))
    # b.insert_node(float("0.5"))
    # b.insert_node(float("-2"))
    # # print(b.pre_order([]))
    # b.g.print_graph()
