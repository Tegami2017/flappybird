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
import game_controller
import random
#vars
from game_controller import *

class rankScene(cocos.layer.Layer):
    def __init__(self, level):
        super(rankScene, self).__init__()
        bg = createAtlasSprite("hell_bg")
        bg.position = common.visibleSize["width"]/2, common.visibleSize["height"]/2
        self.add(bg)
        rankmenu = rankSceneMenu(level)
        self.add(rankmenu)

        self.records = [[], [], [], [], []]     #使用一个List创建二维label
        from game_controller import createLabel
        t_distance = 58     #每行label的间距
        r_position = [172, 270, 325]
        for i in range(len(self.records)):
            for j in range(3):
                label = createLabel("", r_position[j], 366 - t_distance * i)
                self.records[i].append(label)
                self.add(label, z=100)
        from network import request_hero_record
        request_hero_record(level)      #进入界面立即加载数据


class rankSceneMenu(Menu):
    def __init__(self, level):
        super(rankSceneMenu, self).__init__()
        self.menu_valign = CENTER
        self.menu_halign = CENTER
        self.level = level

        item1 = ImageMenuItem(common.load_image("button_return.png"), self.backmain)    #创建按钮，调整位置
        item1.position = (80, -264)
        item2 = ImageMenuItem(common.load_image("button_readme.png"), self.showscore)
        item2.position = (-80, -220)
        items = [
                (item1),
                (item2)
                ]
        self.create_menu(items)

    def backmain(self):     #返回键实现
        from game_controller import gameScene, gameLayer
        gameScene.remove("rank_data_layer")
        gameScene.add(gameLayer)

    def showscore(self):    #看自己的数据排行
        a = game_controller.gameScene.get("rank_data_layer")
        for j in range(5):
            a.records[j][0].element.text, a.records[j][1].element.text, a.records[j][2].element.text = '', '', ''
        from network import request_user_record
        request_user_record(self.level)
        return

class SingleRank(cocos.layer.Layer):  #创建个人战绩Layer
    def __init__(self):
        super(SingleRank, self).__init__()
        bg = createAtlasSprite("single_score")
        bg.position = common.visibleSize["width"] / 2, common.visibleSize["height"] / 2
        self.add(bg)
        from game_controller import ReturnButtom3
        rankmenu = ReturnButtom3()
        self.add(rankmenu)
        self.records = [[], [], [], [], []]
        from game_controller import createLabel
        t_distance = 58
        r_position = [200, 350]
        for i in range(len(self.records)):
            for j in range(2):
                label = createLabel("", r_position[j], 366 - t_distance * i)
                self.records[i].append(label)
                self.add(label, z=100)
        try:
            f = file('save.bin','rb')       #读取排名前五的战绩排序
            scorelist = []
            for eachline in f:
                s = base64.decodestring(eachline)
                ints = float (s)
                scorelist.append(ints)
            scorelist.sort(reverse=True)
            scorelist2 = map(str,scorelist)
            f.close()
            p_list = []
            t_list = []

            if len(scorelist2) == 1:
                recordlist = scorelist2[0].split('.')
                p_list.append(recordlist[0])
                t_list.append(recordlist[1])
            elif len(scorelist2) == 2:
                for i in range(2):
                    recordlist = scorelist2[i].split('.')
                    p_list.append(recordlist[0])
                    t_list.append(recordlist[1])
            elif len(scorelist2) == 3:
                for i in range(3):
                    recordlist = scorelist2[i].split('.')
                    p_list.append(recordlist[0])
                    t_list.append(recordlist[1])
            elif len(scorelist2) == 4:
                for i in range(4):
                    recordlist = scorelist2[i].split('.')
                    p_list.append(recordlist[0])
                    t_list.append(recordlist[1])
            elif len(scorelist2) >= 5:
                for i in range(5):
                    recordlist = scorelist2[i].split('.')
                    p_list.append(recordlist[0])
                    t_list.append(recordlist[1])

            j = 0
            for i in p_list:
                self.records[j][0].element.text = i
                j += 1
            j = 0
            for i in t_list:
                self.records[j][1].element.text = i
                j += 1

        except IOError:        #当存档不存在时，界面为空显示
            pass



