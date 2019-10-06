import threading

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

Config.set('graphics', 'height', 640)

from kivy.app import App
from kivy.uix.gridlayout import GridLayout  # табличное размещение
from kivy.uix.button import Button  # кнопка
from kivy.uix.textinput import TextInput    # поле для ввода
import time

from kivy.uix.widget import Widget


class MyApp(App):   # класс создания главного окна
    # классовые переменные
    left = 1
    right = 0
    x = 3
    ls_of_data = []
    ls_of_labels = []
    key = ''

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
            self.left, self.right = 0, 12
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
                        temp_ls = []

            if instance.text.find('Ш') != -1:
                threading.Thread(target=self.sorting).start()  # делаем второй поток чтоб сразу сортить и выводить на гуи
            else:
                threading.Thread(target=self.sorting2).start()

        gl.add_widget(Button(text='Страны(Ш)',
                             on_press=export))
        gl.add_widget(Button(text='Население(Ш)',
                             on_press=export))
        gl.add_widget(Button(text='Бюджет(Ш)',
                             on_press=export))

        with open('страны.txt', 'r') as f:
            for i in range(1, 40):  # для большего кол-ва записей 79
                a = f.readline()    # считываем с файла и записываем в табл
                self.ls_of_labels.append(TextInput(text=a[:a.find('\n')],
                                                   multiline=False,
                                                   ))
                gl.add_widget(self.ls_of_labels[len(self.ls_of_labels)-1])
        scroll.add_widget(gl)   # привязываем таблицу к скроллу

        def restart(instance):
            with open('страны.txt', 'r') as f:
                for i in range(0, 39):  # для большего кол-ва записей 78
                    a = f.readline()
                    self.ls_of_labels[i].text = a[:a.find('\n')]

        gl.add_widget(Button(text='Страны(В)',
                             on_press=export))
        gl.add_widget(Button(text='Население(В)',
                             on_press=export))
        gl.add_widget(Button(text='Бюджет(В)',
                             on_press=export))
        gl.add_widget(Widget())
        gl.add_widget(Button(text='Переписать',
                             on_press=restart))
        return bl

    @staticmethod
    def checker(value):  # для первой сортировки
        try:
            return int(value)
        except ValueError:
            return 0

    def sorting(self):  # соритировка шейкером (тудым, сюдым)
        while self.left <= self.right:
            for i in range(self.left, self.right, +1):
                a, b = self.ls_of_labels[i * 3 + self.x].text, self.ls_of_labels[i * 3 + 3 + self.x].text
                if self.x != 0:
                    a, b = self.checker(a), self.checker(b)  # проверка на дибила х2
                if a > b:

                    for k in range(0, 3):   # покраска
                        self.ls_of_labels[i * 3 + k].background_color = self.ls_of_labels[i * 3 + 3 + k].background_color = [1, 0, 0, 1]

                    time.sleep(0.1)
                    for k in range(0, 3):   # сама сортировка
                        self.ls_of_labels[i * 3 + k].text, self.ls_of_labels[i * 3 + 3 + k].text = self.ls_of_labels[i * 3 + 3 + k].text, self.ls_of_labels[i * 3 + k].text

                    time.sleep(0.1)

                    for k in range(0, 3):   # покраска
                        self.ls_of_labels[i * 3 + k].background_color = self.ls_of_labels[i * 3 + 3 + k].background_color = [1, 1, 1, 1]
            self.right -= 1

            for i in range(self.right, self.left, -1):
                a, b = self.ls_of_labels[i * 3 - 3 + self.x].text, self.ls_of_labels[i * 3 + self.x].text
                if self.x != 0:
                    a, b = self.checker(a), self.checker(b)  # проверка на дибила х2
                if a > b:

                    for k in range(0, 3):   # покраска
                        self.ls_of_labels[i * 3 - 3 + k].background_color = self.ls_of_labels[i * 3 + k].background_color = [1, 0, 0, 1]

                    time.sleep(0.1)
                    for k in range(0, 3):   # сама сортировка
                        self.ls_of_labels[i * 3 + k].text, self.ls_of_labels[i * 3 - 3 + k].text = self.ls_of_labels[
                                                                                               i * 3 - 3 + k].text, \
                                                                                           self.ls_of_labels[i * 3 + k].text
                    time.sleep(0.1)
                    for k in range(0, 3):   # покраска
                        self.ls_of_labels[i * 3 - 3 + k].background_color = self.ls_of_labels[i * 3 + k].background_color = [1, 1, 1, 1]
            self.left += 1
        else:
            self.x = 3

    def sorting2(self):
        for i in range(self.left, self.right):
            for j in range(i + 1, self.right):
                a, b = self.ls_of_labels[i * 3 + self.x].text, self.ls_of_labels[j * 3 + 3 + self.x].text   # для + читабельности
                if self.x != 0:
                    a, b = self.checker(a), self.checker(b)  # проверка на дибила х2
                if a > b:
                    for k in range(0, 3):   # покраска
                        self.ls_of_labels[i * 3 + k].background_color = self.ls_of_labels[j * 3 + 3 + k].background_color = [1, 0, 0, 1]

                    time.sleep(0.1)
                    for k in range(0, 3):  # сама сортировка
                        self.ls_of_labels[i * 3 + k].text, self.ls_of_labels[j * 3 + 3 + k].text = self.ls_of_labels[j * 3 + 3 + k].text, self.ls_of_labels[i * 3 + k].text

                    time.sleep(0.1)
                    for k in range(0, 3):   # покраска
                        self.ls_of_labels[i * 3 + k].background_color = self.ls_of_labels[j * 3 + 3 + k].background_color = [1, 1, 1, 1]
        else:
            self.x = 3


if __name__ == "__main__":
    MyApp().run()
