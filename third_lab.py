import threading

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.treeview import TreeView, TreeViewLabel

Config.set('graphics', 'height', 640)

from kivy.app import App
from kivy.uix.gridlayout import GridLayout  # табличное размещение
from kivy.uix.button import Button  # кнопка
from kivy.uix.textinput import TextInput    # поле для ввода
import time

from kivy.uix.widget import Widget


from graphviz import Graph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'   # для грапхвиза, его надо скачать

result = ''     # нода родитель


class BinaryTree:
    def __init__(self, value):      # конструктор
        self.value = value          # основное значение
        self.left_child = None      # левый сосу... сынок
        self.right_child = None     # правый сынок

    def insert_node(self, value):   # добавление в дерево
        global result   # стучимся к глоабльному результату
        if value <= self.value and self.left_child:
            self.left_child.insert_node(value)
        elif value <= self.value:
            self.left_child = BinaryTree(value)
            # print(self.value, 'min')
            result = str(self.value)    # если нашли куда вставить, берем родительсую ноду
        elif value > self.value and self.right_child:
            self.right_child.insert_node(value)
        else:
            self.right_child = BinaryTree(value)
            # print(self.value, 'max')
            result = str(self.value)

    def pre_order(self):
        print(self.value)     # вывод всего дерева, не нужно для фраемворка

        if self.left_child:
            self.left_child.pre_order()

        if self.right_child:
            self.right_child.pre_order()

    def remove_node(self, value, parent):   # удаление узла, с присвоение к его перенту его чайлдов
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
            except AttributeError:      # если пытается удалить корень
                return False
            else:
                return True

    def find_minimum_value(self):   # нужно для поиска минимального значения при коннекте к перенту после удаления
        if self.left_child:
            return self.left_child.find_minimum_value()
        else:
            return self.value

    def clear_node(self):   # удаляем саму ноду + сыновей
        self.value = None
        self.left_child = None
        self.right_child = None

    def find_node(self, value):     # поиск по дереву, для того чтоб не вставлять одинаковые значения
        if value < self.value and self.left_child:
            return self.left_child.find_node(value)
        if value > self.value and self.right_child:
            return self.right_child.find_node(value)

        return value == self.value


def reformat(counter):  # подбираем букву по коуyтеру
    return chr(ord('A') + counter)


class MyApp(App):
    root_of_tree = BinaryTree(0)     # само дерево(бинарное)
    dot = Graph(format='png')    # сам граф(рисунок)
    counter = 0     # генерация кода для нод, для рисовалки графа
    dict_of_nodes = {}  # запись узлов в словарь для рисования
    temp_var1 = 0   # переменные для рисования)
    temp_var2 = 0

    img = Image(source='C:\\PyProj\\ASD\\test-output\\round-table.gv.png')  # сам рисунок графа, и его путь, фраемвор сам грузит его в прогу

    def build(self):

        # ФУНКЦИОНАЛЬНАЯ СРЕДА

        bl_for_tree = BoxLayout(orientation='vertical')     # бокс лайаут для картинки дерева

        def add(instance):  # функция на добавление элемента в дерево, рисунок

            try:       # проверка на ввод числа (в TextInput уже стоит проверка, но она не пашет на пустое значение)
                int(ti.text)    # работаем с инт , если что менять тут и в TextInput
            except ValueError:
                ti.text = ''
                ti.hint_text = 'ВВЕДИТЕ ЦЕЛОЕ ЧИСЛО!!!'
                ti.hint_text_color = [1, 0, 0, 1]
                return

            # чистим текст лайаут
            value = ti.text
            ti.text = ''
            ti.hint_text_color = [1, 0, 1, 1]
            ti.hint_text = 'Число принято,\nвведите новое:'

            if self.root_of_tree.find_node(int(value)) is True:    # повторное значения - фи
                return

            if self.root_of_tree.value == 0:    # если корня нет
                self.root_of_tree = BinaryTree(int(value))
                return
            else:
                self.root_of_tree.insert_node(int(value))   # вставляем в дерево новый узел

                if result not in self.dict_of_nodes.values():   # в словарь добавляем значение ноды (value), и её клуч (counter)
                    self.counter += 1
                    code = reformat(self.counter)
                    self.dict_of_nodes.update({code: result})
                    self.temp_var1 = code  # вводим в временную переменную ключ, для вывода графа
                else:
                    for i, j in self.dict_of_nodes.items(): # если же всё таки родитель есть, что скорее всего, просто находим его и берем его клуч
                        if result == j:
                            self.temp_var1 = i

                self.dot.node(self.temp_var1, result)  # добавляем ноду родителя в граф, или же если она была просто конектим её

                if ti.text not in self.dict_of_nodes.values():  # если нет дочернего в словаре, добавляем его, по аналогии с перентом
                    self.counter += 1
                    code = reformat(self.counter)
                    self.dict_of_nodes.update({code: value})
                    self.temp_var2 = code
                else:
                    for i, j in self.dict_of_nodes.items():
                        if result == j:
                            self.temp_var2 = i

                self.dot.node(self.temp_var2, value)

                rebro = self.temp_var1 + self.temp_var2   # код ребра, обычно просто 2 символа - 12 - первый узел со вторым, это же и ребро
                # print(rebro)
                self.dot.edges([rebro])  # рисуем ребра

            bl_for_tree.clear_widgets()     # при успешном добавлении чистим изображние

            self.dot.render('test-output/round-table.gv')   # выводим граф в файл, расширение - выше, путь - папка test-output

            self.img.reload()   # перезагружаем изображение, то есть старое затираем и новое грузим
            bl_for_tree.add_widget(self.img)

        def sorts(x):   # сортировка кода графа
            return x.find('--')

        def task(instance):

            try:  # проверка на ввод числа (в TextInput уже стоит проверка, но она не пашет на пустое значение)
                int(ti1.text)  # работаем с инт , если что менять тут и в TextInput
            except ValueError:
                ti1.text = ''
                ti1.hint_text = 'ВВЕДИТЕ ЦЕЛОЕ ЧИСЛО!!!'
                ti1.hint_text_color = [1, 0, 0, 1]
                return

            value = ti1.text
            ti1.text = ''
            ti1.hint_text_color = [1, 0, 1, 1]
            ti1.font_size = 16
            ti1.hint_text = 'Число принято,\nэлемент удален.'
            if self.root_of_tree.remove_node(int(value), None) is False:
                ti1.hint_text_color = [1, 0, 0, 1]
                ti1.font_size = 12
                ti1.hint_text = 'Нельзя удалить корень,или узел\nу которого НЕТ дочернего.'
                return

            bl_for_tree.clear_widgets()     # чистим вывод для дерева
            # print(self.dot.body)    # выводим в строках код дерева на рисовал дерева
            self.dot.body = sorted(self.dot.body, key=sorts)

            n = len(self.dot.body) - 1

            temp = '0'
            for i in enumerate(self.dot.body):  # находим код узла в рисовалке графов, для удаления узла по коду
                if i[1].find('label=' + value) > -1:
                    temp = i[1][1]
                    break
            i = 0   # бегунок по списку рисовалки графа
            mark = False    # если удалили одно ребро , включаем тру и удаляем другие (если есть дочерние)
            temp1 = '0'
            while i < n:
                if self.dot.body[i].find('label=' + value) > -1:    # находим сам узел и удаляем его
                    self.dot.body.pop(i)
                    n = len(self.dot.body)
                    i = 0
                if self.dot.body[i].find(temp + ' --') > -1 or self.dot.body[i].find('-- ' + temp) > -1:    # находим все связные с удаляемым узлом ребра
                    if mark is False:
                        mark = True
                        temp1 = self.dot.body[i][1]
                        self.dot.body.pop(i)
                        n = len(self.dot.body)
                        i = 0
                    else:
                        self.dot.body[i] = self.dot.body[i][:1] + temp1 + self.dot.body[i][2:]  # после удаления узла привязываем его сыновей к его перенту
                else:
                    i += 1

            # print(self.dot.body)  # выводим в строках код дерева на рисовал дерева

            self.dot.render('test-output/round-table.gv')

            self.img.reload()
            bl_for_tree.add_widget(self.img)

        # РАБОЧАЯ СРЕДА (лайауты)

        bl = BoxLayout(orientation='vertical')      # главный лайаут, верх - дерево, низ - контрол
        control_bl = BoxLayout(orientation='horizontal',    # управляющий лайаут, (кнопки управления тута)
                               size_hint=(1, .08))
        bl.add_widget(bl_for_tree)
        ti = TextInput(hint_text='Введите элемент:',
                       multiline=False,     # для рабочего энтера
                       input_filter='int',      # автопроверка на инт))
                       on_text_validate=add,    # при нажатии на энтер элемент добавляется
                       )

        control_bl.add_widget(ti)
        control_bl.add_widget(Button(text='Добавить',
                                     on_press=add))
        ti1 = TextInput(hint_text='Введите элемент который хотите удалить:',
                        multiline=False,     # для рабочего энтера
                        input_filter='int',      # автопроверка на инт))
                        on_text_validate=task,    # при нажатии на энтер элемент добавляется
                        )
        control_bl.add_widget(ti1)
        control_bl.add_widget(Button(text='Задача',
                                     on_press=task))
        bl.add_widget(control_bl)

        return bl


MyApp().run()
