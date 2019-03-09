#-*- coding: ms949 -*-
from player import Player
# from gamerunner import players
import tkinter.messagebox as mb
import window

class Yangi(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"미친 양 봇",iscomputer)
        else:super().__init__(id, name, turn,"미친 양",iscomputer)
        self.yangiWspeed=0
        self.itemtree=[0,0,0,9,0]        #itemtree complete count(0 for nothing bought), first,second.....  ,last item that will be bought repeatedly if money left

    def useSkill(self, s,players):
        
        mdmg = 0
        pdmg = 0
        fdmg = 0

        skillto=0
        if s == 1:
        
            if self.duration[0]==0:
                self.duration[0]=999
                window.getAlarm(self.name+"Q 활성화됨")
                return 0
            else:
                self.duration[0]=0
                
                window.getAlarm(self.name+"Q 비활성화")
        
                return -1    
            
        elif s == 2:
            if self.duration[1]>0:
                self.duration[1]=0
                self.effects[2]=0
                self.effects[1]=self.yangiWspeed
                return -1
            elif self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[1])
                return -1
            else:
                self.duration[1]=3
                self.cooltime[1]=5
                self.effects[2]=2
                window.getAlarm(self.name+"W 사용함")
                
                return 0   
             
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[2])
                return -1
            else:
                
                skillto=self.choosetarget(players,5,3)
                
                if skillto>-1:
                    self.cooltime[2]=8
                    pdmg=50+self.AD+int(0.5*(players[skillto].MaxHP-players[skillto].HP))
                    needopp=True           
                    window.getAlarm(self.name+"이(가) "+players[skillto].name+"("+players[skillto].champ+") 에게 궁 사용")
                    
                else: return -1  
                
                
        return [pdmg,mdmg,fdmg,[skillto] ]
    def getTooltip(self):
        tool=["","",""]
        tool[0]="활성화시 3칸내의 모든 플레이어 공격 "
        tool[1]="사용시 3턴에 걸쳐 체력회복, \n회복 중엔 움직일 수 없음"
        tool[2]=("사정거리:5 ,대상 플레이어에게 데미지:%d+대상의 잃은 체력"%(50+self.AD))
        return tool
    def resetProjectile(self):
        return
    def Proj(self,p,skillto):
        return 0
    def AI_1(self,players):
        closeopponent=False
        for p in players:
            if abs(self.location-p.location)<7 and self!=p:                
                closeopponent=True
        
        if self.duration[0]>0 and float(self.HP/self.MaxHP)<0.4:      # stops Q if hp is under 40%
            return 1
        elif self.duration[0]>0 and closeopponent==False:      # stops Q if no nearby opponent
            return 1
        elif closeopponent and self.duration[0]==0 and float(self.HP/self.MaxHP)>=0.4:        #start Q if hp is over 40% and Q isnt currently active and opponent is in 7 blocks
            return 1
        else: return 0
    
    def AI_2(self,players):
        if self.phase>1 and self.cooltime[1]==0 and self.duration[1]==0 and float(self.HP/self.MaxHP)<0.3:        #use W if hp is under 40%
            return 2
        else: return 0
    
    def AI_3(self,players):
        if self.phase>2 and self.cooltime[2]==0:           # use U if cool is back
            return 3
        else: return 0
                    
        
        
        
        
    
    