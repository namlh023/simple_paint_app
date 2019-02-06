from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex
from kivy.graphics import Line, Color
from kivy.core.text import LabelBase
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior


class RadioButton(ToggleButton):
    def _do_press(self):
        if self.state == 'normal':
            ToggleButtonBehavior._do_press(self)


class CanvasFloat(FloatLayout):
    undo_list = []
    current_color = get_color_from_hex('#2980b9')

    def on_touch_down(self, touch):
        for child in self.children[:]:
            if child.dispatch('on_touch_down', touch):
                return True

            if child.collide_point(touch.x, touch.y):
                return True

        with self.canvas:
            Color(*self.line_color)
            touch.ud['current_line'] = Line(points=(touch.x, touch.y), width=self.line_width)

    def on_touch_move(self, touch):
        for child in self.children[:]:
            if child.collide_point(touch.x, touch.y):
                return True

        with self.canvas:
            Color(*self.line_color)
            if 'current_line' in touch.ud:
                touch.ud['current_line'].points += (touch.x, touch.y)

    def on_touch_up(self, touch):
        if 'current_line' in touch.ud:
            self.undo_list.append(touch.ud['current_line'])

    def set_line_color(self, color):
        self.line_color = color

    def clear_canvas(self):
        saved = self.children[:]
        self.clear_widgets()
        self.canvas.clear()
        for child in saved:
            self.add_widget(child)

    def undo_canvas(self):
        try:
            self.canvas.remove(self.undo_list.pop())
        except IndexError:
            pass

    def erase_canvas(self):
        white_color = get_color_from_hex('#ffffff')

        return self.set_line_color(white_color)

    def set_line_width(self, line_width):
        self.line_width = line_width


class PaintApp(App):
    _default_line_color = get_color_from_hex('#2980b9')
    _normal_line_width = 2

    def build(self):
        self.canvas_float = CanvasFloat()
        self.canvas_float.set_line_color(self._default_line_color)
        self.canvas_float.set_line_width(self._normal_line_width)

        return self.canvas_float


if __name__ == '__main__':
    LabelBase.register(name='Modern Pictograms',
                       fn_regular='./fonts/modernpics.ttf')

    LabelBase.register(name='Heydings',
                       fn_regular='./fonts/heydings_controls.ttf')

    from kivy.core.window import Window

    Window.clearcolor = get_color_from_hex('#ffffff')

    PaintApp().run()
