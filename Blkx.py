#-*- coding: ms949 -*-
from player import Player
from player import Projectile
import tkinter.messagebox as mb
import winsound
from board import drawrange
from board import rangepen
class Blkx(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"로봇 봇",iscomputer)
        else:super().__init__(id, name, turn,"로봇",iscomputer)
        
        self.hand=(Projectile(9,self,3))
        self.mine=(Projectile(10,self,3))
        self.bomb=(Projectile(11,self,5))
        
    def useSkill(self, s,players):
        
        
        
        if s == 1:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[0])
                return -1 
            else:
                mdmg = 20 + 0.5*self.AP
               
                # projectile check
                if self.adamage==30:
                    drawrange(self.zero(self.location-30),(self.location+30))
                else:
                    drawrange(self.zero(self.location-10),self.location+10)
                project=[False,0]
                while(True):
                    project=self.testProj(10,10)
                    if project==0: return -1
                    
                    if project[0]: break;
                    
                
                self.cooltime[0] = 8        
                winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                self.hand.setproj(mdmg,project[1],4)
                
        elif s == 2:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[1])
                return -1
            else:
                mdmg = 30 + self.AP
               
                # projectile check
                if self.adamage==30:
                    drawrange(self.zero(self.location-45),(self.location+45))
                else:
                    drawrange(self.zero(self.location-15),self.location+15)
                project=[False,0]
                while(True):
                    project=self.testProj(15,15)
                    if project==0: return -1
                    
                    if project[0]: break;
                    
                
                self.cooltime[1] = 6        
                winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                self.mine.setproj(mdmg,project[1],4)
                
             
             
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[2])
                return -1
            else:
                mdmg = 40 + self.AP
               
                # projectile check
                if self.adamage==30:
                    drawrange(self.zero(self.location-90),(self.location+90))
                else:
                    drawrange(self.zero(self.location-30),self.location+30)
                project=[False,0]
                while(True):
                    project=self.testProj(30,30)
                    if project==0: return -1
                    
                    if project[0]: break;
                    
                
                self.cooltime[2] = 10        
                winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                self.bomb.setproj(mdmg,project[1],4)
                
           
        return 0
    def getTooltip(self):
        tool=["","",""]
       
        tool[0]=("사용시 3칸범위의 손을 발사, 맞은 대상을 끌어옴,데미지:%d,사정거리:10"%(20+0.5*self.AP))
        tool[1]=("사용시 3칸범위의 지뢰 발사,\n 맞은 대상은 속박, 데미지: %d, 사정거리:15"%(30+self.AP))
        tool[2]=("사용시 5칸범위의 폭탄 투척, 사정거리:30,맞은 대상에게 데미지:%d"%(40+self.AP))
      
        return tool
    def resetProjectile(self):
        self.hand.reset()
        self.mine.reset()
        self.bomb.reset()
    
    def Proj(self,p,skillto):
        
        died=False   
        if self.projCheck(p,self.turn,skillto,self.hand) and self.hand.dur>0: 
            p[skillto].location = self.location
            p[skillto].character.Move(self.location)
            
            p[skillto].effects[2]=0
            p[skillto].effects[4]=1
            died=self.skillHit(p, [0,self.hand.damage,0], self.turn, skillto, 1)
            if died: 
                self.addKill(1)
            p[skillto].resetOutbattle()
            
            
        
            self.hand.reset()
            
        if self.projCheck(p,self.turn,skillto,self.mine) and self.mine.dur>0: 
            p[skillto].effects[2]=1
            died=self.skillHit(p, [0,self.mine.damage,0], self.turn, skillto, 2)
            
            if died: 
                self.addKill(2)
            p[skillto].resetOutbattle()
            
            self.mine.reset()
            
            
        if self.projCheck(p,self.turn,skillto,self.bomb) and self.bomb.dur>0: 
            died=self.skillHit(p, [0,self.bomb.damage,0], self.turn, skillto, 3)
            
            if died: 
                self.addKill(3)
            p[skillto].resetOutbattle()
            
            self.bomb.reset()
            
        if self.hand.dur==0:
            self.hand.reset()
        if  self.mine.dur==0:
            self.mine.reset()
        if  self.bomb.dur==0:
            self.bomb.reset()
        
        self.hand.dur-=1
        self.mine.dur-=1
        self.bomb.dur-=1
        return died
