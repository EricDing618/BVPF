#系统库
import path
#获取配置文件信息
import json5 #用户可以自定义设置
#网络通信库
import socket as sock #多人联机需要TCP通信
#语法库
from typing import Union
#游戏库
import pygame as pg #使用pygame制作2D小游戏
from pygame.locals import *

class Config: #解析配置文件
    def __init__(self):
        with open(self.pj("./settings.jsonc"),"r",encoding="utf-8") as f:
            sets:dict[str,Union[str,int,list]] = json5.load(f)
            if not isinstance(sets,dict):
                raise TypeError(f"文件读取类型有误，得：{type(sets)}，应为：dict。")
            
        self.WINDOW=sets["window"]
        self.NPC=sets["Bobo"]
        self.PLAYER=sets["player"]

        self.WIDTH=self.WINDOW["size"][0]
        self.HEIGHT=self.WINDOW["size"][1]
        self.ICON_PATH=self.WINDOW['icon']
        self.NPC_COUNT=self.NPC['count']
        self.PLAYER_ICON=self.PLAYER['your_icon']

        del self.WINDOW,self.NPC,self.PLAYER,sets

    def pj(self,paths):
        '''join paths'''
        return path.join(path.workpath,paths)

class BaseGame(Config): #游戏基类，也是主界面
    def __init__(self): #初始化，把配置文件中的数据放入内存
        pg.init()

        self.win = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Escape From Bobo")
        pg.display.set_icon(pg.image.load(self.sets["window"]["icon"]))
    
    def play(self):
        self.win.blit(pg.image.load("./img/flag.png").convert(), (0,0))


class SinglePlayerGame(BaseGame): #单人游戏
    def __init__(self):
        super().__init__()

class MultiPlayerGame(BaseGame): #多人联机
    def __init__(self):
        super().__init__()

if __name__=="__main__":
    g = BaseGame()
