#-*- coding: ms949 -*-
from player import Player
from board import player
from player import Projectile
import tkinter.messagebox as mb
import winsound
import window
from board import drawrange
class Creed(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"검사 봇",iscomputer)
        else:super().__init__(id, name, turn,"검사",iscomputer)
        self.proj=(Projectile(3,self,3)) 
        self.itemtree=[0,0,0,0,9,9,0]
        self.usedQ1=False
    def useSkill(self, s, players):
        
        mdmg = 0
        pdmg = 0
        fdmg = 0

        skillto = 0
        if s == 1:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[0])
                return -1    
            elif self.usedQ1:
                skillto=self.choosetarget(players,3,1)
                if skillto > -1:
                    pdmg = int((20 + self.AD)*0.5)
                    self.cooltime[0] = 3
                    needopp = True
                    self.usedQ1=False
                else: return -1  
            else:
                skillto=self.choosetarget(players,3,1)
                if skillto > -1:
                    pdmg = int((20 + self.AD))
                    needopp = True
                    self.usedQ1=True
                else: return -1  
        elif s == 2:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[1])
                return -1
            else:
                if self.isai:             #AI projectile launch
                    project=self.AIproj(30,30,players)
                    if project==0: return -1
                else:
                    if self.adamage==30:
                        drawrange(self.zero(self.location-90),(self.location+90))
                    else:
                        drawrange(self.zero(self.location-30),self.location+30)
                    project=[False,0]
                    while(True):
                        project=self.testProj(30,30)
                        if project==0: return -1
                        if project[0]: break;
                
                 
                self.cooltime[1] = 5        
                nontarget=True
                winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                self.proj.setproj(0, project[1],4)
                
            return 0   
             
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[2])
                return -1
            else:
                skillto=self.choosetarget(players,25,3)
                
                if skillto > -1 and self.isbehindof(players[skillto]):
                    pdmg = int(30 + self.AD)
                    self.cooltime[2] = 8
                    self.location = players[skillto].location
                    self.character.Move(self.location)
                    needopp = True
                else: return -1  
        return [pdmg, mdmg, fdmg,[skillto]] 
    def getTooltip(self):
        tool=["","",""]
       
        tool[0]=("사정거리:3,맞은 플레이어 데미지:%d"%(int((20 + self.AD) * 1.5)))
        tool[1]="사정거리:30 ,맞은 플레이어를 5칸 뒤로 이동시키는 \n 범위 3칸의 토네이도 발사"
        tool[2]=("사정거리: 25, 사용시 대상에게 순간이동함.데미지:%d"%(30+self.AD))
        return tool
    def resetProjectile(self):
        self.proj.reset()
    def Proj(self,p,skillto):
        
        if self.projCheck(p,self.turn,skillto,self.proj) and self.proj.dur>0: 
            winsound.PlaySound('sound\\hit.wav', winsound.SND_ASYNC)
            p[skillto].location-=5
            obs=p[skillto].character.Move(p[skillto].location)
            p[skillto].obstacle(0,p,obs)
            p[skillto].effects[2]=0
            self.proj.reset()
            
        if self.proj.dur==0:
            self.proj.reset()
        self.proj.dur-=1
        return False
    def AI_1(self,players):
        if self.cooltime[0]==0:           # use q if cool is back
            window.getAlarm(self.name+"Q 사용")
            return 1
        else: return 0
    def AI_2(self,players):
        if self.cooltime[1]==0:           # use w if cool is back
            return 2
        else: return 0
    def AI_3(self,players):
        if self.phase>2 and self.cooltime[2]==0:           # use U if cool is back
            window.getAlarm(self.name+"궁 사용")
            return 3
        else: return 0
                    