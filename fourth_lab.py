from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button  # кнопка
from kivy.uix.textinput import TextInput  # поле для ввода
from kivy.uix.widget import Widget
Config.set('graphics', 'height', 640)
from kivy.app import App
import hesh_lib


class MyApp(App):
    def build(self):
        main_bl = BoxLayout(orientation='vertical')     # главный лайаут
        toolbar = BoxLayout(orientation='horizontal',   # лайаут с кнопками/полями
                            size_hint=(1, .07))
        text_input_value = TextInput(hint_text='Введите сюда ключ:',
                                     font_size=20)
        text_input_data = TextInput(hint_text='Введите сюда значение:',
                                    font_size=20)

        def add_in_table(instance):
            if text_input_data.text == '' or text_input_value.text == '':   # если какое-то поле пусто
                if text_input_data.text == '':
                    self.clear_text_input(text_input_data)
                    return
                else:
                    self.clear_text_input(text_input_value)
                    return
            else:
                hesh_lib.add_in_table(text_input_value, text_input_data)

        button_to_add = Button(text='Добавить',
                               font_size=20,
                               on_press=add_in_table)
        toolbar.add_widget(text_input_value)
        toolbar.add_widget(text_input_data)
        toolbar.add_widget(button_to_add)
        table = GridLayout(cols=2)  # хеш - таблица
        main_bl.add_widget(toolbar)
        main_bl.add_widget(table)
        return main_bl

    def clear_text_input(self, text_input):
        text_input.text = ''
        text_input.hint_text = 'ВВЕДИТЕ ЧТО-ТО ВЕЩЕСТВЕННОЕ!!!'
        text_input.hint_text_color = [1, 0, 0, 1]

if __name__ == '__main__':
    MyApp().run()
