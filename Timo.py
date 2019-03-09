#-*- coding: ms949 -*-
from player import Player
from player import Projectile
# from gamerunner import players
import tkinter.messagebox as mb
import winsound
from board import drawrange
class Timo(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"정찰병 봇",iscomputer)
        else:super().__init__(id, name, turn,"정찰병",iscomputer)
        self.proj=(Projectile(4,self,4))
    def useSkill(self, s, players):
        
        mdmg = 0
        pdmg = 0
        fdmg = 0

        skillto = 0
        if s == 1:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[0])
                return -1    
            else:
                skillto=self.choosetarget(players,10,1)
                if skillto > -1:
                    pdmg = int(20 + self.AP)
                    self.cooltime[0] = 3
                    needopp = True
                else: return -1  
        elif s == 2:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[1])
                return -1
            else:
                self.cooltime[1] = 4
                self.duration[1] = 1
               
            return 0   
             
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[2])
                return -1
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
                
                
                self.cooltime[2] = 4        
                nontarget=True
                winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                self.proj.setproj(0, project[1],6)
            return -1
        return [pdmg, mdmg, fdmg,[skillto]]
    def getTooltip(self):
        tool=["","",""]
       
        tool[0]=("범위:10,사용시 맞은 대상을 실명시킴, 데미지:%d"%(20+self.AP))
        tool[1]="사용시 1턴간 모든 스킬,장애물 무시"
        tool[2]=("사정거리:30 , 범위 4칸의 버섯 설치, \n 맞은 플레이어는 지속 데미지")
        return tool
    def resetProjectile(self):
        self.proj.reset()
    def Proj(self,p,skillto):
        
        if self.projCheck(p,self.turn,skillto,self.proj) and self.proj.dur>0: 
            winsound.PlaySound('sound\\hit.wav', winsound.SND_ASYNC)
            p[skillto].effects[5][0]=3
            p[skillto].effects[5][1]=self.turn
            self.proj.reset()
        if self.proj.dur==0:
            self.proj.reset
        self.proj.dur-=1
        return False