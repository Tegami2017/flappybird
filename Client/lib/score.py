# -*- coding: utf-8 -*-
from cocos.actions import *
from atlas import *
import common

spriteScores = {}
scoreLayer = None
scoreStr = 0


#开始游戏后显示当前得分
def createScoreLayer(gameLayer):
    global scoreLayer
    scoreLayer = gameLayer
    setSpriteScores(0)

def setSpriteScores(score):
    global scoreLayer, scoreStr
    for k in spriteScores:
        try:
            scoreLayer.remove(spriteScores[k])
            spriteScores[k] = None
        except:
            pass

    scoreStr = str(score)
    i = 0
    for d in scoreStr:
        global s
        s = createAtlasSprite("number_score_0"+d)
        s.position = common.visibleSize["width"]/2 + 18 * i, common.visibleSize["height"]*4/5
        scoreLayer.add(s, z=50)
        spriteScores[i] = s
        i = i + 1
