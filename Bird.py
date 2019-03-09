#-*- coding: ms949 -*-
from player import Player
from player import Projectile
import tkinter.messagebox as mb
# from gamerunner import players
import winsound
import window
from board import drawrange

class Bird(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"���� ��",iscomputer)
        else:super().__init__(id, name, turn,"����",iscomputer)
        self.proj=(Projectile(1,self,3))
        self.itemtree=[0,3,0,3,0,9,0]        #itemtree complete count(0 for nothing bought), first,second.....  ,last item that will be bought repeatedly if money left

    def getQcool(self):
        return self.cooltime[1]
    
    def useSkill(self, s, players):

        if s == 1:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[0])
                return -1
            else:
                mdmg = 10 + self.AP
                if self.duration[1] > 0:
                    if self.duration[2] > 0:
                        mdmg += 10 + self.AP
                    else:
                        mdmg += int(10 + 0.5 * self.AP)
                        
                if self.isai:             #AI projectile launch
                    project=self.AIproj(20,20,players)
                    if project==0: return -1
                    
                    
                # projectile check
                else:
                    if self.adamage==30:
                        drawrange(self.zero(self.location-60),(self.location+60))
                    else:
                        drawrange(self.zero(self.location-20),self.location+20)
                    project=[False,0]
                    while(True):
                        project=self.testProj(20,20)
                        if project==0: return -1
                        
                        if project[0]: break;
                    
                
                self.cooltime[0] = 4        
                winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                self.proj.setproj(mdmg,project[1],4)
                window.getAlarm(self.name+"Q �����")
                return 0
                
        elif s == 2:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[1])
                return -1
            else:
                self.duration[1] = 3
                self.cooltime[1] = 5
                window.getAlarm(self.name+"W Ȱ��ȭ��")
                return 0
             
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "���� ��Ÿ���� ���ƿ��� �ʾҽ��ϴ�! %d �� ����" %self.cooltime[2])
                return -1
            else:
                self.duration[2] = 8
                self.cooltime[2] = 13
                window.getAlarm(self.name+"�� Ȱ��ȭ��")
                return 0    
                
    def getTooltip(self):
        tool=["","",""]
        dmg = 10 + self.AP
        if self.duration[1] > 0:
            if self.duration[2] > 0:
                dmg += 10 + self.AP
            else:
                dmg += int(10 + 0.5 * self.AP)
        tool[0]=("�����Ÿ�:20ĭ,����3ĭ,������:%d �� ħ�� �߻���"%dmg)
        tool[1]="������� ��ȯ, \n ��Ÿ�� Q ���� �߰�����"
        tool[2]="�չ��� ��ȯ, \n ��Ÿ ��Ÿ� ����, ������� �߰����� ����"
        
        return tool
    
    def resetProjectile(self):
        self.proj.reset()
    
    def Proj(self,p,skillto):
        
        died=False   
        
        if self.projCheck(p,self.turn,skillto,self.proj) and self.proj.dur>0: 
            
            
            p[skillto].moneyTaken(30)
            window.getAlarm("���忡�� 30��带 ���ѱ�")
            self.giveMoney(30)
            died=self.skillHit(p, [0,self.proj.damage,0], self.turn, skillto, 1)
#             mdmg=self.proj.damage
#             self.stats[0]+=mdmg
#             totaldamage=p[skillto].totalDamage(self,0,mdmg,self.arP,self.MP)
#             died = p[skillto].giveDamage(p,totaldamage, self.turn)
            
            if died: 
                self.addKill(1)
            
            
            
            self.proj.reset()
            
           
            p[skillto].resetOutbattle()
        
        elif self.proj.dur==0:
            self.proj.reset()
            
        self.proj.dur-=1
        return died
    
    
    def AI_1(self,players):
        if self.cooltime[0]==0:           # use q if cool is back
            return 1
        else: return 0
        
    def AI_2(self,players):
                
        if self.phase>1 and self.cooltime[1]==0:           # use w if cool is back and there`s nearby opponent
            return 2
        else: return 0
        
    def AI_3(self,players):
        if self.cooltime[2]==0 and self.phase>2 and self.duration[2]==0:           # use u if cool is back
            return 3
        else: return 0
    
                
