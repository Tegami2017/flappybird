# coding:utf-8
import cocos
from cocos.director import director
import pyglet


class EventLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(EventLayer, self).__init__()

        self.gravitay_text = cocos.text.Label('gravity: ', font_size=10, x=50, y=100)
        self.upSpeed_text = cocos.text.Label('upSpeed: ', font_size=10, x=50, y=80)
        self.spriteBird = None
        self.debug = False
        self.TouchHandler = None

    def open_debug(self):
        self.debug = True

    def show_gravity(self):
        self.add(self.gravitay_text, z=100)
        self.add(self.upSpeed_text, z=100)

    def set_spriteBird(self, spriteBird):
        self.spriteBird = spriteBird

    def set_TouchHandler(self, TouchHandler):
        self.TouchHandler = TouchHandler

    def update_text(self):
        self.gravitay_text.element.text = 'gravity:  ' + str(self.spriteBird.gravity)
        self.upSpeed_text.element.text = 'upSpeed:  ' + str(self.TouchHandler.upSpeed)

    def on_key_press(self, key, modifiers):
        #按下按键自动触发本方法
        if self.debug and self.spriteBird is not None:
            press = pyglet.window.key.symbol_string(key)
            if press == 'UP':
                self.spriteBird.gravity = self.spriteBird.gravity * float(11) / 10
                self.TouchHandler.upSpeed = self.TouchHandler.upSpeed * float(11) / 10
                self.update_text()
                print 'gravity、upSpeed increase'
            elif press == 'DOWN':
                self.spriteBird.gravity = self.spriteBird.gravity * float(9) / 10
                self.TouchHandler.upSpeed = self.TouchHandler.upSpeed * float(9) / 10
                self.update_text()
                print 'gravity、upSpeed reduce'

    def on_key_release(self, key, modifiers):
        #松开按键自动触发本方法
        pass


# class MouseDisplay(cocos.layer.Layer):
#
#     is_event_handler = True
#
#     def __init__(self):
#         super(MouseDisplay, self).__init__()
#
#         self.text = cocos.text.Label('Mouse @', font_size=18,
#                                      x=100, y=240)
#         self.add(self.text)
#
#     def on_mouse_motion(self, x, y, dx, dy):
#         #dx,dy为向量,表示鼠标移动方向
#         self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, dx, dy)
#
#     def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
#         self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y,buttons, modifiers)
#
#     def on_mouse_press(self, x, y, buttons, modifiers):
#         #按下鼠标按键不仅更新鼠标位置,还改变标签的位置.这里使用director.get_virtual_coordinates(),用于保证即使窗口缩放过也能正确更新位置,如果直接用x,y会位置错乱,原因不明
#         self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y,buttons, modifiers)
#         self.text.element.x, self.text.element.y = director.get_virtual_coordinates(x, y)

