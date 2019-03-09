#-*- coding: ms949 -*-
from player import Player
from player import Projectile
import tkinter.messagebox as mb
import winsound
from board import drawrange
class Jean(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"���ݼ� ��",iscomputer)
        else:super().__init__(id, name, turn,"���ݼ�",iscomputer)
        self.utarget=0
        self.proj=Projectile(5,self,3)     

    def useSkill(self, s,players):
        
        mdmg = 0
        pdmg = 0
        fdmg = 0

        skillto=0
        if s == 1:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[0])
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
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[1])
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
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[2])
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
       
        tool[0]=("�����Ÿ�:20 ,���� ��󿡰� ������:%d \n ǥ���� ������ �ӹڽ�Ŵ"%(10+self.AD))
        tool[1]="�����Ÿ�:20 ,���� 3ĭ������ ���� �߻���, ���� ������ ��ȭ, ǥ���� ���� "
        if self.duration[2]==0:
            tool[2]=("�����Ÿ�:50, ���� ��� ������ �ִ�3�� �߻�, ������: %d" %(20+self.AD))
        elif self.duration[2]>0:
            tool[2]=("��󿡰� ��� �߻�, ������: %d"%(20+self.AD))
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
