#系统库
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"]="1" #禁用Pygame的输出
#获取配置文件信息
import json5 #用户可以自定义设置
#网络通信库
import socket as sock #多人联机需要TCP通信
#游戏库
import pygame as pg #使用pygame制作2D小游戏
from pygame.locals import *

class BaseGame: #游戏基类
    def __init__(self):
        pg.init()
        if "EscapeFromBobo" not in ''.join(os.getcwd().split('\\')).split('/'):
            self.workpath=os.path.join(os.getcwd(),"EscapeFromBobo")
        else:
            self.workpath=os.getcwd()

        self.pj=lambda paths,path=self.workpath:os.path.join(path,paths)

        with open(self.pj("./settings.jsonc"),"r",encoding="utf-8") as f:
            self.sets = json5.load(f)
            if not isinstance(self.sets,dict):
                raise TypeError(f"文件读取类型有误，得：{type(self.sets)}，应为：dict。")

        self.win = pg.display.set_mode((self.sets["window"]["size"][0], self.sets["window"]["size"][1]))
        pg.display.set_caption("Escape From Bobo")
        pg.display.set_icon(pg.image.load(self.sets["window"]["icon"]))
        self.win.blit(pg.image.load("./img/flag.png").convert(), (0,0))


class SinglePlayerGame(BaseGame): #单人游戏
    def __init__(self):
        super().__init__()

class MultiPlayerGame(BaseGame): #多人联机
    def __init__(self):
        super().__init__()

if __name__=="__main__":
    g = BaseGame()
