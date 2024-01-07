from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line
import speech_recognition
import pyttsx3
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView

glob_viewer = ['numbers', 'zero']
dict_of_numbers = {'one': ['один', '1'], 'two': ['два', '2'], 'three': ['три', '3'], 'four': ['четыре', '4'],
                   'five': ['пять', '5'], 'six': ['шесть', '6'], 'seven': ['семь', '7'],
                   'eight': ['восемь', '8'], 'nine': ['девять', '9'], 'ten': ['десять', '10']}

dict_of_shapes = {'квадрат': 'square', 'прямоугольник': 'rectangle', 'ромб': 'rhombus',
                  'трапеция': 'trapezium', 'параллелограм': 'parallelogram',
                  'треугольник': 'triangle', 'звезда': 'star', 'пятиугольник': 'pentagon',
                  'шестиугольник': 'hexagon', 'восьмиугольник': 'octagon',
                  'круг': 'circle', 'овал': 'ellipse', 'полумесяц': 'crescent'}

dict_of_colors = {'белый': 'white', 'серый': 'gray', 'черный': 'black', 'красный': 'red', 'оранжевый': 'orange',
                  'жёлтый': 'yellow', 'зелёный': 'green', 'голубой': 'turquoise', 'синий': 'blue',
                  'фиолетовый': 'purple', 'розовый': 'pink', 'коричневый': 'brown',
                  'бордовый': 'burgundy', 'салатовый': 'light_green'}

colors_to_paint = {'red': (1, 0, 0), 'yellow': (1, 1, 0), 'blue': (0, 0, 1),
          'white': (1, 1, 1), 'green': (0, 1, 0), 'purple': (1, 0, 1)}
color = colors_to_paint['blue']


def record_and_recognize_audio(microphone, recognizer):
    with microphone:
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        audio = recognizer.listen(microphone, 7, 5)
        try:
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()
        except:
            recognized_data = "No"

        return recognized_data


def start_recognize():
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    speak = pyttsx3.init()
    speak.setProperty('voice', 'ru')

    voice_input = record_and_recognize_audio(microphone, recognizer)
    return voice_input


class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(*color)
            d = 10
            touch.ud['line'] = Line(points=(touch.x, touch.y), size=(2*d, 2*d))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class MyPaintApp(App):

    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget()
        parent.add_widget(self.painter)

        clear_btn = Button(text='Clear', size_hint=(2., .7), pos=(50, 50),
                          background_normal='buttons/clear_btn.png',
                          background_down='buttons/clear_btn.png')
        clear_btn.bind(on_release=self.clear_rec)
        parent.add_widget(clear_btn)

        red_btn = Button(text='Red', size_hint=(2., .7), pos=(850, 600),
                         background_normal='buttons/red_btn_normal.png',
                         background_down='buttons/red_btn_down.png')
        red_btn.bind(on_release=lambda x: self.change_color(('red')))
        parent.add_widget(red_btn)

        blue_btn = Button(text='Blue', size_hint=(2., .7),
                         pos=(850, 500), background_normal='buttons/blue_btn_normal.png',
                         background_down='buttons/blue_btn_down.png')
        blue_btn.bind(on_release=lambda x: self.change_color(('blue')))
        parent.add_widget(blue_btn)

        green_btn = Button(text='Green', size_hint=(2., .7),
                           pos=(850, 400), background_normal='buttons/green_btn_normal.png',
                           background_down='buttons/green_btn_down.png')
        green_btn.bind(on_release=lambda x: self.change_color(('green')))
        parent.add_widget(green_btn)

        white_btn = Button(text='White', size_hint=(2., .7),
                         pos=(850, 300), background_normal='buttons/white_btn_normal.png',
                         background_down='buttons/white_btn_down.png')
        white_btn.bind(on_release=lambda x: self.change_color(('white')))
        parent.add_widget(white_btn)

        yellow_btn = Button(text='Yellow', size_hint=(2., .7),
                            pos=(850, 200), background_normal='buttons/yellow_btn_normal.png',
                            background_down='buttons/yellow_btn_down.png')
        yellow_btn.bind(on_release=lambda x: self.change_color(('yellow')))
        parent.add_widget(yellow_btn)

        purple_btn = Button(text='Purple', size_hint=(2., .7),
                            pos=(850, 100), background_normal='buttons/purple_btn_normal.png',
                            background_down='buttons/purple_btn_down.png')
        purple_btn.bind(on_release=lambda x: self.change_color('purple'))
        parent.add_widget(purple_btn)

        return parent

    def change_color(self, clr):
        global color, colors_to_paint
        color = colors_to_paint[clr]

    def clear_rec(self, obj):
        global glob_viewer
        self.painter.canvas.clear()

        viewer = start_recognize()
        try:
            for val in dict_of_numbers.values():
                if val[0] in viewer.split(' '):
                    glob_viewer[0] = 'numbers'
                    glob_viewer[1] = list(dict_of_numbers.keys())[list(dict_of_numbers.values()).index(val)]
                elif val[1] in viewer.split(' '):
                    glob_viewer[0] = 'numbers'
                    glob_viewer[1] = list(dict_of_numbers.keys())[list(dict_of_numbers.values()).index(val)]

            for key in dict_of_colors.keys():
                if key in viewer:
                    glob_viewer[0] = 'colors'
                    glob_viewer[1] = dict_of_colors[key]

            for key in dict_of_shapes.keys():
                if key in viewer:
                    glob_viewer[0] = 'shapes'
                    glob_viewer[1] = dict_of_shapes[key]

            modal = ModalView(background_color="black", size_hint=(.4, .4))
            modal.add_widget(Image(source=f'{glob_viewer[0]}/{glob_viewer[1]}.png', height=400, width=400))
            modal.open()
        except:
            pass
        pass
        glob_viewer[0], glob_viewer[1] = 'numbers', 'zero'


if __name__ == '__main__':
    MyPaintApp().run()
