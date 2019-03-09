#-*- coding: ms949 -*-
from player import Player
import tkinter.messagebox as mb
import window

class Silver(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"닌자 봇",iscomputer)
        else:super().__init__(id, name, turn,"닌자",iscomputer)
        self.silveru1 = 0
        self.silveru2 = 0
        self.itemtree=[0,3,9,9,9,3]
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
                skillto=self.choosetarget(players,2,1)
                if skillto > -1: 
                    mdmg = int(10 + 0.5 * (self.AP + self.AR + self.MR))
                    self.cooltime[0] = 2
                    needopp = True
                    #window.getAlarm(self.name+"used Q to "+players[skillto].name+"("+players[skillto].champ+")")
                else: return -1  
        elif s == 2:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[1])
                return -1 
            else:
                skillto=self.choosetarget(players,20,2)
                if skillto > -1:
                    self.cooltime[1] = 5  
                    needopp = True
                    #window.getAlarm(self.name+"used W to "+players[skillto].name+"("+players[skillto].champ+")")
                else: return -1  
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[2])
                return -1
            else:
                self.cooltime[2] = 14
                self.duration[2] = 4
                if self.HP <= 150:
                    self.silveru1 = 200
                    self.MR += 200
                    self.AR += 200
                else:
                    self.silveru1 = 100
                    self.MR += 100
                    self.AR += 100
                window.getAlarm(self.name+"궁 사용, 방어력,마법저항력 +%d"%self.silveru1)
            return 0
        
        return [pdmg, mdmg, fdmg, [skillto]] 
    
    def passive(self):
        if self.phase<3: return 
        
        if self.HP>250: return
        self.AR-=self.silveru2
        self.MR-=self.silveru2
        if 150<self.HP <= 250:
            self.silveru2 = 60
            self.MR += 60
            self.AR += 60
        elif 50<self.HP<=150:
            self.silveru2 = 90
            self.MR += 90
            self.AR += 90
        elif self.HP<=50:
            self.silveru2 = 120
            self.MR += 120
            self.AR += 120
            
            
    def getTooltip(self):
        tool=["","",""]
        if self.HP<=150: df=200
        else: df=100
        tool[0]=("사정거리:2, 표식 있을시 7,사용시 대상에게 데미지:%d \n 대상이 표식을 가지고 있으면 데미지+3"%(10 + 0.5 * (self.AP + self.AR + self.MR)))
        tool[1]="범위:20,사용시 대상에게 표식을 남김"
        tool[2]=("사용시 4턴간 방어력,마법저항력 +%d"%df)
        return tool      
    def resetProjectile(self):
        return  
    def Proj(self,p,skillto):
        return 0
    
    def AI_1(self,players):
        if self.cooltime[0]==0:           # use q if cool is back
            window.getAlarm(self.name+"Q 사용")
            return 1
        
        else: return 0
        
    def AI_2(self,players):
        closeopponent=False
        for p in players:
            if abs(self.location-p.location)<7 and self!=p:                
                closeopponent=True
                
                
        if self.phase>1 and self.cooltime[1]==0 and self.cooltime[0]==0 and closeopponent:           # use w if w,q cool is back and theres nearby opponent
            window.getAlarm(self.name+"W 사용")
            return 2
        else: return 0
        
    def AI_3(self,players):
        if self.cooltime[2]==0 and self.phase>2 and self.duration[2]==0:           # use u if cool is back
            return 3
        else: return 0
    
    