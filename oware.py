import pygame
from pygame.locals import *
import random
import sys
import copy
import time

screen = pygame.display.set_mode((600, 400))

nextScore=0.8
nextP=[1,2,3,4,5,6,7,8,9,10,11,0]
comLevel=4#遊べるのは6ぐらいまで

def nextPos(pos):
    pos+=1
    if pos==12:pos=0
    return pos

def dropSeedScore(h,startPos):
    seed=h[startPos]
    if seed==0:return h,-1

    pos=startPos
    dh=copy.deepcopy(h)

    dh[startPos]=0
    for i in range(seed):
        pos=nextP[pos]
        if pos==startPos:
            pos=nextP[pos]
        dh[pos]+=1

    score=0
    for j in range(pos,-1,-1):
        if startPos<6 and j<6:break
        if startPos>5 and j>5:break
        if 2<=dh[j]<=3:
            score+=dh[j]
            dh[j]=0
        else:break
    #相手を0にしてはいけない
    if startPos<=5 and sum(dh[6:])==0:return h,-1
    if startPos>=6 and sum(dh[:6])==0:return h,-1

    return dh,score

def enemyTurn(dh,lvl):
    global nextScore
    eh=copy.deepcopy(dh)
    b=-1000
    bi=0
    for i in range(6,12):
        edh,score=dropSeedScore(eh,i)
        if score==-1:continue
        if lvl>0:score-=myTurn(edh,lvl-1)*nextScore
        if b<score:
            b=score
            bi=i
    return b

def myTurn(h,lvl):
    global nextScore
    mh=copy.deepcopy(h)
    b=-1000
    bi=0
    for i in range(6):
        mdh,score=dropSeedScore(mh,i)
        if score==-1:continue
        if lvl>0:score-=enemyTurn(mdh,lvl-1)*nextScore
        if b<score:
            b=score
            bi=i
    return b

def think(h,comLevel):
    startTime=time.time()
    b=-1000
    bestSeed=0
    bestDh=[]
    for i in range(6):
        dh,score=dropSeedScore(h,i)
        if score==-1:continue
        score-=enemyTurn(dh,comLevel)*nextScore

        if b<score:
            b=score
            bestSeed=sum(h)-sum(dh)
            bestDh=copy.deepcopy(dh)
    #print(time.time()-startTime,file=sys.stderr)
    return bestDh,bestSeed

def gamemain(comLevel):
    #board data
    # 5  4  3  2  1  0
    # 6  7  8  9 10 11
    h=[4,4,4,4,4,4,4,4,4,4,4,4]
    score=[0,0]
    turn=0#先手:0　後手:1 にする
    while 1:
        screen.fill((0,0,0))
        write(h,score)
        pygame.display.update()
        pygame.time.wait(500)
        if turn==1:
            h,sco=think(h,comLevel)
            score[1]+=sco
            turn=0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONUP and event.button == 1 and turn==0:
                x, y = event.pos
                px=int(x/100)
                if 0<=px<=5 and 200<y<300:
                    rh,sco=dropSeedScore(h,6+px)
                    if sco==-1:break
                    score[0]+=sco
                    if rh!=h:
                        h=rh
                        turn=1
        if score[0]>24 or score[1]>24 or (score[0]==24 and score[1]==24):turn=-1

def write(h,score):
    font = pygame.font.Font(None, 80)
    for p,hp in enumerate([5,4,3,2,1,0,6,7,8,9,10,11]):
        text = font.render(str(h[hp]), True, randcolor())
        screen.blit(text, [p%6*100+30, int(p/6)*100+100+30])

    font = pygame.font.Font(None, 30)
    text = font.render("yourScore="+str(score[0]), True, randcolor())
    screen.blit(text, [10,10])
    text = font.render("com Score="+str(score[1]), True, randcolor())
    screen.blit(text, [10,40])
    font = pygame.font.Font(None, 50)
    if score[0]>24:
        text = font.render("You Win", True, randcolor())
        screen.blit(text, [10,320])
    if score[1]>24:
        text = font.render("Com Win", True, randcolor())
        screen.blit(text, [10,320])
    if score[0]==24 and score[1]==24:
        text = font.render("Draw!!", True, randcolor())
        screen.blit(text, [10,320])

def randcolor():
    return (random.randint(128,255),random.randint(128,255),random.randint(128,255))

pygame.init()
gamemain(comLevel)
pygame.quit()
