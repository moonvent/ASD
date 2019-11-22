from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

Config.set('graphics', 'height', 640)

from kivy.app import App
from kivy.uix.button import Button  # кнопка
from kivy.uix.textinput import TextInput    # поле для ввода


class ListNode:  # сам узел
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:   # реализация самого списка
    def __init__(self):
        self.head = None    # начало начал
        self.tail = None    # для создания очереди

    def add(self, node):    # добавление в список (механизм очереди)
        if self.head is None:
            node.next = self.head
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def print(self):    # вывод списка
        current = self.head
        all_list = ''
        while current is not None:
            all_list += str(current.value) + ' '
            current = current.next
            # print(all_list)
        return all_list

    def swap(self, f_num, s_num):     # задача по варианту
        pre = self.head
        if self.head == self.tail or self.head is None:  # если дырка - выкидываем
            return True
        size = 0    # для счета кол-ва элемента
        while pre is not None:
            size += 1   # счет колва
            pre = pre.next  # доходим до хвоста
        if size < s_num or size < f_num or f_num == 0 or s_num == 0:    # если кол-во меньше
            return True
        if f_num > s_num:
            f_num, s_num = s_num, f_num
        counter = 0     # счетчик элементов
        pre = self.head
        temp = 0
        while pre is not None:  # основной цицкл
            counter += 1
            if counter == f_num:    # нашли первый элемент
                temp = pre.value
            if counter == s_num:    # нашли второй
                temp, pre.value = pre.value, temp   # поменяли второй элемент
                pre = self.head
                counter = 0
                while pre is not None:  # идем к первому элементу
                    counter += 1
                    if counter == f_num:    # нашли первый , поменяли его на старый второй
                        pre.value = temp
                        return
                    pre = pre.next
            pre = pre.next


class MyApp(App, LinkedList):
    ls = LinkedList()   # первый списк
    ls2 = LinkedList()   # второй списк
    main = BoxLayout(orientation='horizontal')  # главный лайаут. в нем все и будет

    def checker(self, value):   # проверка на ввод, чтоб юзер не вводил каку в i-ый и j-ый
        try:
            return int(value)
        except ValueError:
            return 'Error'

    def build(self):
        bl = BoxLayout(orientation='vertical',  # настраиваем вывод первого списка
                       padding=[80, 10, 80, 10],
                       height=50,
                       spacing=35,
                       size_hint=(1, None))  # создание красоты для списка
        bl.bind(minimum_height=bl.setter('height'))
        bl2 = BoxLayout(orientation='vertical',
                        padding=[30, 30, 30, 30],
                        spacing=20)  # создание самого рабочего стола, в который мы и будем пихать кнопки и прочее
        bl3 = BoxLayout(orientation='vertical',  # настраиваем вывод второго списка
                        padding=[10, 10, 10, 10],
                        spacing=35)
        bl3.bind(minimum_height=bl3.setter('height'))
        scroll = ScrollView(size_hint=(None, None),  # возможность скроллить
                            size=(Window.width / 3, 600))
        scroll.add_widget(bl)
        self.main.add_widget(scroll)
        self.main.add_widget(bl2)
        self.main.add_widget(bl3)

        fti = TextInput(hint_text="Какой элемент:>",
                                  multiline=False,
                                  size=(100, 100),
                                  size_hint=(1, .07),
                                  input_filter='float',
                                  )
        bl3.add_widget(fti)
        sti = TextInput(hint_text="На какой элемент:>",
                                  multiline=False,
                                  size=(100, 100),
                                  size_hint=(1, .07),
                                  input_filter='float',)
        bl3.add_widget(sti)

        ti = TextInput(hint_text='Введите элемент списка:',
                       padding=[10, 10, 10, 10],
                       multiline=False,
                       input_filter='float',)
        bl2.add_widget(ti)

        def add_elem(instance):  # добавляем элемент с попутным выводом на экран
            if len(ti.text) == 0:
                return
            temp = str(len(bl.children) + 1)
            temp = str(int(temp) / 2 + 1)
            temp = temp[:temp.find('.')] + '. '
            self.ls.add(ListNode(ti.text))
            bl.add_widget(Label(text=temp + ti.text,
                                font_size=30))
            bl.add_widget(Button(text="||" + "\nV",
                                 background_color=[1, 1, 1, 1]))
            ti.text = ''

        bl2.add_widget(Button(text='Добавить элемент',
                              on_press=add_elem))

        def task(instance):
            if self.checker(fti.text) == 'Error' or self.checker(sti.text) == 'Error':  # если юзер ввел плохие числа
                fti.text = sti.text = ''
                fti.hint_text_color = sti.hint_text_color = [1, 0, 0, 1]
                sti.hint_text = fti.hint_text = "Введите числа сюда!!!"
                return
            if self.ls.swap(int(fti.text), int(sti.text)):  # делаем свое грязное дело, если юзер ввел числа не удовлетворяющие диапозону списка
                fti.text = sti.text = ''
                fti.hint_text_color = sti.hint_text_color = [1, 0, 0, 1]
                sti.hint_text = fti.hint_text = "Введите числа до последнего\nэлемента списка."
                return
            else:
                fti.text = sti.text = ''
                fti.hint_text_color = sti.hint_text_color = [1, 1, 1, 1]
                sti.hint_text = fti.hint_text = "Введите числа."
                # return
            bl.clear_widgets()  # чистим виджеты,
            fti.text = sti.text = ''
            temp = self.ls.print()  # получаем новый список
            if len(temp) == 0:
                return
            counter = 0
            while temp.find(' ') != -1:  # выводим новый список на экран
                counter += 1
                bl.add_widget(Label(text=str(counter) + '. ' + temp[:temp.find(' ')],
                                    font_size=30))
                bl.add_widget(Button(text="||" + "\nV",
                                     background_color=[1, 1, 1, 1]))
                temp = temp[temp.find(' ') + 1:]

        bl2.add_widget(Button(text='Задача:\nПоменять i-ый на j-ый\n',
                              font_size=16,
                              on_press=task))

        return self.main


if __name__ == '__main__':
    MyApp().run()
