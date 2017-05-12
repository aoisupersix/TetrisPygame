#coding:utf-8
import pygame
from pygame.locals import *
import sys
import random
import copy

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
    field[i][FIELD_HEIGHT - 1] = FIELD_WALL
for i in range(FIELD_HEIGHT):
    field[0][i] = FIELD_WALL
    field[FIELD_WIDTH - 1][i] = FIELD_WALL

#次に出すテトリミノ
nextMino = []

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
             Mino(1,Pos(0,-1),Pos(1,-1),Pos(1,0),[255,255,0]),   #O
            ]

#現在のテトリミノ
class MinoStatus:

    def __init__(self, t, r, p):
        self.type = t
        self.rotate = r
        self.pos = p
        print("---Create Status---")
        print("type=" + str(self.type))
        print("rotate=" + str(self.rotate))
        print("pos=" + str(self.pos.x) + ", " + str(self.pos.y))
        self.updatePos(self.pos,self.rotate)


    #ブロックのポジションを返す。
    def getPos(self, p, r):
        pos = []
        pos.append(p)
        for i in range(3):
            ro = r % tetrimino[self.type].rotate
            dx = tetrimino[self.type].pos[i].x
            dy = tetrimino[self.type].pos[i].y
            for j in range(1, ro+1):
                tmp = -dy
                dy = dx
                dx = tmp
            pos.append(Pos(dx + p.x, dy + p.y))
        for po in pos:
            print("getPos:Pos=" + str(po.x) + ", " + str(po.y))
        print("returnPos")
        return pos

    def canPut(self, gp):
        bpos = self.getPos(self.pos, self.rotate)
        for i in gp:
            for j in bpos:
                if j.x == i.x and j.y == i.y:
                    #自分がいるので除外
                    break
            else:
                if i.x < 0 or i.x >= FIELD_WIDTH or i.y < 0 or i.y >= FIELD_HEIGHT or field[i.x][i.y] != FIELD_NONE:
                    #置けない
                    print("DONT PUT")
                    break
        else:
            return True
        return False

    def updatePos(self, p, r):
        #置けるかどうかのチェック
        bpos = self.getPos(self.pos, self.rotate)
        apos = self.getPos(p, r)

        if self.canPut(apos):
            if p.x != self.pos.x or p.y != self.pos.y or r != self.rotate:
                #前回地点を削除
                for i in bpos:
                    field[i.x][i.y] = FIELD_NONE

            #フィールド更新
            for i in apos:
                field[i.x][i.y] = self.type
            field[p.x][p.y] = self.type
            self.rotate = r
            self.pos = p

#新しいテトリミノを出す
def spawn():
    if len(nextMino) == 0:
        #セット
        for i in range(len(tetrimino)):
            nextMino.append(i)
        random.shuffle(nextMino)
    print(nextMino[0])
    return MinoStatus(nextMino.pop(), 0, Pos(6,2))

#消す
def deleteLine():
    for y in range(FIELD_HEIGHT-1):
        for x in range(1,FIELD_WIDTH-1):
            if field[x][y] == FIELD_NONE:
                break
        else:
            #この行が全て埋まってる
            for j in reversed(range(y)):
                print("del:" + str(j))
                for i in range(FIELD_WIDTH):
                    field[i][j + 1] = field[i][j]
            y += 1
def main():
    #初期設定
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("PyTetris")
    frame = 0   #テトリミノの落下管理
    keyFrame = 0    #キー入力の間隔管理
    spinFrame = 0   #スピンの間隔管理
    currentMino = spawn()
    while(1):
        clock.tick(framerate)
        screen.fill((0,0,0))    #画面塗りつぶし
        __draw(screen)
        pygame.display.update()

        #下端に達したかどうか
        gePos = currentMino.getPos(Pos(currentMino.pos.x, currentMino.pos.y + 1), currentMino.rotate)
        if not currentMino.canPut(gePos):
            deleteLine()
            currentMino = spawn()
            continue

        #イベント処理
        for event in pygame.event.get():
            #終了
            if event.type == QUIT:
                print("END")
                pygame.quit()
                sys.exit()

        if frame >= fallFrame:
            #落ちる
            currentMino.updatePos(Pos(currentMino.pos.x, currentMino.pos.y + 1), currentMino.rotate)
            frame = 0

        #キー入力
        pressed = pygame.key.get_pressed()
        if keyFrame >= framerate / 10:
            keyFrame = 0
            #左移動
            if pressed[K_LEFT]:
                currentMino.updatePos(Pos(currentMino.pos.x - 1,currentMino.pos.y),currentMino.rotate)
            #右移動
            if pressed[K_RIGHT]:
                currentMino.updatePos(Pos(currentMino.pos.x + 1,currentMino.pos.y),currentMino.rotate)
            #スピン
            if pressed[K_SPACE] and spinFrame >= framerate / 7:
                currentMino.updatePos(currentMino.pos, currentMino.rotate + 1)
                spinFrame = 0
            #ソフトドロップ
            if pressed[K_DOWN]:
                currentMino.updatePos(Pos(currentMino.pos.x,currentMino.pos.y+1),currentMino.rotate)

        frame += 1
        keyFrame += 1
        spinFrame += 1
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
