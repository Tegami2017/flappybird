# -*- coding: utf-8 -*-
import cocos
from cocos.scene import *
from cocos.actions import *
from cocos.layer import *  
from cocos.text  import *
from cocos.menu import *
import random
from atlas import *
from land import *
from bird import *
from score import *
from pipe import *
from collision import *
from network import *
import common
import random
import base64
from rankPanel import *
from Layer_with_event import EventLayer
import time
from UiHandlerTk import UiHandler
import network
import Tkinter


#vars
gameLayer = None
gameScene = None
spriteBird = None
spriteBird0 = None  # edi by 张宏聪
land_1 = None
land_2 = None
startLayer = None
pipes = None
score = 0
listener = None
account = None
password = None
ipTextField = None
errorLabel = None
isGamseStart = False
login_name = None


def initGameLayer():
    global spriteBird, spriteBird0, gameLayer, land_1, land_2, title, login_name   # edi by 张宏聪
    # gameLayer: 游戏场景所在的layer
    gameLayer = EventLayer()
    # add background
    bg_num = random.randint(0,1)
    if bg_num == 0: #增加了背景随机切换的功能
        bg = createAtlasSprite("bg_day")
    else:
        bg = createAtlasSprite("bg_night")
    bg.position = (common.visibleSize["width"]/2, common.visibleSize["height"]/2)
    gameLayer.add(bg, z=0)
    # add moving bird
    title = createAtlasSprite("title")
    title.position = (common.visibleSize["width"] / 2, common.visibleSize["height"] * 4 / 5)
    gameLayer.add(title, z=50) #增加标题title——张晋达
    # add moving land
    land_1, land_2 = createLand()
    gameLayer.add(land_1, z=20)
    gameLayer.add(land_2, z=20)

    login_label = createLabel("", 200, 500)
    gameLayer.add(login_label, z=20, name="login_label")

    if login_name is not None:
        login_label.element.text = u"欢迎，" + login_name

    # add gameLayer to gameScene
    gameScene.add(gameLayer)

def initRankList():
    global spriteBird, spriteBird0, gameLayer, land_1, land_2, title  # edi by 张宏聪
    # gameLayer: 游戏场景所在的layer
    gameLayer = Layer()
    # add background
    bg_num = random.randint(0, 1)
    if bg_num == 0:  # 增加了背景随机切换的功能
        bg = createAtlasSprite("bg_day")
    else:
        bg = createAtlasSprite("bg_night")
    bg.position = (common.visibleSize["width"] / 2, common.visibleSize["height"] / 2)
    gameLayer.add(bg, z=0)
    # add moving land
    land_1, land_2 = createLand()
    gameLayer.add(land_1, z=10)
    gameLayer.add(land_2, z=10)
    # add gameLayer to gameScene
    gameScene.add(gameLayer)




def game_start(_gameScene):
    global gameScene
    # 给gameScene赋值
    gameScene = _gameScene
    initGameLayer()
    login_button = LoginMenu()
    gameLayer.add(login_button, z=20, name="login_button")
    # start_botton = SingleGameStartMenu()
    # gameLayer.add(start_botton, z=20, name="start_button")
    connect(gameScene)


def createLabel(value, x, y):
    label=Label(value,  
        font_name='Times New Roman',  
        font_size=15, 
        color = (0,0,0,255), 
        width = common.visibleSize["width"] - 20,
        multiline = True,
        anchor_x='center',anchor_y='center')
    label.position = (x, y)
    return label


# single game start button的回调函数
def singleGameReady(game_level):
    if gameLayer.debug:
        gameLayer.show_gravity()
    removeContent()
    spriteBird = creatBird()
    spriteBird0 = creatBird0()  # 创建第二只小鸟的精灵；edi by 张宏聪

    gameLayer.set_spriteBird(spriteBird)

    gameLayer.add(spriteBird, z=20)
    gameLayer.add(spriteBird0, z=20)  # 创建第二只小鸟的画布；edi by 张宏聪
    ready = createAtlasSprite("text_ready")
    ready.position = (common.visibleSize["width"]/2, common.visibleSize["height"] * 3/4)

    tutorial = createAtlasSprite("tutorial")
    tutorial.position = (common.visibleSize["width"]/2, common.visibleSize["height"]/2)
    
    spriteBird.position = (common.visibleSize["width"]/3, spriteBird.position[1])

    def movespriteBird0(dt):  # 实现第二只小鸟与第一只小鸟位置同步； edi by 张宏聪
        spriteBird0.position = spriteBird.position

    movespriteBird0Func = movespriteBird0
    gameScene.schedule(movespriteBird0Func)
    #handling touch events

    class ReadyTouchHandler(cocos.layer.Layer):
        is_event_handler = True     #: enable director.window events
        global start
        def __init__(self, game_level):
            super( ReadyTouchHandler, self).__init__()
            self.game_level = game_level

        def on_mouse_press (self, x, y, buttons, modifiers):
            """This function is called when any mouse button is pressed

            (x, y) are the physical coordinates of the mouse
            'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
            'modifiers' is a bitwise or of pyglet.window.key modifier constants
               (values like 'SHIFT', 'OPTION', 'ALT')
            """
            self.singleGameStart(buttons, x, y)
    
        # ready layer的回调函数
        def singleGameStart(self, eventType, x, y,):
            global start
            isGamseStart = True
            start = time.time()
            spriteBird.gravity = gravity  # gravity is from bird.py
            # handling bird touch events
            addTouchHandler(gameScene, isGamseStart, spriteBird, spriteBird0)   # 在控制器中添加第二只鸟； edi by 张宏聪
            score = 0   #分数，飞过一个管子得到一分
            # add moving pipes
            pipes = createPipes(gameLayer, gameScene, spriteBird, score, self.game_level)
            # 小鸟AI初始化
            # initAI(gameLayer)
            # add score
            createScoreLayer(gameLayer)
            # add collision detect
            addCollision(gameScene, gameLayer, spriteBird, pipes, land_1, land_2)
            # remove startLayer
            gameScene.remove(readyLayer)

    readyLayer = ReadyTouchHandler(game_level)
    readyLayer.add(ready)
    readyLayer.add(tutorial)
    gameScene.add(readyLayer, z=10)

def back_to_login():
    global login_name
    if login_name is not None:
        login_name = None
        wrong_ui = Tkinter.Tk()
        wrong_ui.title('网络错误')
        l = Tkinter.Label(wrong_ui, text="与服务器连接已断开，请重启游戏再尝试，或进行离单人线模式")
        l.pack()
        wrong_ui.geometry('400x30')
        x = (wrong_ui.winfo_screenwidth() - wrong_ui.winfo_reqwidth()) / 2
        y = (wrong_ui.winfo_screenheight() - wrong_ui.winfo_reqheight()) / 2
        wrong_ui.geometry("+%d+%d" % (x, y))
        wrong_ui.resizable(False, False)
        wrong_ui.mainloop()
        gameScene.remove(gameLayer)
        initGameLayer()
        login_button = LoginMenu()
        gameLayer.add(login_button, z=20, name="login_button")
        return

def logout():
    global login_name
    login_name = None
    gameScene.remove(gameLayer)
    initGameLayer()
    login_button = LoginMenu()
    gameLayer.add(login_button, z=20, name="login_button")

def init_rankList(level):#定义init_rankList函数用于实例化rankScene，创建英雄榜界面(edit by Ice)
    a = rankScene(level)
    gameScene.remove(gameLayer)
    gameScene.add(a, z=0, name="rank_data_layer")

def single_rank():
    a = SingleRank()
    gameScene.remove(gameLayer)
    gameScene.add(a, z=0, name="singlerank_layer")

def backToMainMenu():
    restartButton = RestartMenu()
    gameLayer.add(restartButton, z=50)


def diff_Menu():
    diffButton = DifficultyMenu()
    gameLayer.add(diffButton, z=50)


def showNotice():
    connected = connect(gameScene) # connect is from network.py
    if not connected:
        content = "Cannot connect to server"
        showContent(content)
    else:
        request_notice() # request_notice is from network.py


def showContent(content):
    removeContent()
    notice = createLabel(content, common.visibleSize["width"]/2+5, common.visibleSize["height"] * 9/10)
    gameLayer.add(notice, z=70, name="content")


def removeContent():
    try:
        gameLayer.remove("content")
    except Exception, e:
        pass
    

class RestartMenu(Menu):
    global diff
    def __init__(self):  
        super(RestartMenu, self).__init__()
        self.menu_valign = BOTTOM
        self.menu_halign = CENTER
        items = [
                (ImageMenuItem(common.load_image("button_restart.png"), self.reGame)),
                (ImageMenuItem(common.load_image("button_main.png"), self.initMainMenu))
                ]  
        self.create_menu(items,selected_effect=zoom_in(),unselected_effect=zoom_out())
        from score import scoreStr
        s = int(scoreStr)
        if s < 10:
            scores = createAtlasSprite("score_panel")  #增加战绩展示及分级——张晋达
        elif s >=10 and s < 20:
            scores = createAtlasSprite("score_tong")
        elif s >= 20 and s < 30:
            scores = createAtlasSprite("score_silver")
        elif s >= 30 and s < 40:
            scores = createAtlasSprite("score_gold")
        elif s >= 40 :
            scores = createAtlasSprite("score_pat")
        scores.position = (common.visibleSize["width"] / 2, common.visibleSize["height"] * 6 / 11)
        gameLayer.add(scores,z=52)
        over = createAtlasSprite("text_game_over")  #增加game over字体——张晋达
        over.position = (common.visibleSize["width"] / 2, common.visibleSize["height"] * 5 / 7)
        gameLayer.add(over, z=60)
        superman = createAtlasSprite("hero")  # 增加hero图片——张晋达
        superman.position = (common.visibleSize["width"]*22 / 40, common.visibleSize["height"] * 8 / 10)
        gameLayer.add(superman, z=70)

        end = time.time()
        gameTime = str(int(end - start)) #计算游戏时间


        from score import scoreStr   # 增加战绩展示的数字——张晋达
        spritScores = {}
        for k in spritScores:
            gameLayer.remove(spriteScores[k])
            spriteScores[k] = None
        scoreSt = str(scoreStr)
        i = 0
        for d in scoreSt:
            s = createAtlasSprite("number_score_0" + d)
            s.position = common.visibleSize["width"]*16 /23 + 18 * i, common.visibleSize["height"] * 19 / 33
            gameLayer.add(s, z=80)
            spriteScores[i] = s
            i = i + 1

        savedata = '.'.join([scoreStr, gameTime])
        s = base64.encodestring(savedata)  #加密并保存数据——张晋达
        f = file('save.bin', 'ab')
        f.write(s)
        f.close()

        f = file('save.bin', 'rb')
        scorelist = []  #读取并解密数据——张晋达
        for eachline in f:
            bests = (base64.decodestring(eachline))
            s = bests.split('.')
            scorelist.append(int(s[0]))
        bestscore = max(scorelist)
        f.close()
        si = int(scoreStr)
        print si
        b = int(bestscore)
        print b
        if b == si: #当当前战绩等于最高战绩时显示新战绩——张晋达
            over = createAtlasSprite("new")
            over.position = (common.visibleSize["width"]* 17/ 29, common.visibleSize["height"] * 11 / 20)
            gameLayer.add(over, z=90)

        spritbest = {}
        for k in spritbest:
            gameLayer.remove(spritbest[k])
            spritbest[k] = None
        scorebst = str(bestscore)
        i = 0
        for d in scorebst:  #显示最高战绩——张晋达
            s = createAtlasSprite("number_score_0" + d)
            s.position = common.visibleSize["width"] * 16 / 23 + 18 * i, common.visibleSize["height"] * 14 / 28
            gameLayer.add(s, z=80)
            spritbest[i] = s
            i = i + 1

        if login_name is not None:
            network.request_commit_result(int(scoreStr), float(gameTime), diff)





    def initMainMenu(self):
        gameScene.remove(gameLayer)
        initGameLayer()
        start_botton = SingleGameStartMenu()
        gameLayer.add(start_botton, z=20, name="start_button")

    def reGame(self):   #重新开始相同难度的游戏——张晋达
        global diff
        gameScene.remove(gameLayer)
        initGameLayer()
        gameLayer.remove(title)
        isGamseStart = False
        singleGameReady(diff)


class LoginMenu(Menu):
    def __init__(self):
        super(LoginMenu, self).__init__()
        self.menu_valign = CENTER
        self.menu_halign = CENTER
        self.ui_handler = None

        items = [(ImageMenuItem(common.load_image("button_login2.png"), self.open_ui_handler)),
                 (ImageMenuItem(common.load_image("button_singlegame2.png"), self.start_single_game))
                 ]

        self.create_menu(items, selected_effect=zoom_in(), unselected_effect=zoom_out())

    def open_ui_handler(self):
        if self.ui_handler is not None:
            return
        if not network.connected:
            wrong_ui = Tkinter.Tk()
            wrong_ui.title('错误提示')
            l = Tkinter.Label(wrong_ui, text="未连接服务器，请重启游戏再尝试，或进行离单人线模式")
            l.pack()
            wrong_ui.geometry('350x30')
            x = (wrong_ui.winfo_screenwidth() - wrong_ui.winfo_reqwidth()) / 2
            y = (wrong_ui.winfo_screenheight() - wrong_ui.winfo_reqheight()) / 2
            wrong_ui.geometry("+%d+%d" % (x, y))
            wrong_ui.resizable(False, False)
            wrong_ui.mainloop()
            return
        if self.ui_handler is None:
            self.ui_handler = UiHandler()
            self.ui_handler.show_login_ui()
        self.ui_handler = None

    def start_single_game(self):
        if self.ui_handler is not None:
            return
        start_botton = SingleGameStartMenu()
        gameLayer.add(start_botton, z=20, name="start_button")
        gameLayer.remove("login_button")


class SingleGameStartMenu(Menu):
    def __init__(self):  
        super(SingleGameStartMenu, self).__init__()
        self.menu_valign = BOTTOM
        self.menu_halign = CENTER
        global login_name
        if login_name is not None:
            items = [(ImageMenuItem(common.load_image("button_start.png"), self.diffMenu_normal)),
                     (ImageMenuItem(common.load_image("button_debug.png"), self.diffMenu_debug)),
                     (ImageMenuItem(common.load_image("button_notice.png"), showNotice)),
                     (ImageMenuItem(common.load_image('button_rank.png'), self.rankMenu)),
                     (ImageMenuItem(common.load_image('button_exit.png'), self.xite)),
                     (ImageMenuItem(common.load_image('button_logout.png'), self.logout))
                     ]
        else:
            items = [(ImageMenuItem(common.load_image("button_start.png"), self.diffMenu_normal)),
                     (ImageMenuItem(common.load_image("button_debug.png"), self.diffMenu_debug)),
                     (ImageMenuItem(common.load_image('button_rate.png'), self.singrank)),
                     (ImageMenuItem(common.load_image('button_exit.png'), self.xite)),
                     (ImageMenuItem(common.load_image('button_return.png'), self.return_login))
                     ]

        self.create_menu(items, selected_effect=zoom_in(), unselected_effect=zoom_out())

    def diffMenu_normal(self):
        gameLayer.debug = False
        gameLayer.remove('start_button')
        gameLayer.remove(title)
        diff_botton = DifficultyMenu()
        gameLayer.add(diff_botton, z=20, name="diff_button")
        return_buttom = ReturnButtom()
        gameLayer.add(return_buttom, z=20, name='return_buttom')

    def diffMenu_debug(self):
        gameLayer.debug = True
        gameLayer.remove('start_button')
        gameLayer.remove(title)
        diff_botton = DifficultyMenu()
        gameLayer.add(diff_botton, z=20, name="diff_button")
        return_buttom = ReturnButtom()
        gameLayer.add(return_buttom, z=20, name='return_buttom')


    def rankMenu(self):
        gameLayer.remove('start_button')
        gameLayer.remove(title)
        rank_button = RankListMenu()
        gameLayer.add(rank_button, z=20, name="rank_button")
        return_button2 = ReturnButtom2()
        gameLayer.add(return_button2, z=20, name='return_button2')

    def singrank(self):
        single_rank()

    def xite(self):
        exit()

    def return_login(self):
        gameLayer.remove("start_button")
        login_button = LoginMenu()
        gameLayer.add(login_button, z=20, name="login_button")

    def logout(self):
        network.request_logout()




class RankListMenu(Menu):    #创建英雄榜的菜单按钮(edit by Ice)
    def __init__(self):
        super(RankListMenu, self).__init__()
        self.menu_valign = CENTER
        self.menu_halign = CENTER
        items = [
            (ImageMenuItem(common.load_image('button_easy_rank.png'), self.rankEasy)),
            (ImageMenuItem(common.load_image('button_normal_rank.png'), self.rankNormal)),
            (ImageMenuItem(common.load_image('button_hard_rank.png'), self.rankHard)),
            (ImageMenuItem(common.load_image('button_hell_rank.png'), self.rankHell))
        ]
        self.create_menu(items, selected_effect=zoom_in(), unselected_effect=zoom_out())

    def rankEasy(self):    #获取easy难度的数据库信息
        init_rankList(1)
        return
    def rankNormal(self):    # 获取normal难度的数据库信息
        init_rankList(2)
        return
    def rankHard(self):    # 获取hard难度的数据库信息
        init_rankList(3)
        return
    def rankHell(self):    # 获取hell难度的数据库信息
        init_rankList(4)
        return







class DifficultyMenu(Menu):  #难度选择界面
    global diff
    def __init__(self):
        super(DifficultyMenu, self).__init__()
        self.menu_valign = CENTER
        self.menu_halign = CENTER
        items = [
            (ImageMenuItem(common.load_image('button_easy.png'), self.gameStart_easy)),
            (ImageMenuItem(common.load_image('button_normal.png'), self.gameStart_normal)),
            (ImageMenuItem(common.load_image('button_hard.png'), self.gameStart_hard)),
            (ImageMenuItem(common.load_image('button_hell.png'), self.gameStart_hell))

        ]
        self.create_menu(items, selected_effect=zoom_in(), unselected_effect=zoom_out())

    def gameStart_easy(self):
        global diff
        gameLayer.remove('diff_button')
        gameLayer.remove('return_buttom')
        singleGameReady(1)
        diff = 1

    def gameStart_normal(self):
        global diff
        gameLayer.remove('diff_button')
        gameLayer.remove('return_buttom')
        singleGameReady(2)
        diff = 2

    def gameStart_hard(self):
        global diff
        gameLayer.remove('diff_button')
        gameLayer.remove('return_buttom')
        singleGameReady(3)
        diff = 3

    def gameStart_hell(self):
        global diff
        gameLayer.remove('diff_button')
        gameLayer.remove('return_buttom')
        singleGameReady(4)
        diff = 4

class ReturnButtom(Menu):  #返回按钮——张晋达
    def __init__(self):
        super(ReturnButtom, self).__init__()
        self.menu_valign = BOTTOM
        self.menu_halign = RIGHT
        items = [(ImageMenuItem(common.load_image('button_return.png'),self.retmain))]
        self.create_menu(items, selected_effect=zoom_in(), unselected_effect=zoom_out())

    def retmain(self):
        gameScene.remove(gameLayer)
        initGameLayer()
        start_botton = SingleGameStartMenu()
        gameLayer.add(start_botton, z=20, name="start_button")

class ReturnButtom2(Menu):
    def __init__(self):
        super(ReturnButtom2, self).__init__()
        self.menu_valign = BOTTOM
        self.menu_halign = RIGHT
        items = [(ImageMenuItem(common.load_image('button_return.png'),self.retmain))]
        self.create_menu(items, selected_effect=zoom_in(), unselected_effect=zoom_out())

    def retmain(self):
        gameScene.remove(gameLayer)
        initGameLayer()
        start_botton = SingleGameStartMenu()
        gameLayer.add(start_botton, z=20, name="start_button")

class ReturnButtom3(Menu):
    def __init__(self):
        super(ReturnButtom3, self).__init__()
        self.menu_valign = BOTTOM
        self.menu_halign = RIGHT
        items = [(ImageMenuItem(common.load_image('button_return.png'),self.retmain))]
        self.create_menu(items, selected_effect=zoom_in(), unselected_effect=zoom_out())

    def retmain(self):
        gameScene.remove("singlerank_layer")
        initGameLayer()
        start_button = SingleGameStartMenu()
        gameLayer.add(start_button, z=20, name="start_button")