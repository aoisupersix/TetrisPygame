#coding:utf-8
import pygame
from pygame.locals import *
import sys


BLOCK_SIZE = 30
#フィールドサイズ
FIELD_WIDTH = 12
FIELD_HEIGHT = 22
#フィールドステータス
FIELD_NONE = -1
FIELD_WALL = -2

#画面サイズ
TOP_SPACE = 20
RIGHT_SPACE = 20
DOWN_SPACE = 10
LEFT_SPACE = 20
WINDOW_WIDTH = FIELD_WIDTH * BLOCK_SIZE + RIGHT_SPACE + LEFT_SPACE
WINDOW_HEIGHT = FIELD_HEIGHT * BLOCK_SIZE + TOP_SPACE + DOWN_SPACE

#Timer関連
framerate = 60  #60fps
fallFrame = 60

#フィールド
field = [[FIELD_NONE for i in range(FIELD_HEIGHT)] for j in range(FIELD_WIDTH) ]
for i in range(FIELD_WIDTH):
    field[i][0] = FIELD_WALL
    field[i][FIELD_HEIGHT - 1] = FIELD_WALL
for i in range(FIELD_HEIGHT):
    field[0][i] = FIELD_WALL
    field[FIELD_WIDTH - 1][i] = FIELD_WALL

#座標を管理するクラス
class Pos:
    def __init__(self,dx,dy):
        self.x = dx
        self.y = dy

#テトリミノ
MINO_I = 0
MINO_T = 1
MINO_J = 2
MINO_L = 3
MINO_S = 4
MINO_Z = 5
MINO_O = 6

class Mino:
    def __init__(self,r,p1,p2,p3,c):
        self.rotate = r
        self.pos = [p1,p2,p3]
        self.color = c

tetrimino = [Mino(2,Pos(0,-1),Pos(0,1),Pos(0,2),[0,255,255]),   #I
             Mino(4,Pos(0,-1),Pos(-1,0),Pos(1,0),[128,0,128]),   #T
             Mino(4,Pos(-1,0),Pos(1,0),Pos(1,1),[0,0,255]),   #J
             Mino(4,Pos(-1,1),Pos(-1,0),Pos(1,0),[0,0,128]),   #L
             Mino(2,Pos(-1,0),Pos(0,-1),Pos(1,-1),[0,255,0]),   #S
             Mino(2,Pos(1,0),Pos(0,-1),Pos(-1,-1),[255,0,0]),   #Z
             Mino(0,Pos(0,-1),Pos(1,-1),Pos(1,0),[255,255,0]),   #O
            ]

#現在のテトリミノ
class MinoStatus:
    def __init__(self, t, r, p):
        self.type = t
        self.rotate = r
        self.pos = p
        self.updatePos(self.pos,self.rotate)

    def updatePos(self, p, r):
        if p.x != self.pos.x or p.y != self.pos.y or r != self.rotate:
            #前回地点を削除
            field[self.pos.x][self.pos.y] = FIELD_NONE
            for i in range(3):
                ro = rotate % tetrimino[self.type].rotate
                dx = tetrimino[self.type].pos[i].x
                dy = tetrimino[self.type].pos[i].y
                for j in range(1, ro+1):
                    tmp = -dy
                    dy = dx
                    dx = tmp
                field[dx + self.pos.x][dy + self.pos.y] = FIELD_NONE

        #フィールド更新
        field[p.x][p.y] = self.type
        for i in range(3):
            ro = r % tetrimino[self.type].rotate
            dx = tetrimino[self.type].pos[i].x
            dy = tetrimino[self.type].pos[i].y
            for j in range(1, ro+1):
                tmp = -dy
                dy = dx
                dx = tmp
            field[dx + p.x][dy + p.y] = self.type
def main():
    #初期設定
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("PyGameTest")
    frame = 0
    currentMino = MinoStatus(MINO_J, 2, Pos(6,2))
    while(1):
        screen.fill((0,0,0))    #画面塗りつぶし
        __draw(screen)
        pygame.display.update()
        #イベント処理
        for event in pygame.event.get():
            #終了
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(framerate)
        if frame >= fallFrame:
            #落ちる
            print("fall")
            frame = 0
        frame += 1
def __draw(sc):
    #ブロック描画
    for x in range(FIELD_WIDTH):
        for y in range(FIELD_HEIGHT):
            dx = LEFT_SPACE + BLOCK_SIZE * x
            dy = TOP_SPACE + BLOCK_SIZE * y
            if field[x][y] == FIELD_NONE:
                #何もない
                pygame.draw.rect(sc,(230,230,230),Rect(dx,dy,BLOCK_SIZE,BLOCK_SIZE))
                pygame.draw.rect(sc,(150,150,150),Rect(dx,dy,BLOCK_SIZE,BLOCK_SIZE), 1)
            elif field[x][y] == FIELD_WALL:
                #壁
                pygame.draw.rect(sc,(60,60,60),Rect(dx,dy,BLOCK_SIZE,BLOCK_SIZE))
                pygame.draw.rect(sc,(10,10,10),Rect(dx,dy,BLOCK_SIZE,BLOCK_SIZE), 1)
            else:
                t = field[x][y]
                #テトリミノ
                pygame.draw.rect(sc,(tetrimino[t].color[0],tetrimino[t].color[1],tetrimino[t].color[2]),Rect(dx,dy,BLOCK_SIZE,BLOCK_SIZE))
                pygame.draw.rect(sc,(10,10,10),Rect(dx,dy,BLOCK_SIZE,BLOCK_SIZE), 1)
if __name__ == "__main__":
    main()
