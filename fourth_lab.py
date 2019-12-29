from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button  # кнопка
from kivy.uix.textinput import TextInput  # поле для ввода
Config.set('graphics', 'height', 640)
from kivy.app import App
import hesh_lib


class MyApp(App):
    def build(self):
        main_bl = BoxLayout(orientation='vertical')     # главный лайаут
        toolbar = BoxLayout(orientation='horizontal',   # лайаут с кнопками/полями
                            size_hint=(1, .07))
        label_of_log = Label(text='Панель действий',    # панель снизу, для просмотра действий
                             color=[1, 0, 0, 1],
                             size_hint=(1, .07),
                             )
        text_input_value = TextInput(hint_text='Введите сюда ключ:',
                                     font_size=12,
                                     multiline=False)
        text_input_data = TextInput(hint_text='Введите сюда значение:',
                                    font_size=12,
                                    multiline=False)
        table = GridLayout(cols=4,  # хеш - таблица
                           rows=6)
        for i in ['Ключ', 'Значение', 'Рез-тат хеш-функции', 'Индекс в массиве']:
            table.add_widget(Button(text=i,
                                    size_hint=(1, .3)))

        def add_in_table(instance):     # действия кнопки добавить
            if text_input_data.text == '' or text_input_value.text == '':   # если какое-то поле пусто
                if text_input_value.text == '':
                    self.clear_text_input(text_input_value)
                    return
                else:
                    self.clear_text_input(text_input_data)
                    return
            else:   # если поля заполненны добавляем в таблицу
                result = hesh_lib.add_in_table(text_input_value.text, text_input_data.text)
                if result[4] is True:
                    label_of_log.color = [0, 1, 0, 1]
                    label_of_log.text = 'Элемент добавлен'
                    for i in range(4):
                        table.add_widget(TextInput(text=str(result[i]),
                                                   readonly=True,
                                                   size=(1, .1)))
                else:
                    label_of_log.color = [1, 0, 0, 1]
                    label_of_log.text = result

        button_to_add = Button(text='Добавить',
                               font_size=15,
                               on_press=add_in_table)

        def find_in_table(instance):
            if text_input_find.text == '':
                self.clear_text_input(text_input_find)
                return
            result = hesh_lib.find_in_table(text_input_find.text)
            if result == -1:
                text_input_find.hint_text = 'Элемент не найден.'
                text_input_find.hint_text_color = [1, 0, 0, 1]
                text_input_find.text = ''
            else:
                text_input_find.hint_text = 'Введите нужный ключ:'
                label_of_log.text = ''
                for i in result:
                    if i[0] == text_input_find.text:
                        label_of_log.text += 'Результат поиска по ключу - ' + text_input_find.text + ': ' + i[1] + ' '

        button_to_find = Button(text='Найти',
                                font_size=15,
                                on_press=find_in_table)
        text_input_find = TextInput(hint_text='Введите нужный ключ:',
                                    font_size=12,
                                    multiline=False,
                                    on_text_validate=find_in_table)

        toolbar.add_widget(text_input_value)
        toolbar.add_widget(text_input_data)
        toolbar.add_widget(button_to_add)
        toolbar.add_widget(text_input_find)
        toolbar.add_widget(button_to_find)

        main_bl.add_widget(toolbar)

        main_bl.add_widget(table)

        main_bl.add_widget(label_of_log)
        return main_bl

    @staticmethod
    def clear_text_input(text_input):
        text_input.text = ''
        text_input.hint_text = 'ВВЕДИТЕ ЧТО-ТО!!!'
        text_input.hint_text_color = [1, 0, 0, 1]


if __name__ == '__main__':
    MyApp().run()
