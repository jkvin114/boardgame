#-*- coding: ms949 -*-
from player import Player
from player import Projectile
import tkinter.messagebox as mb
import winsound
from board import drawrange
from board import rangepen
class Blkx(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"�κ� ��",iscomputer)
        else:super().__init__(id, name, turn,"�κ�",iscomputer)
        
        self.hand=(Projectile(9,self,3))
        self.mine=(Projectile(10,self,3))
        self.bomb=(Projectile(11,self,5))
        
    def useSkill(self, s,players):
        
        
        
        if s == 1:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[0])
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
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[1])
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
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[2])
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
       
        tool[0]=("���� 3ĭ������ ���� �߻�, ���� ����� �����,������:%d,�����Ÿ�:10"%(20+0.5*self.AP))
        tool[1]=("���� 3ĭ������ ���� �߻�,\n ���� ����� �ӹ�, ������: %d, �����Ÿ�:15"%(30+self.AP))
        tool[2]=("���� 5ĭ������ ��ź ��ô, �����Ÿ�:30,���� ��󿡰� ������:%d"%(40+self.AP))
      
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
