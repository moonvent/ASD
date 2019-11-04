from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button  # кнопка
from kivy.uix.textinput import TextInput  # поле для ввода
from kivy.uix.widget import Widget
from test import BinaryTree
Config.set('graphics', 'height', 640)
from kivy.app import App


class MyApp(App):
    root_of_tree = None  # само дерево(бинарное)

    img = Image(
        source='C:\\Users\\Keks\\Documents\\PythonProjects\\ASD\\test-output\\round-table.gv.png')  # сам рисунок графа, и его путь, фраемвор сам грузит его в прогу

    def build(self):

        # ФУНКЦИОНАЛЬНАЯ СРЕДА

        bl_for_tree = BoxLayout(orientation='vertical')  # бокс лайаут для картинки дерева

        # =====================================================================================

        def add(instance):  # функция на добавление элемента в дерево, рисунок
            try:  # проверка на ввод числа (в TextInput уже стоит проверка, но она не пашет на пустое значение)
                float(ti.text)  # работаем с инт , если что менять тут и в TextInput
                if ti.text.find('-0') > -1:
                    raise Exception('Ноль')
            except ValueError:
                ti.text = ''
                ti.hint_text = 'ВВЕДИТЕ ЦЕЛОЕ ЧИСЛО!!!'
                ti.hint_text_color = [1, 0, 0, 1]
                return
            except Exception:
                ti.text = ''
                ti.hint_text = 'ПРИКОЛЬНЫЙ ПРИКОЛ)))'
                ti.hint_text_color = [1, 0, 0, 1]
                return

            # чистим текст лайаут
            value = float(ti.text)
            ti.text = ''
            ti.hint_text_color = [1, 0, 1, 1]
            ti.hint_text = 'Число принято,\nвведите новое:'

            if self.root_of_tree is None:  # если корня нет
                self.root_of_tree = BinaryTree(value)
                self.root_of_tree.g.add_node(str(value), None)
                self.root_of_tree.g.print_graph()
                bl_for_tree.clear_widgets()  # при успешном добавлении чистим изображние

                self.img.reload()  # перезагружаем изображение, то есть старое затираем и новое грузим
                bl_for_tree.add_widget(self.img)
                return
            else:
                self.root_of_tree.insert_node(value)  # вставляем в дерево новый узел

            bl_for_tree.clear_widgets()  # при успешном добавлении чистим изображние

            self.img.reload()  # перезагружаем изображение, то есть старое затираем и новое грузим
            bl_for_tree.add_widget(self.img)

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
        ti.focus = True

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


if __name__ == '__main__':
    MyApp().run()
