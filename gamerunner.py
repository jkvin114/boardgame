#-*- coding: ms949 -*-
import tkinter.messagebox as mb
from tkinter import *
import random
from board import wn

from player import *
from Bird import Bird
from Yangi import Yangi
from Gorae import Gorae
from Creed import Creed
from Silver import Silver
from Timo import Timo
from Jean import Jean
from Jellice import Jellice
from Movingshin import Movingshin
from Blkx import Blkx
from DrMichin import DrMichin
import time
import window
from window import storewin
from window import dicewin
from window import choosedice
from board import player
from board import *
#win=window()
storewin.withdraw()
casino.withdraw()
subway.withdraw()
judge.withdraw()
dicewin.withdraw()
turn=0

reportfmt = '{0:<10} ({1:<2}): {2:<6}|{3:<6}|{4:<6}|{5:<5}|{6:<5}|{7:<5}|{8:<7}|{9:<13}'    
PLAYERNUMBER = int(input("플레이어 수 입력:"))  
COMPUTERNUMBER=0
names = ['1P','2P','#3','#4']
cnames=['봇1','봇2','봇3','봇4']
PLAYERS = []



print("1.버드\n2. 양\n3.고래\n4.크리드 \n5.실버\n6.티모\n7.진 \n8.젤리스 \n9.무빙신\n10.블크스\n11. 미친박사")

for i in range(0, PLAYERNUMBER):
    n = int(input('%d 턴 챔피언 선택:'% (i+1)))
    #n=1
    if n==1:
        PLAYERS.append(Bird(n, names[i], i,False))
    elif n==2:
        PLAYERS.append(Yangi(n, names[i], i,False))
    elif n==3:
        PLAYERS.append(Gorae(n, names[i], i,False))
    elif n==4:
        PLAYERS.append(Creed(n, names[i], i,False))
    elif n==5:
        PLAYERS.append(Silver(n, names[i], i,False))
    elif n==6:
        PLAYERS.append(Timo(n, names[i], i,False))
    elif n==7:
        PLAYERS.append(Jean(n, names[i], i,False))
    elif n==8:
        PLAYERS.append(Jellice(n, names[i], i,False))
    elif n==9:
        PLAYERS.append(Movingshin(n, names[i], i,False))
    elif n==10:
        PLAYERS.append(Blkx(n, names[i], i,False))
    elif n==11:
        PLAYERS.append(DrMichin(n, names[i], i,False))
for i in range(0, COMPUTERNUMBER):
    n = int(input('computer:1,2,3,4,5,11'))
    if n==1:
        PLAYERS.append(Bird(n, cnames[PLAYERNUMBER+i], PLAYERNUMBER+i,True))
    elif n==2:
        PLAYERS.append(Yangi(n, cnames[PLAYERNUMBER+i], PLAYERNUMBER+i,True))
    elif n==3:
        PLAYERS.append(Gorae(n, cnames[PLAYERNUMBER+i], PLAYERNUMBER+i,True))
    elif n==4:
        PLAYERS.append(Creed(n, cnames[PLAYERNUMBER+i], PLAYERNUMBER+i,True))
    elif n==5:
        PLAYERS.append(Silver(n, cnames[PLAYERNUMBER+i], PLAYERNUMBER+i,True))
    elif n==11:
        PLAYERS.append(DrMichin(n, cnames[PLAYERNUMBER+i], PLAYERNUMBER+i,True))
    
for i in range(0, PLAYERNUMBER+COMPUTERNUMBER):
    print('check', (i + 1, 'turn player:', PLAYERS[i].name,'(',PLAYERS[i].champ,')'))
    PLAYERS[i].character.show()
wn.update()
#   1. dice
# 2.projectile
#  3.creed w
#   4.cooltime,effect cooldown 
#   5.obstacle
#   6.lastmoneycooldown 
#   7.durcooldown
#    8.useskill
#    9.etc cooldown

keepgoing = True

while(keepgoing):  # oneturnloop
    turn+=1
    
    wn.update()
    obs=-1
    for p in PLAYERS:  # oneplayerloop
        if turn%2==0 and p.turn==PLAYERNUMBER%(PLAYERNUMBER+COMPUTERNUMBER): window.alarmReset()
        for pl in PLAYERS:
            pl.character.changecolor(p.turn)
        window.buttonupdate(p.cooltime)
        
        p.playsound()
        
        
        if p.effects[2] == 0:
            
            if p.isai==False: dice = choosedice(p.name)
            else: dice=random.randint(1,6)
            
            
            obs=p.move(dice,PLAYERS)

        else:
            window.passturn(p.name)
            obs=p.currobs
            #mb.showerror(None, "속박 상태입니다!")
            
            
            
        wn.update()
        p.Invulnerable=False
        skillfrom = p.turn
        notthisturn = [0, 0,0]
        c = 0
        for i in range(0, PLAYERNUMBER):
            if PLAYERS[i].turn != p.turn: 
                notthisturn[c] = PLAYERS[i].turn
                c += 1
        
        
        
        p.allCooldown(PLAYERS)      
        if not p.Invulnerable:
            store=p.obstacle(0,PLAYERS,obs)
        # obstacle
            wn.update()
            
            for pl in PLAYERS:                 # projectile
                if(pl.turn!=p.turn): 
                    pl.Proj(PLAYERS,p.turn)
        
       
        wn.update()
        
        
        # mushrrom damage,yangiQ,goraewave
        p.constDamage(PLAYERS)
        
        wn.update()
        # skill duration cooldown\
        p.durCooldown(PLAYERS)
        
        for ps in PLAYERS:
            ps.addOutbattle()
        
        
            
        if store==-1: continue        # dont use skill after store
        
        # normalhit,
        p.basicAttack(PLAYERS)
        
            
        skills=["Q","W","U"]
            
        for i in range(0, 4):  # oneskillloop
            window.buttonupdate(p.cooltime)
            window.reportReset()
            window.getReport('이름        턴    |공격   |주문  |방어  |마저 |방관 |마관 |재생  |생명력흡수  \n')
            for ps in PLAYERS:
                window.getReport((reportfmt.format(ps.champ, ps.turn + 1, ps.AD, ps.AP, ps.AR, ps.MR, ps.arP, ps.MP, ps.regen, ps.absorb),'\n'))
            for ps in PLAYERS:
                window.getReport((ps.name,'위치:',ps.location,ps.kill, '/', ps.death, '/', ps.assist, '쉴드:', ps.shield,'쿨타임:', ps.cooltime[0], '/', ps.cooltime[1], '/', ps.cooltime[2], '스킬지속시간:', ps.duration[0], '/', ps.duration[1], '/', ps.duration[2],'\n'))

            # skill damage display
            
            # chose skill
           
            if p.effects[4]>0 and not p.isai: 
                mb.showinfo(None, "이번턴엔 스킬사용 불가")
                break
            
            
            
            if p.isai:
                time.sleep(0.2)
                if i==0:
                    skill=p.AI_3(PLAYERS)
                elif i==1:
                    skill=p.AI_2(PLAYERS)
                elif i==2:
                    skill=p.AI_1(PLAYERS)
                else: break
                
                if skill==0:           #use next skill
                    continue                   
                
                
                
            else:
                skill=window.skillupdate(p.getTooltip())
                
                if skill==2 and p.phase<2:
                    mb.showerror(None, "아직 스킬을 배우지 않았습니다!")
                    continue
                    
                elif skill==3 and p.phase<3:
                    mb.showerror(None, "아직 스킬을 배우지 않았습니다!")
                    continue
                     
            
            if skill == 0:                  #goto next turn
                #p.otherCooldown()
                window.reportReset()
                window.getReport('이름        턴    |공격   |주문  |방어  |마저 |방관 |마관 |재생  |생명력흡수 \n')
                for ps in PLAYERS:
                    window.getReport((reportfmt.format(ps.champ, ps.turn + 1, ps.AD, ps.AP, ps.AR, ps.MR, ps.arP, ps.MP, ps.regen, ps.absorb),'\n'))
                for ps in PLAYERS:
                    window.getReport((ps.name,'위치:',ps.location,ps.kill, '/', ps.death, '/', ps.assist, '쉴드:', ps.shield,'쿨타임:', ps.cooltime[0], '/', ps.cooltime[1], '/', ps.cooltime[2], '스킬지속시간:', ps.duration[0], '/', ps.duration[1], '/', ps.duration[2],'\n'))

                break
            

            
            output = p.useSkill(skill, PLAYERS) #output=-1   nocool or canceled   output=0 used  skill anyways
            window.statusupdate(p.turn,p.champ,p.duration,p.effects)
            
            
            if output == -1: continue
            
            if output==0:
                if p.mregion==1:
                        p.effects[1]=1
                continue
            
            
            
            
            
            
            for i in range(len(output[3])):   #onetarget loop (loops multiple times if multiple target  )
                p.hitoneTarget(i,PLAYERS,output,skillfrom,skill)
                

                
                
                    
                window.reportReset()
                window.getReport('이름        턴|공격   |주문   |방어   |마저   |방관   |마관   |재생 |생명력흡수 \n')
                for ps in PLAYERS:
                    window.getReport((reportfmt.format(ps.champ, ps.turn + 1, ps.AD, ps.AP, ps.AR, ps.MR, ps.arP, ps.MP, ps.regen, ps.absorb),'\n'))
                for ps in PLAYERS:
                    window.getReport((ps.name,'위치:',ps.location,ps.kill, '/', ps.death, '/', ps.assist, '쉴드:', ps.shield,'쿨타임:', ps.cooltime[0], '/', ps.cooltime[1], '/', ps.cooltime[2], '스킬지속시간:', ps.duration[0], '/', ps.duration[1], '/', ps.duration[2],'\n'))

        p.otherCooldown()
                    
                    
