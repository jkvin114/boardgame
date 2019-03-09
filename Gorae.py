#-*- coding: ms949 -*-
from player import Player
from player import Projectile
# from gamerunner import players
import tkinter.messagebox as mb
from winsound import PlaySound,SND_ASYNC
import window
class Gorae(Player):
    
    def __init__(self, id, name, turn,iscomputer):
        if iscomputer:super().__init__(id, name, turn,"고래 봇",iscomputer)
        else:super().__init__(id, name, turn,"고래",iscomputer)
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
                skillto=self.choosetarget(players,25,3)
                
                if skillto > -1 and self.isbehindof(players[skillto]):
                    pdmg = int(10 + int(0.5*self.AP)+int(self.HP/10)*2)
                    self.cooltime[0] = 8
                    self.location = players[skillto].location
                    self.character.Move(self.location)
                    needopp = True
                    return [pdmg, mdmg, fdmg,[ skillto]]
                
                return 0    
            
        elif s == 2:
            if self.duration[1]>0:
                self.endW(players)
                return -1
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[1])
                return -1
            else:
                if self.phase<=4:self.addShield(int(50 + self.AP + (self.HP / 10) * 5))
                else: self.addShield(int(100 + self.AP + (self.HP / 10) * 5))
                
                self.duration[1] = 4
                
                return 0   
             
        elif s == 3:
            if self.cooltime[s - 1] > 0:
                mb.showinfo(None, "아직 쿨타임이 돌아오지 않았습니다! %d 턴 남음" %self.cooltime[2])
                return -1
            else:
                skillto=self.choosetarget(players,20,3)
                
                if skillto > -1:
                    fdmg = int(20 + 0.5 * self.AP + 0.3 * self.MaxHP)
                    self.cooltime[2] = 8
                    needopp = True
                else: return -1  
        return [pdmg, mdmg, fdmg,[ skillto] ]
    def getTooltip(self):
        tool=["","",""]
       
        tool[0]="5칸 뒤에 매턴마다 5칸씩 이동하는 파도 소환 \n데미지:%d"%(10+0.5*self.AP)
        tool[1]="4턴간 일정량의 피해를 막아주는 쉴드 생성,다시 시전시 중단됨, 중단시 다음턴에 주변 3칸에 데미지 %d"%int(30+0.5*self.AP+self.HP*0.1)
        tool[2]=("범위:20,대상 플레이어에게 데미지:%d, \n 대상이 죽으면 최대체력 50증가"%(int(20 + 0.5 * self.AP + 0.2 * self.MaxHP)))
        return tool
    def Proj(self,p,skillto):
    
        return 0
    def endW(self,players):
        self.cooltime[1]=6
        self.duration[1]=0
        skillto=self.multitarget(players,self.location-3,self.location+3,2)
        if skillto==None: return 0              #used skill but there was no players in range
        window.getAlarm(self.name+"W 끝남")
        mdmg=int(30+0.5*self.AP+self.HP*0.1)
        self.addShield(-1*self.shield)
        #return [pdmg,mdmg,fdmg,skillto] 
        for i in range(len(skillto)):
            self.hitoneTarget(i, players, [0,mdmg,0,skillto], self.turn, 2)
        
    def autoskill(self,players):
        window.getAlarm("auto")
        w=self.useWnext
        
        self.useWnext=False
        if w: return self.endW(players)
        else: return 0
    def resetProjectile(self):
        return
    def goraeProj(self,pl):
        died=False   
        PlaySound('sound\\wave.wav', SND_ASYNC)
        pdmg=self.proj.damage
        for p in pl:
            skillto=p.turn
            if self.projCheck(pl,self.turn,skillto,self.proj) and self.turn != skillto: 
                self.stats[0]+=pdmg
                totaldamage=p.totalDamage(self,pdmg,0,self.arP,self.MP)
               
                p.effects[0]=2
                #PlaySound('sound\\hit.wav', SND_ASYNC)
                died = p.giveDamage(pl,totaldamage, self.turn)
                
                if died: 
                    self.addKill(1)
                
                p.resetOutbattle()
                return died
    def AI_1(self,players):
        if self.cooltime[0]==0:           # use q if cool is back
            window.getAlarm(self.name+"Q 사용")
            return 1
        else: return 0
        
    def AI_2(self,players):
        if self.phase>1 and self.cooltime[1]==0 and self.duration[1]==0:           # use w if cool is back 
            window.getAlarm(self.name+"W 사용")
            return 2
        else: return 0
        
    def AI_3(self,players):
        if self.cooltime[2]==0 and self.phase>2 and self.duration[2]==0:  # use u if cool is back
            window.getAlarm(self.name+"궁 사용")
            return 3
        else: return 0
