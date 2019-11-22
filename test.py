import chardet
import graphviz
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # для грапхвиза, его надо скачать

counter, pre_minimum, minimun = 0, 0, 0


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
        print(self.dict_of_nodes)
        print(code_of_parent, parent, 'Отец')
        print(code_of_node, value, 'Сын')
        print(self.g.body)
        self.g.render('test-output/round-table.gv')     # переписываем граф

    def print_graph(self):
        self.g.render('test-output/round-table.gv')

    def clear_graph(self):
        for i in self.g.body:
            if i.find(' [label="" style=invis]') > -1:  # нашли инвизный узел
                for j in self.g.body:
                    if j.find(' -- ' + i[1] + ' [style=invis weight=10]') > -1:  # ищем ребро к инвизному узлу
                        break
                else:   # если не нашли ребро, то удаляем узел
                    self.g.body.remove(i)

    def for_leaf(self, value, parent):
        self.clear_graph()
        code_of_parent, code_of_son = '0', '0'
        for i in self.dict_of_nodes.items():
            if i[1] == parent:  # вот тут and code_of_parent == '0'
                code_of_parent = i[0]
            if i[1] == value:  # вот тут and code_of_son == '0'
                code_of_son = i[0]
            if code_of_parent != '0' and code_of_son != '0':
                break

        self.dict_of_nodes.pop(code_of_son)     # удаление из словаря лишнего узла
        self.g.body.remove('\t' + code_of_son + ' [label=' + value + ']')  # удаляем узел удаляемого

        for i in self.g.body:   # удаление ребра
            if i.find(code_of_son) > -1:
                self.g.body.remove(i)
                # break     # баг, если 1 2 3 удалить 3 2

        self.g.render('test-output/round-table.gv')     # переписываем граф

    def for_one_son(self, value, parent):
        self.clear_graph()
        code_of_parent, code_of_son = '0', '0'
        for i in self.dict_of_nodes.items():
            if i[1] == parent:   # вот тут and code_of_parent == '0'
                code_of_parent = i[0]
            if i[1] == value:   # вот тут and code_of_son == '0'
                code_of_son = i[0]
            if code_of_parent != '0' and code_of_son != '0':
                break

        self.dict_of_nodes.pop(code_of_son)  # удаления узла из словаря с узлами
        self.g.body.remove('\t' + code_of_son + ' [label=' + value + ']')   # удаляем узел удаляемого

        code_of_new_son = '0'
        for i in self.g.body:   # ведем поиск привязанных узлов к удаляемому (удаляемый -- нужный для сейва)
            if i.find(code_of_son + ' --') > -1 and i.find('invis') == -1:    # нашли дочерние узлы у удаляемого
                code_of_new_son = i[6]  # сохраняем код дочернего узла
                self.g.body.remove(i)

        for i in enumerate(self.g.body):    # добавляем к перенту удаляемого узла дочерний зузел удаляемого узла
            if i[1] == '\t' + code_of_parent + ' -- ' + code_of_son:
                self.g.body[i[0]] = '\t' + code_of_parent + ' -- ' + code_of_new_son

        i, n = 0, len(self.g.body)

        # print(self.g.body)
        while i < n:
            if self.g.body[i].find('\t' + code_of_son + ' --') > -1:
                self.g.body.pop(i)
                i = 0
                n -= 1
            else:
                i += 1

        # print(self.g.body)

        # for i in self.g.body:   # удаляем все инвизные узлы у узла который мы удалили
        #     if i.find('\t' + code_of_son + ' --') > -1:
        #         if i.find('invis') > -1:    # удаление ещё и узлов инвизных, если будет карать , коментнуть
        #             self.g.body.remove('\t' + i[6] + ' [label="" style=invis]')
        #         self.g.body.remove(i)

        self.g.render('test-output/round-table.gv')     # переписываем граф

    def for_two_son(self, value, parent, new_value):
        # print(value, parent, new_value)
        self.clear_graph()
        code_of_parent, code_of_son = '0', '0'
        for i in self.dict_of_nodes.items():
            if i[1] == parent:  # вот тут and code_of_parent == '0'
                code_of_parent = i[0]
            if i[1] == value:  # вот тут and code_of_son == '0'
                code_of_son = i[0]
            if code_of_parent != '0' and code_of_son != '0':
                break

        self.for_leaf(new_value, value)

        for i in enumerate(self.g.body):    # меняем значение узла
            if i[1] == '\t' + code_of_son + ' [label=' + value + ']':
                self.g.body[i[0]] = '\t' + code_of_son + ' [label=' + new_value + ']'
                self.dict_of_nodes[code_of_son] = new_value
                break

        self.g.render('test-output/round-table.gv')  # переписываем граф

    def for_two_son_and_one_root(self, value, parent):
        # print(value, parent)
        self.clear_graph()
        code_of_parent, code_of_son = '0', '0'
        for i in self.dict_of_nodes.items():
            if i[1] == parent:  # вот тут and code_of_parent == '0'
                code_of_parent = i[0]
            if i[1] == value:  # вот тут and code_of_son == '0'
                code_of_son = i[0]
            if code_of_parent != '0' and code_of_son != '0':
                break

        temp_node = str()
        for i in self.g.body:   # находим узлы дочерние от дочернего, чтоб перепривязать к отцу
            if i.find(code_of_son + ' -- ') > -1:
                if i.find('invis') == -1:   # записываем дочерние которые не инвиз
                    temp_node = i[6]  # код узла дочернего от дочерненго перента
                    # print(temp_node)
                    self.g.body.remove(i)   # удаляем все узлы у него, и дочерние тоже, если не будет работать убрать условие и поставить брейк

        for i in self.g.body:   # чистка дочернего узла, от инвизных
            if i.find(code_of_son + ' -- ') > -1 and i.find('invis') > -1:
                self.g.body.remove(i)
                break

        self.g.body.remove('\t' + code_of_son + ' [label=' + value + ']')   # удалил нужный узел
        self.dict_of_nodes.pop(code_of_son)
        self.dict_of_nodes[code_of_parent] = value

        for i in enumerate(self.g.body):    # переписываем перента на сына, меняем значение сына на отца то есть
            if i[1].find('\t' + code_of_parent + ' [label=' + parent + ']') > -1:
                self.g.body[i[0]] = '\t' + code_of_parent + ' [label=' + value + ']'
                break

        for i in enumerate(self.g.body):    # привязываем дочерний узел у дочернего к перенту, перенту
            if i[1].find(code_of_parent + ' -- ' + code_of_son) > -1:
                self.g.body[i[0]] = '\t' + code_of_parent + ' -- ' + temp_node
                break

        self.g.render('test-output/round-table.gv')  # переписываем граф


class BinaryTree:
    g = Graph()

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
            global counter, pre_minimum, minimun
            try:
                if self.left_child is None and self.right_child is None and self == parent.left_child:  # удаление листа
                    parent.left_child = None
                    self.clear_node()
                    if counter > 0:  # если удаляем элемент с двумя сыновьями
                        return
                    else:
                        self.g.for_leaf(str(value), str(parent.value))  # передаем в задачу родителя и сына,
                elif self.left_child is None and self.right_child is None and self == parent.right_child:  # удаление листа
                    parent.right_child = None
                    self.clear_node()
                    if counter > 0:  # если удаляем элемент с двумя сыновьями
                        return
                    else:
                        self.g.for_leaf(str(value), str(parent.value))  # передаем в задачу родителя и сына,
                elif self.left_child and self.right_child is None and self == parent.left_child:    # удаление если есть один сын
                    print('sex3')
                    parent.left_child = self.left_child
                    self.clear_node()
                    self.g.for_one_son(str(value), str(parent.value))  # передаем в задачу родителя и сына,
                elif self.left_child and self.right_child is None and self == parent.right_child:   # один сын
                    print('sex2')
                    parent.right_child = self.left_child
                    self.clear_node()
                    self.g.for_one_son(str(value), str(parent.value))  # передаем в задачу родителя и сына,
                elif self.right_child and self.left_child is None and self == parent.left_child:   # один сын
                    print('sex1')
                    parent.left_child = self.right_child
                    self.clear_node()
                    self.g.for_one_son(str(value), str(parent.value))  # передаем в задачу родителя и сына,
                elif self.right_child and self.left_child is None and self == parent.right_child:   # один сын
                    print('sex')
                    if counter == 1:    # флаг, если удаляем узел с двумя
                        counter += 1
                    parent.right_child = self.right_child
                    self.clear_node()
                    if counter == 2:    # выходим из функции если с двумя, так как для этого другая удалялка
                        return
                    else:
                        self.g.for_one_son(str(value), str(parent.value))  # передаем в задачу родителя и сына,
                else:   # если два сына
                    counter += 1    # ставим метку что удаляем узел с 2
                    pre_minimum = self.value
                    minimun = self.right_child.find_minimum_value()
                    self.value = self.right_child.find_minimum_value()
                    self.right_child.remove_node(self.value, self)
            except AttributeError:  # если пытается удалить корень
                return False
            else:
                # print(pre_minimum, parent.value, minimun, 'keks', self.value, value)
                if counter == 1:    # если у узла с двумя удаляемыми есть меньший элемент в правой левой ветке
                    self.g.for_two_son(str(pre_minimum), str(parent.value), str(minimun))
                elif counter == 2:  # если его нет
                    self.g.for_two_son_and_one_root(str(self.value), str(value))
                counter = 0
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
