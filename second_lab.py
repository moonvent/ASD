from kivy.config import Config
Config.set('graphics', 'width', 640)    # меняем разрешение, ширина
Config.set('graphics', 'height', 200)   # высота
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button  # кнопка
from kivy.uix.textinput import TextInput    # поле для ввода


class MyApp(App):
    main_list = list()      # главный список
    second_list = list()    # второстепенный список

    def build(self):

        def add_in_main_list(instance):     # функция на добавление в мейн список
            if text_input_for_add_main_ls.text:
                self.main_list.append(text_input_for_add_main_ls.text)
                text_input_for_add_main_ls.hint_text = 'Элемент - ' + text_input_for_add_main_ls.text + ' добавлен.'
                text_input_for_add_main_ls.text = ''
                text_input_for_add_main_ls.hint_text_color = [0, .7, 0, 1]  # меняем цвет отзыва программы
                text_input_main_ls.text = ' -> '.join(self.main_list)   # само добавление в мейн список
            else:   # если юзер ввёл фигню
                text_input_for_add_main_ls.hint_text = 'Ошибка добавления элемента'
                text_input_for_add_main_ls.text = ''
                text_input_for_add_main_ls.hint_text_color = [1, 0, 0, 1]

        def task(instance):
            if len(self.main_list) > 1:
                self.main_list = [self.main_list[-1]] + self.main_list[1:-1] + [self.main_list[0]]
                text_input_main_ls.text = ' -> '.join(self.main_list)

        main = GridLayout(cols=2,  # главный лайаут. в нем все и будет
                          )
        text_input_for_add_main_ls = TextInput(hint_text='Введите элемент для основного списка',
                                               multiline=False,
                                               on_text_validate=add_in_main_list)
        button_for_main_ls = Button(text='Добавить элемент в основной список',
                                    on_press=add_in_main_list)  # привязываем к кнопке функцию - её действия
        text_input_main_ls = TextInput(hint_text='Главный список',
                                       readonly=True,
                                       )
        # далее, тупо добавляем всё в главное окно
        main.add_widget(text_input_for_add_main_ls)
        main.add_widget(button_for_main_ls)
        main.add_widget(text_input_main_ls)
        button_for_task = Button(text='Пуск',
                                 on_press=task)   # привязываем к кнопке функцию - её действия
        main.add_widget(button_for_task)
        return main


if __name__ == '__main__':
    MyApp().run()
