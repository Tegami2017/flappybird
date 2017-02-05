# -*- coding: utf-8 -*-
import cocos
from cocos.actions import *
from cocos.cocosnode import *
from cocos.collision_model import *
from cocos.director import *
import random
from atlas import *
from bird import *
from score import *
from game_controller import *
import common

#constants
gravity = -800   #重力大小
upSpeed = 250    #点击后上升的高度


#vars
AIFunc = None
inputListener = None
spriteBirdName = None
isAIOn = True
birdNum = str(random.randint(0, 2))     # 随机选取三种颜色小鸟的

#create the moving bird
def creatBird():        # 创建第一只小鸟的animate
    global birdNum
    spriteBird = CollidableAnimatingSprite("bird_" + birdNum, common.visibleSize["width"]/2, common.visibleSize["height"]/2, atlas["bird0_0"]["width"]/2 - 9)
    return spriteBird
def creatBird0():       # 创建第二只小鸟的animate
    global birdNum
    spriteBird0 = CollidableAnimatingSprite0("bird"+birdNum+"_", common.visibleSize["width"] / 2, common.visibleSize["height"] / 2, atlas["bird0_0"]["width"] / 2 - 9)
    spriteBird0.do(Hide())  # 开始的时候先隐藏这只扇动翅膀的小鸟

    return spriteBird0

#handling touch events
class birdTouchHandler(cocos.layer.Layer):
    is_event_handler = True     #: enable director.window events
    def __init__(self, spriteBird, spriteBird0):
        super( birdTouchHandler, self ).__init__()
        self.spriteBird = spriteBird
        self.spriteBird0 = spriteBird0
        self.spriteBird.gravity = gravity
        self.upSpeed = upSpeed

    def on_mouse_press(self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed

        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
           (values like 'SHIFT', 'OPTION', 'ALT')
        """
        #点击屏幕时，如果小鸟没有到达游戏顶部，给它一个上升速度
        if self.spriteBird.position[1] < common.visibleSize["height"]-20:
            self.spriteBird.velocity = (0, self.upSpeed)

            # 点击屏幕时，如果小鸟没有到达游戏顶部，会从第一只不会扇动翅膀的小鸟切换到第二只一直扇动翅膀的小鸟
            self.spriteBird.do(Hide())  # 第一只小鸟隐藏
            self.spriteBird0.do(Show()) # 第二只小鸟显示
            self.spriteBird0.do(Delay(0.3) + Hide())    # 第二只小鸟出现0.3s后隐藏
            self.spriteBird.do(Delay(0.3) + Show())     # 第一只小鸟隐藏0.3s后显示

HANDLER_NAME = "birdTouchHandler"


def addTouchHandler(gameScene, isGamseStart, spriteBird, spriteBird0):
    if isGamseStart:
        handler = birdTouchHandler(spriteBird, spriteBird0)
        gameScene.add(handler, z=50, name=HANDLER_NAME)
        from game_controller import gameLayer
        if gameLayer.debug:
            gameLayer.set_TouchHandler(handler)


#remove touch events
def removeBirdTouchHandler(gameScene):
    try:
        gameScene.remove(HANDLER_NAME)
    except:
        pass

#get spriteBird
def getSpriteBird():
    return spriteBird
