import pygame as pg #使用pygame制作2D小游戏
import json5 #用户可以自定义设置

import socket as sock #多人联机需要TCP通信

class BaseGame: #游戏基类
    def __init__(self):
        pg.init()
        with open("./settings.jsonc","r",encoding="utf-8") as f:
            self.sets = json5.load(f)
            if not isinstance(self.sets,dict):
                raise TypeError(f"文件读取类型有误，得：{type(self.sets)}，应为：dict。")

        win = pg.display.set_mode((self.sets["window"]["size"][0], self.sets["window"]["size"][1]))
        pg.display.set_caption("Escape From Bobo")
        pg.display.set_icon(pg.image.load(self.sets["window"]["icon"]))

class SinglePlayerGame(BaseGame): #单人游戏
    def __init__(self):
        super().__init__()

class MultiPlayerGame(BaseGame): #多人联机
    def __init__(self):
        super().__init__()
