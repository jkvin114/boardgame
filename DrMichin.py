#-*- coding: ms949 -*-
from player import Player
from player import Projectile
import tkinter.messagebox as mb
# from gamerunner import players
import winsound
import window
from board import drawrange

class DrMichin(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"미친박사 봇",iscomputer)
        else:super().__init__(id, name, turn,"미친박사",iscomputer)
        self.proj=(Projectile(12,self,2))
        self.itemtree=[0,3,0,3,0,9,0]        #itemtree complete count(0 for nothing bought), first,second.....  ,last item that will be bought repeatedly if money left
        self.additionalHP=0
        self.Wactive=False
    
    def useSkill(self, s, players):

        if s == 1:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[0])
                return -1
            else:
                if self.HP<=35:
                    mb.showinfo(None, "체력이 부족합니다")
                    return -1
                
                mdmg = 10 + int(self.MaxHP/5)
                
                        
                if self.isai:             #AI projectile launch
                    project=self.AIproj(20,20,players)
                    if project==0: return -1
                    
                    
                # projectile check
                else:
                    if self.adamage==30:
                        drawrange(self.zero(self.location-30),(self.location+30))
                    else:
                        drawrange(self.zero(self.location-10),self.location+10)
                    project=[False,0]
                    while(True):
                        project=self.testProj(10,10)
                        if project==0: return -1
                        
                        if project[0]: break;
                    
                
                self.cooltime[0] = 2        
                self.giveDamage(players,35, 0)
                winsound.PlaySound('sound\\place.wav', winsound.SND_ASYNC)
                self.proj.setproj(mdmg,project[1],3)
                window.getAlarm(self.name+"Q 사용함")
                return 0
                
        elif s == 2:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[1])
                return -1
            if self.Wactive: return -1
            else:
                self.additionalHP=int(self.MaxHP*0.3)
                self.addMaxhp(self.additionalHP)
                window.getAlarm(self.name+"W 활성화됨")
                self.Wactive=True
                return 0
             
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[2])
                return -1
            else:
                self.duration[2] = 5
                self.cooltime[2] = 12
                window.getAlarm(self.name+"궁 활성화됨")
                return 0    
                
    def getTooltip(self):
        tool=["","",""]
        dmg = 10 + int(self.additionalHP/10)
        
        tool[0]=("사정거리:10칸,범위2칸,데미지:%d 인 식칼을 발사함"%dmg)
        tool[1]="고유 지속 효과: 최대체력 30%증가(최초1회 w 사용하여 발동 시작)"
        tool[2]="사용시 5턴간 매턴마다 최대체력의 20%회복, 잃은체력 10당 추가회복 4"
        
        return tool
    
    def resetProjectile(self):
        self.proj.reset()
    
    def Proj(self,p,skillto):
        
        died=False   
        
        if self.projCheck(p,self.turn,skillto,self.proj) and self.proj.dur>0: 
            
            p[skillto].effects[0]=1
            died=self.skillHit(p, [0,self.proj.damage,0], self.turn, skillto, 1)            
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
                
        if self.phase>1 and not self.Wactive:           # use w if cool is back and there`s nearby opponent
            return 2
        else: return 0
        
    def AI_3(self,players):
        if self.cooltime[2]==0 and self.phase>2 and self.duration[2]==0:           # use u if cool is back
            return 3
        else: return 0
    
                
