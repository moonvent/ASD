import threading

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.treeview import TreeView, TreeViewLabel

Config.set('graphics', 'height', 640)

from kivy.app import App
from kivy.uix.gridlayout import GridLayout  # табличное размещение
from kivy.uix.button import Button  # кнопка
from kivy.uix.textinput import TextInput  # поле для ввода
import time

from kivy.uix.widget import Widget

from graphviz import Graph
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # для грапхвиза, его надо скачать

result = ''  # нода родитель
marks = False

class BinaryTree:
    def __init__(self, value):  # конструктор
        self.value = value  # основное значение
        self.left_child = None  # левый сосу... сынок
        self.right_child = None  # правый сынок

    def insert_node(self, value):  # добавление в дерево
        global result  # стучимся к глоабльному результату
        if value <= self.value and self.left_child:
            self.left_child.insert_node(value)
        elif value <= self.value:
            self.left_child = BinaryTree(value)
            # print(self.value, 'min')
            result = str(self.value)  # если нашли куда вставить, берем родительсую ноду
        elif value > self.value and self.right_child:
            self.right_child.insert_node(value)
        else:
            self.right_child = BinaryTree(value)
            # print(self.value, 'max')
            result = str(self.value)

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
        global mark
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
                global marks
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

                    marks = True
                    self.clear_node()
                elif self.left_child and self.right_child is None and self == parent.right_child:
                    parent.right_child = self.left_child

                    self.clear_node()
                elif self.right_child and self.left_child is None and self == parent.left_child:
                    parent.left_child = self.right_child

                    marks = True
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


def reformat(counter):  # подбираем букву по коуyтеру
    return chr(ord('A') + counter)


class MyApp(App):
    root_of_tree = BinaryTree(0)  # само дерево(бинарное)
    dot = Graph(format='png')  # сам граф(рисунок)
    counter = 0  # генерация кода для нод, для рисовалки графа
    dict_of_nodes = {}  # запись узлов в словарь для рисования
    temp_var1 = 0  # переменные для рисования)
    temp_var2 = 0
    temp_var3 = '0'
    temp_var4 = '0'
    vihod = False

    def sorts2(self, x):  # сортировка по ключу, а именно для обновления графа
        return x.find('label')

    img = Image(
        source='C:\\PyProj\\ASD\\test-output\\round-table.gv.png')  # сам рисунок графа, и его путь, фраемвор сам грузит его в прогу

    def build(self):

        # ФУНКЦИОНАЛЬНАЯ СРЕДА

        bl_for_tree = BoxLayout(orientation='vertical')  # бокс лайаут для картинки дерева

        # =====================================================================================

        def add(instance):  # функция на добавление элемента в дерево, рисунок
            try:  # проверка на ввод числа (в TextInput уже стоит проверка, но она не пашет на пустое значение)
                float(ti.text)  # работаем с инт , если что менять тут и в TextInput
            except ValueError:
                ti.text = ''
                ti.hint_text = 'ВВЕДИТЕ ЦЕЛОЕ ЧИСЛО!!!'
                ti.hint_text_color = [1, 0, 0, 1]
                return

            # чистим текст лайаут
            value = float(ti.text)
            ti.text = ''
            ti.hint_text_color = [1, 0, 1, 1]
            ti.hint_text = 'Число принято,\nвведите новое:'

            if self.root_of_tree.value == 0:  # если корня нет
                self.root_of_tree = BinaryTree(value)
                return
            else:
                self.root_of_tree.insert_node(value)  # вставляем в дерево новый узел

                if result not in self.dict_of_nodes.values():  # в словарь добавляем значение ноды (value), и её клуч (counter)
                    self.counter += 1   # ключ генерируется для рисовалки, каждый новый узел + 1
                    code = reformat(self.counter)   # мы получаем ключ буквенный, чтоб было легче
                    self.dict_of_nodes.update({code: str(result)})  # добавляем ключ + значеение в словарь
                    self.temp_var1 = code  # вводим в временную переменную ключ, для вывода графа
                else:
                    for i, j in self.dict_of_nodes.items():  # если же всё таки родитель есть, что скорее всего, просто находим его и берем его клуч
                        if result == j:
                            self.temp_var1 = i
                            break

                self.dot.node(self.temp_var1,
                              str(result))  # добавляем ноду родителя в граф, или же если она была просто конектим её

                if ti.text not in self.dict_of_nodes.values():  # если нет дочернего в словаре, добавляем его, по аналогии с перентом
                    self.counter += 1
                    code = reformat(self.counter)
                    self.dict_of_nodes.update({code: str(value)})
                    self.temp_var2 = code
                else:
                    for i, j in self.dict_of_nodes.items():
                        if result == j:
                            self.temp_var2 = i

                self.dot.node(self.temp_var2, str(value))

                rebro = self.temp_var1 + self.temp_var2  # код ребра, обычно просто 2 символа - 12 - первый узел со вторым, это же и ребро
                self.dot.edges([rebro])  # рисуем ребра

                for i in self.dot.body:     # делаем чтоб было как бинарное!!!!
                    if i.find(self.temp_var1 + ' -- ') > -1 and i.find('[style=invis]') == -1:
                        # мы находим узел который уже прицеплен к ноде, допустим перент 1 дочь 2, мы нашли 2
                        for j in enumerate(self.dot.body):
                            # но, так как всё в кодах, мы через код (букву узла) ищем значение этого узла,
                            # то есть 1 - A 2 - B, мы знаем B и ищем значение, то есть 2
                            if j[1].find(i[6:7]) > -1 and j[1].find(' -- ') == -1 and float(j[1][j[1].find('=') + 1:j[1].find(']')]) > value:  # сравниваем его с добавляемым
                                # если тот что блы дочерний, больше, то просто свапаем их в списке узлов (graphviz), далее, до break тупо свап
                                self.dot.body[len(self.dot.body) - 1] = '\t' + self.temp_var1 + ' -- ' + j[1][1:2]
                                for k in enumerate(self.dot.body):
                                    if k[1].find(self.temp_var1 + ' -- ' + j[1][1:2]) > -1:
                                        self.dot.body[k[0]] = '\t' + self.temp_var1 + ' -- ' + self.temp_var2
                                        print('Вошел')
                                        break
                                break
                        break



                self.dot.body = sorted(self.dot.body, key=self.sorts2)   # обновляем граф

                if self.temp_var3 != rebro[:1]:  # для того чтоб нормально рисовалось (как дерево)
                    # если узел который мы добавляем - новый, то бахаем к вместе с ним к перенту невидимый узел,
                    # чтоб он смещал его туда, куда надо
                    self.temp_var3 = rebro[:1]
                    self.dot.node(str(self.counter), "", style='invis')
                    self.dot.edge(rebro[:1], str(self.counter), style='invis')
                else:
                    # если же, уже есть 1 доч. узел у перента, то удаляем инвизный узел и суем обычный,
                    # тем самым дерево остается таким каким было
                    for i in enumerate(self.dot.body):
                        if i[1].find(' -- ' + self.temp_var3) > -1 and i[1].find('[style=invis]') > -1:
                            self.dot.body.pop(i[0])

            bl_for_tree.clear_widgets()  # при успешном добавлении чистим изображние

            self.dot.render(
                'test-output/round-table.gv')  # выводим граф в файл, расширение - выше, путь - папка test-output

            self.img.reload()  # перезагружаем изображение, то есть старое затираем и новое грузим
            bl_for_tree.add_widget(self.img)

        def sorts(x):  # сортировка кода графа  по ребрам
            return x.find('--')

        # =============================================================================

        def task(instance):     # ЗАДАНИЕ ПО ВАРИАНТУ
            try:  # проверка на ввод числа (в TextInput уже стоит проверка, но она не пашет на пустое значение)
                float(ti1.text)  # работаем с инт , если что менять тут и в TextInput
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
            if self.root_of_tree.remove_node(float(value), None) is False:
                ti1.hint_text_color = [1, 0, 0, 1]
                ti1.font_size = 12
                ti1.hint_text = 'Нельзя удалить корень,или узел\nу которого НЕТ дочернего.'
                return

            bl_for_tree.clear_widgets()  # чистим вывод для дерева
            self.dot.body = sorted(self.dot.body, key=sorts)

            n = len(self.dot.body) - 1

            temp = '0'
            for i in enumerate(self.dot.body):  # находим код узла в рисовалке графов, для удаления узла по коду
                if i[1].find('label=' + value) > -1:
                    temp = i[1][1]
                    break
            i = 0  # бегунок по списку рисовалки графа
            mark = False  # если удалили одно ребро , включаем тру и удаляем другие (если есть дочерние)
            temp1 = '0'
            while i < n:
                # print(self.dot.body)
                if self.dot.body[i].find('label=' + value) > -1:  # находим сам узел, то есть код и значение и удаляем его
                    self.dot.body.pop(i)
                    n = len(self.dot.body)
                    i = 0

                if self.dot.body[i].find(temp + ' --') > -1 or self.dot.body[i].find('-- ' + temp) > -1:
                    # находим все связные с удаляемым узлом ребра
                    if mark is False:
                        mark = True
                        temp1 = self.dot.body[i][1]
                        self.dot.body.pop(i)
                        n = len(self.dot.body)
                        i = 0
                    else:
                        self.dot.body[i] = self.dot.body[i][:1] + temp1 + self.dot.body[i][2:]
                        # после удаления узла привязываем его сыновей к его перенту
                        # break
                else:
                    i += 1

            # global marks
            # if marks is True:
            #     marks = False
            #     self.dot.body = list(reversed(self.dot.body))



            self.dot.render('test-output/round-table.gv')

            self.img.reload()
            bl_for_tree.add_widget(self.img)

        # РАБОЧАЯ СРЕДА (лайауты)

        bl = BoxLayout(orientation='vertical')  # главный лайаут, верх - дерево, низ - контрол
        bl_full_control = BoxLayout(orientation='vertical',
                                    size_hint=(1, .2))
        control_bl = BoxLayout(orientation='horizontal',  # управляющий лайаут, (добавить элемент/задача)
                               size_hint=(1, .1))
        order_bl = BoxLayout(orientation='horizontal',  # часть за обходы дерева
                             size_hint=(1, .1))
        bl_full_control.add_widget(control_bl)
        bl_full_control.add_widget(order_bl)
        label = Label(text='Тут будет результат обхода')  # сюда будут выводится результаты обхода
        order_bl.add_widget(label)

        def pre_order(instance):
            label.text = str(self.root_of_tree.pre_order([]))

        def in_order(instance):
            label.text = str(self.root_of_tree.in_order([]))

        def post_order(instance):
            label.text = str(self.root_of_tree.post_order([]))

        order_bl.add_widget(Button(text="Предв. обход",
                                   on_press=pre_order,
                                   size_hint=(0.4, 1)))
        order_bl.add_widget(Button(text="Симм. обход",
                                   on_press=in_order,
                                   size_hint=(0.4, 1)))
        order_bl.add_widget(Button(text="В обратном пор.",
                                   on_press=post_order,
                                   size_hint=(0.4, 1)))
        bl.add_widget(bl_for_tree)
        ti = TextInput(hint_text='Введите элемент:',
                       multiline=False,  # для рабочего энтера
                       input_filter='float',  # автопроверка на инт))
                       on_text_validate=add,  # при нажатии на энтер элемент добавляется
                       )

        control_bl.add_widget(ti)
        control_bl.add_widget(Button(text='Добавить',
                                     on_press=add))
        ti1 = TextInput(hint_text='Введите элемент который\nхотите удалить:',
                        multiline=False,  # для рабочего энтера
                        input_filter='float',  # автопроверка на инт))
                        on_text_validate=task,  # при нажатии на энтер элемент добавляется
                        )
        control_bl.add_widget(ti1)
        control_bl.add_widget(Button(text='Задача',
                                     on_press=task))
        bl.add_widget(bl_full_control)

        return bl


MyApp().run()
