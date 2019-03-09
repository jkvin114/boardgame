#-*- coding: ms949 -*-
from player import Player
from player import Projectile
import tkinter.messagebox as mb
import winsound
from board import drawrange
class Jean(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"저격수 봇",iscomputer)
        else:super().__init__(id, name, turn,"저격수",iscomputer)
        self.utarget=0
        self.proj=Projectile(5,self,3)     

    def useSkill(self, s,players):
        
        mdmg = 0
        pdmg = 0
        fdmg = 0

        skillto=0
        if s == 1:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[0])
                return -1    
            else:
                skillto=self.choosetarget(players,20,1)
                if skillto>-1:
                    pdmg=int(10+self.AD)
                    self.cooltime[0]=2
                    needopp=True
                else: return -1
            
        elif s == 2:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[1])
                return -1
            else:

                
                if self.adamage==30:
                    drawrange(self.zero(self.location-90),(self.location+90))
                else:
                    drawrange(self.zero(self.location-30),self.location+30)
                project=[False,0]
                while(True):
                    project=self.testProj(20,20)
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
                needopp=True
                
                if self.duration[2]==0:
                    skillto=self.choosetarget(players,50,3)
                    if skillto>-1:
                        pdmg=int(20+self.AD)
                        self.duration[2]=3
                        self.effects[2]=1
                        self.utarget=skillto
                    else: return -1  
                elif self.duration[2]==2:
                    pdmg=int(20+self.AD)
                    self.effects[2]=1
                    skillto=self.utarget
                elif self.duration[2]==1:
                    fdmg=int(20+self.AD)
                    
                    skillto=self.utarget
                
                
        return [pdmg,mdmg,fdmg,[skillto]] 
    def getTooltip(self):
        tool=["","",""]
       
        tool[0]=("사정거리:20 ,사용시 대상에게 데미지:%d \n 표식이 있을시 속박시킴"%(10+self.AD))
        tool[1]="사정거리:20 ,사용시 3칸범위의 덫을 발사함, 덫에 맞으면 둔화, 표식을 남김 "
        if self.duration[2]==0:
            tool[2]=("사정거리:50, 사용시 대상 고정후 최대3번 발사, 데미지: %d" %(20+self.AD))
        elif self.duration[2]>0:
            tool[2]=("대상에게 계속 발사, 데미지: %d"%(20+self.AD))
        return tool
    def resetProjectile(self):
        self.proj.reset()
    def Proj(self,p,skillto):
        
        if self.projCheck(p,self.turn,skillto,self.proj) and self.proj.dur>0: 
            p[skillto].marks[1]=[3,self.turn+1]
            winsound.PlaySound('sound\\hit.wav', winsound.SND_ASYNC)
            p[skillto].effects[0]=4
            self.proj.reset()
        if self.proj.dur==0:
            self.proj.reset()
        
        self.proj.dur-=1 
        return False
