from kivy.config import Config

Config.set('graphics', 'height', 640)
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.gridlayout import GridLayout  # табличное размещение
from kivy.uix.button import Button  # кнопка
from kivy.uix.textinput import TextInput  # поле для ввода
import time
from kivy.uix.widget import Widget
import threading


class MyApp(App):  # класс создания главного окна
    # классовые переменные
    x = 3
    ls_of_data = []
    ls_of_labels = []
    key = ''
    speed = .3
    ppc = []

    def build(self):
        bl = BoxLayout(orientation='horizontal')
        scroll = ScrollView(size_hint=(None, None),  # возможность скроллить
                            size=(800, Window.height),
                            )
        bl.add_widget(scroll)

        gl = GridLayout(cols=3,
                        row_force_default=True,
                        row_default_height=40,
                        width=800,
                        height=40,
                        size_hint=(None, None))  # создаем саму таблицу, в 3 столбика
        gl.bind(minimum_height=gl.setter('height'))

        def export(instance):
            if self.x == 3:  # узнаем какой столбик сортируем и сортируем тот который выбрал юзер
                if instance.text.find('Население') != -1:
                    self.x = 1
                elif instance.text.find('Бюджет') != -1:
                    self.x = 2
                else:
                    self.x = 0

            temp_ls = []
            for i in enumerate(self.ls_of_labels):  # перемещаем объекты в нужной нам последовательности
                if self.x != 0 and i[0] % 3 != 0:  # проверка на дибила
                    try:
                        int(i[1].text)
                    except ValueError:
                        i[1].text = '0'
                temp_ls.append(i[1])
                if (i[0] + 1) % 3 == 0:  # когда контейнер полон, помещаем их в основной корабль, и подаем новый контейнер
                    self.ls_of_data.append(temp_ls)
                    temp_ls2 = []
                    for i in temp_ls:
                        temp_ls2.append(i.text)
                    self.ppc.append(temp_ls2)
                    temp_ls = []

            if instance.text.find('Пузырь') != -1:
                threading.Thread(target=self.sorting).start()  # делаем второй поток чтоб сразу сортить и выводить на гуи
            else:
                threading.Thread(target=self.sorting2).start()

        gl.add_widget(Button(text='Страны(Пузырь)',
                             on_press=export))
        gl.add_widget(Button(text='Население(Пузырь)',
                             on_press=export))
        gl.add_widget(Button(text='Бюджет(Пузырь)',
                             on_press=export))

        with open('страны.txt', 'r') as f:
            for i in range(1, 40):  # для большего кол-ва записей 79
                a = f.readline()  # считываем с файла и записываем в табл
                self.ls_of_labels.append(TextInput(text=a[:a.find('\n')],
                                                   multiline=False,
                                                   ))
                gl.add_widget(self.ls_of_labels[len(self.ls_of_labels) - 1])
        scroll.add_widget(gl)  # привязываем таблицу к скроллу

        def restart(instance):
            with open('страны.txt', 'r') as f:
                for i in range(0, 39):  # для большего кол-ва записей 78
                    a = f.readline()
                    self.ls_of_labels[i].text = a[:a.find('\n')]

        gl.add_widget(Button(text='Страны(Слияние)',
                             on_press=export))
        gl.add_widget(Button(text='Население(Слияние)',
                             on_press=export))
        gl.add_widget(Button(text='Бюджет(Слияние)',
                             on_press=export))

        def low_speed(instance):
            if 0.2 < self.speed:
                self.speed -= 0.1
            else:
                self.speed = 0

        gl.add_widget(Button(text='Ускорить',
                             on_press=low_speed))

        gl.add_widget(Button(text='Переписать',
                             on_press=restart))

        def high_speed(instance):
            if self.speed < 1:
                self.speed += 0.1

        gl.add_widget(Button(text='Замедлить',
                             on_press=high_speed))
        return bl

    def checker(self, value):  # для первой сортировки
        try:
            if self.x != 0:
                return int(value)
            else:
                return value
        except ValueError:
            return 0

    def sorting(self):  # соритировка пузырьком
        for i in range(len(self.ls_of_data) - 1):
            for j in range(len(self.ls_of_data) - i - 1):

                if self.checker(self.ls_of_data[j][self.x].text) > self.checker(self.ls_of_data[j + 1][self.x].text):

                    for k in range(3):  # покраска в красный элементов которые будут вот-вот заменены
                        self.ls_of_data[j][k].background_color = self.ls_of_data[j + 1][k].background_color = (
                        1, 0, 0, 1)
                    time.sleep(self.speed)

                    for k in range(3):
                        self.ls_of_data[j][k].text, self.ls_of_data[j + 1][k].text = self.ls_of_data[j + 1][k].text, \
                                                                                     self.ls_of_data[j][k].text
                    time.sleep(self.speed)

                    for k in range(3):  # покраска обратно
                        self.ls_of_data[j][k].background_color = self.ls_of_data[j + 1][k].background_color = (
                        1, 1, 1, 1)
        self.x = 3
        self.ppc.clear()
        self.ls_of_data.clear()

    def sorting2(self):
        def mergeSort(alist):
            if len(alist) > 1:
                mid = len(alist) // 2
                lefthalf = alist[:mid]
                righthalf = alist[mid:]

                mergeSort(lefthalf)
                mergeSort(righthalf)

                i = 0
                j = 0
                k = 0
                while i < len(lefthalf) and j < len(righthalf):
                    if self.checker(lefthalf[i][self.x]) < self.checker(righthalf[j][self.x]):
                        alist[k] = lefthalf[i]
                        i = i + 1
                    else:
                        alist[k] = righthalf[j]
                        j = j + 1
                    k = k + 1

                while i < len(lefthalf):
                    alist[k] = lefthalf[i]
                    i = i + 1
                    k = k + 1

                while j < len(righthalf):
                    alist[k] = righthalf[j]
                    j = j + 1
                    k = k + 1
        mergeSort(self.ppc)

        for i in range(13):
            for j in range(3):
                self.ls_of_data[i][j].text = self.ppc[i][j]
        self.ppc.clear()
        self.ls_of_data.clear()
        self.x = 3


if __name__ == "__main__":
    MyApp().run()
