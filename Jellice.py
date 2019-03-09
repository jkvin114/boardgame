#-*- coding: ms949 -*-
from player import Player
from player import Projectile
import tkinter.messagebox as mb
import winsound
from board import drawrange
from board import rangepen
class Jellice(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"���콺 ��",iscomputer)
        else:super().__init__(id, name, turn,"���콺",iscomputer)
        
        self.proj=Projectile(6,self,3) 
        self.Uuse=0

    def useSkill(self, s,players):
        
        mdmg = 0
        pdmg = 0
        fdmg = 0

        skillto=0
        skillto2=0
        if s == 1:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[0])
                return -1    
            else:
               # mdmg=10+self.AP*0.5
                r=15
                
                if self.duration[1]>1: r*=2
                if self.adamage==30: r*=3
                drawrange(self.zero(self.location+5),(self.location+r))
                rangepen.clear()
                drawrange(self.zero(self.location-r),self.zero(self.location-5))
                skillto=self.multitarget(players,self.zero(self.location+5),self.location+r,1)
                
                rangepen.clear()
                
                skillto2=self.multitarget(players,self.zero(self.location-r),self.zero(self.location-5),1)
                #print(skillto,skillto2)
                if skillto==None and skillto2==None: return -1
                elif skillto==None: skillto=skillto2
                elif skillto2!=None and skillto!=None: skillto.extend(skillto2)
                
                mdmg=int(10+self.AP)
                self.cooltime[0]=4
                needopp=True
                #nn  n1 1n 11
                    
                return [pdmg,mdmg,fdmg,skillto] 
            
        elif s == 2:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[1])
                return -1
            else:
                self.effects[2]=1
                self.effects[1]=2
                self.cooltime[1]=5
                self.duration[1]=2
                
                
                return 0   
             
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[2])
                return -1
            else:
                self.Uuse+=1
                mdmg=10+self.AP*0.5
                r=30
                if self.duration[1]>1: r*=2
                
                if self.adamage==30: r*=3
                
                
                
                drawrange(self.zero(self.location-r),self.location+r)
                project=[False,0]
                while(True):
                    if self.duration[1]>1: project=self.testProj(60,60)
                    else: project=self.testProj(30,30)
                    if project==0: return -1
                    if project[0]: break;
                    
                
                        
                
                winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                self.proj.setproj(mdmg, project[1],2)
                
                
                return 0
    def getTooltip(self):
        tool=["","",""]
       
        tool[0]=("����:�յ� 5~15ĭ, ������:%d \n ���� �������� ��� �÷��̾� ������"%(10+self.AP))
        tool[1]="���� 1 �� �ӹ� �� ��罺ų ��Ÿ�2��, �����Ͽ� �ż�"
        tool[2]=("�����Ÿ�:30, ����:3, ���� ������:%d, \n %d �� �� ��밡��, ���� ����� ħ���� �ɸ�"%((10+0.5*self.AP),(3-self.Uuse)))
        
      
        return tool
    def resetProjectile(self):
        self.proj.reset()
    def Proj(self,p,skillto):
        died=False   
        if self.projCheck(p,self.turn,skillto,self.proj) and self.proj.dur>0: 
            
            
            died=self.skillHit(p, [0,self.proj.damage,0], self.turn, skillto, 1)
            
            if died: 
                self.addKill(3)
            
            self.proj.reset()
            p[skillto].resetOutbattle()
            if self.Uuse>=2:
                self.cooltime[2]=3
                self.Uuse=0
                
        self.proj.dur-=1
        
        if self.proj.dur==0:
            self.proj.reset()
        return died
        
                
