#-*- coding: ms949 -*-
from player import Player
from player import Projectile
import tkinter.messagebox as mb
import winsound
from board import drawrange
from board import rangepen
class Movingshin(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"무빙신 봇",iscomputer)
        else:super().__init__(id, name, turn,"무빙신",iscomputer)
        self.shadow=(Projectile(8,self,0))
        self.sound=(Projectile(7,self,3))
        self.Qhit=-1
        
    def useSkill(self, s,players):
        
        mdmg = 0
        pdmg = 0
        fdmg = 0

        skillto=0
        if s == 1:
            if self.Qhit>-1:
                self.goto(players[self.Qhit].location)
                skillto=self.Qhit
                self.Qhit=-1
                
                pdmg=20+self.AD
                needopp=True
                
                return [pdmg,mdmg,fdmg,[skillto]] 
            
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[0])
                return -1
            else:
              
                if self.adamage==30:
                    drawrange(self.zero(self.location-45),(self.location+45))
                else:
                    drawrange(self.zero(self.location-15),self.location+15)
                project=[False,0]
                while(True):
                    project=self.testProj(15,15)
                    if project==0: return -1
                    if project[0]: break;
                
                self.cooltime[0] = 4        
                nontarget=True
                winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                self.sound.setproj(0, project[1],2)
                
                
                return 0
        elif s == 2:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[1])
                return -1
            else:
                skillto=self.multitarget(players,self.location-3,self.location+3,2)
                if skillto==None: return 0              #used skill but there was no players in range
                
                print(skillto)
                pdmg=int(20+0.5*self.AD)
                self.cooltime[1]=2
                
                return [pdmg,mdmg,fdmg,skillto] 
             
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[2])
                return -1
            else:
                if self.shadow.dur>0:
                    self.location=self.shadow.location
                    obs=self.character.Move(self.shadow.location)
                    self.shadow.reset()
                    self.cooltime[2] = 4
                    self.obstacle(0, players,obs)
                else:
                    if self.adamage==30:
                        drawrange(self.zero(self.location-60),(self.location+15))
                    else:
                        drawrange(self.zero(self.location-20),self.location+5)
                    
                    while(True):
                        project=self.testProj(5,20)
                        if project==0: return -1
                        if project[0]: break;
                    
                   
                    self.shadow.setproj(0, project[1],4)
                    rangepen.clear()
                    winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                    
                return 0
        
    def getTooltip(self):
        tool=["","",""]
       
        if self.Qhit>-1:
            tool[0]=("Q를 맞은 대상에게 이동, 데미지:%d"%(20+self.AD))
        else:
            tool[0]=("사정거리:15 \n 다음턴에 대상에게 이동 가능")
            
        tool[1]=("3칸내의 모든 플레이어 데미지, \n데미지:%d"%(20+0.5*self.AD))
        if self.shadow.location==-1:
            tool[2]=("그림자 설치, 사정거리:20")
        else:
            tool[2]=("그림자로 이동")
        return tool
    def resetProjectile(self):
        self.shadow.reset()
        self.sound.reset()
    
    def Proj(self,p,skillto):
        
        if self.projCheck(p,self.turn,skillto,self.sound) and self.sound.dur>0: 
            p[skillto].marks[2]=[3,self.turn+1]
            winsound.PlaySound('sound\\hit.wav', winsound.SND_ASYNC)
            self.Qhit=p[skillto].turn
            
            self.sound.reset()
            
        if self.sound.dur==0:
            self.sound.reset()
        if  self.shadow.dur==0:
            self.shadow.reset()
        
        self.sound.dur-=1
        self.shadow.dur-=1
        return False
