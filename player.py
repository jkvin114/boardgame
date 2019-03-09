#-*- coding: ms949 -*-





# #0 name
# 1 id
# 2 location
# 3 phase
#  4 turn
#  5 money
#       0  1        2   3   4   5   6   7    8        9
# 6 [HP,MaxHP,AD,AP,AR,MR,arP.MP,absorb,HPregen]
# 7 [Qcool,Wcool,Ucool]
# 8 [Qdur,Wdur,Udur]
#       0     1       2     3     4        5           6       7            8        9    10       11   1 
# 9 [slow,speed,stun,blind,silent,mushroom,bank,realshield,potato,radi,annuity,loan,slave]
# 10 [tempPD,tempMD]
# 11  [silvermark,jeanmark,movinshinmark]
# 12 [outbattle,adamage,nextdmg]
# 13 [lastobs,currentobs]
# 14 proj
# 15 lastdice
# 16 mregion
# 17 lastmoney
# 18 gacool
# 19 items
# 20 stats
# player = [[],[],[],[]]
# damagedby=[turns after last damage,skillfrom] 
# 
#


 
#-*- coding: ms949 -*-
from board import *
from board import player
from board import Projgraphic
import tkinter.messagebox as mb
import winsound
import window
from displaytext import textdisplay
import random
import time
import Item
from Item import allItem
from cgi import escape
num=0
class Projectile():
    def __init__(self,Id,player,size):
        self.Id=Id
        self.who=player
        self.size=size
        self.location=-1
        self.dur=0
        self.damage=0
        self.projgraphic=(Projgraphic(Id))
        """
        Id
        1.bird
        2.goraewave
        3. creed
        4.timomush
        5.jean
        6.jellice
        7.movingshin Q
        8.movingshin U
        9. blkx q
        10 blkx w
        11 blkx u
        
        """
        
        
    def setproj(self,damage,loca,dur):
        self.damage=damage
        self.location=loca
        if loca>int(muststop[len(muststop)-1])-3: 
            loca=int(muststop[len(muststop)-1])-3
        self.dur=dur
        self.projgraphic.set(loca,self.size)
    
    def reset(self):
        self.location=-1
        self.damage=0
        self.dur=0
        self.projgraphic.hide()
        
        

class Player():
    def __init__(self, id, name, turn,champ,isai):
        self.isai=isai
        self.id = id
        self.name = name
        self.turn = turn
        self.champ=champ
        self.location =0
        self.phase = 0
        self.money = 0
        self.kill = 0
        self.death = 0
        self.assist = 0
        self.damagedby = [0, 0]  # for assist calc
        
        self.HP = 200
        self.MaxHP = 200
        self.AD = 0
        self.AP = 0
        self.AR = 0
        self.MR = 0
        self.arP = 0
        self.MP = 0
        self.absorb = 0
        self.regen = 0
        self.adStat=0
        self.basicattackRange=0
        self.addMdmg=0
        self.skilldmgReduction=0
        
        self.adStatAD=True
        self.shield = 0
        self.cooltime = [0, 0, 0]
        self.duration = [0, 0, 0]
        self.effects = [0, 0, 0, 0, 0, [0,-1], 0, 0, 0, 0, 0, 0, 0]
        self.temp = [0, 0]
        self.marks = [[0,0],[0,0],[0,0]]
        self.outbattle=0
        self.adamage=0
        self.nextdmg=0
        self.lastobs=0
        self.currobs=0
        self.proj = [0, -1]
        self.lastloc = 0
        self.mregion = 0
        self.lastmoney = 0
        self.gacool = 0 
        self.items = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0]
        self.stats = [0, 0, 0, 0, 0, 0, 0]
        self.character=(player(turn))
        self.Invulnerable=False
        
        
        
    
    def obstacle(self,re,players,obs):
        others = []
        target=-1
        out=0
        c = 0
        if 0<obs:
            textdisplay(obs)
        for i in range(0, len(players)):
            if players[i].turn != self.turn: 
                others.append(players[i].turn)
                c += 1
        if(self.effects[2]!=0):
            curobs=self.currobs
            if curobs==13 or curobs==42 or curobs==43 or curobs==44 or curobs== 45 or  curobs==51 or  curobs==57 or curobs==64:
                obs=curobs
            else:
                self.srCooldown()
                return 0
        else:
            if(self.nextdmg>0):
                winsound.PlaySound('sound\\explode.wav', winsound.SND_ASYNC)
                died=self.giveDamage(players,self.nextdmg, -4)
                
                self.nextdmg=0
                if died: return -1
                
                
            if obs==0: 
                self.Item()
                return -1
            elif self.effects[6]>0 and re==0:
                self.Bankrupt()
            self.lastobs=self.currobs
            self.currobs=obs
        if re==0: self.srCooldown()
        died=False
        if re!=0:
            for pl in players:                 # projectile
                if pl.turn!=self.turn: 
                    died=pl.Proj(players,self.turn)
            if died:
                return -1
        
        
        
        if not (-1<obs<=11 or obs== 16 or obs== 18 or obs==21 or obs==22 or obs==24 or obs==29 or obs==30 or obs==31 or obs==32 or obs==33 or obs==37 or obs==56 or obs==57):
            if self.id==6 and self.duration[1]>0:
                window.getAlarm('스킬로 장애물 무시함')
                return 0
            if self.effects[7]>0:
                self.resetRealshield()
                window.getAlarm('방어막으로 장애물 무시함')
                return 0
        if 166  <=self.location<=168:
            self.effects[9]=1
        
        
        if 0<obs<11: 
            self.giveMoney(10*obs)
            winsound.PlaySound('sound\\gold.wav', winsound.SND_ASYNC)
        elif obs==11: 
            winsound.PlaySound('sound\\trap.wav', winsound.SND_ASYNC)
            self.giveDamage(players,10,-1)
            
        elif obs==12: 
            self.moneyTaken(30)
            winsound.PlaySound('sound\\crime.wav', winsound.SND_ASYNC)
        elif obs==13 or obs==58: 
            winsound.PlaySound('sound\\explode.wav', winsound.SND_ASYNC)
            self.giveDamage(players,30, -6)
            
        elif obs==14: self.nextdmg=30
        elif obs==15: 
            winsound.PlaySound('sound\\knife.wav', winsound.SND_ASYNC)
            self.giveDamage(players,20, -7)
            
        elif obs==16: self.giveHeal(50)
        elif obs==17: self.effects[4]=1
        elif obs==18: 
            self.mregion=1
            self.adamage=20
            window.getAlarm('스킬 사용시 추가피해20, 신속 1턴 ')
        elif obs==19:
            if self.money>=0: self.giveDamage(players,self.money,-8)
            else: self.giveHeal(-1*self.money)
        elif obs==20: 
            self.thief()
            winsound.PlaySound('sound\\crime.wav', winsound.SND_ASYNC)
        elif obs==21: 
            self.resetCooltime()
            window.getAlarm('cooltime reset')
        elif obs==22: 
            self.adamage=30
            window.getAlarm('추가피해3, 사거리 3배증가')
        elif obs==23: 
            self.effects[2]=1
            winsound.PlaySound('sound\\web.wav', winsound.SND_ASYNC)
        elif obs==24: self.giveMoney(10*random.randint(1,6))
        elif obs==25: 
            target=self.turn
            if not self.isai:
                mb.showinfo(None, "태풍! 주사위 던지기 전 칸으로 이동!")
            self.currobs=self.lastobs
            time.sleep(0.3)
            
            obs=self.character.Move(self.lastloc)
            self.location=self.lastloc
            out=1
        elif obs==26: 
            
            self.effects[0]=1
            self.giveDamage(players,20, -1)
        elif obs==27:
            self.giveDamage(players,len(others)*20, -1)
            for o in others:
                players[o].giveHeal(20)
        elif obs==28:
            winsound.PlaySound('sound\\crime.wav', winsound.SND_ASYNC)
            self.moneyTaken(len(others)*30.-1)
            for o in others:
                players[o].giveMoney(30)
        elif obs==29:
            time.sleep(0.3)
            for o in others:
                players[o].effects[2]=0
                players[o].location=self.location
                players[o].character.Move(self.location)
                time.sleep(0.3)
        elif obs==30:
            dist=1000000
            for o in others:
                if abs(players[o].location-self.location)<=dist:
                    dist=abs(players[o].location-self.location)
                    if players[o].location!=self.location: target=o
            if target==-1: return 0
            if not self.isai:
                mb.showinfo(None, "위치교환!")
            died=players[target].nextDmg(players)
            died=self.nextDmg(players)
            if died: return 0
            time.sleep(0.3)
            temp=self.location
            self.location=players[target].location
            obs=self.character.Move(self.location)
            
            players[target].location=temp
            players[target].currobs=30
            players[target].character.Move(temp)
            target=self.turn
            out=2
        elif obs==31:
            if self.isai:
                return 0
            
            targets=[]
            for p in players:
                if self!=p:
                    for m in muststop:
                        if p.location==int(m):
                            break
                    else:
                        targets.append(p)
            if len(targets)==0: 
                if self.isai==False: window.getAlarm('벙위내에 플레이어 없음')
                return 0
        
            skillto=window.skillchoose(targets)
            
            if skillto==0: return 0
            else: target=targets[skillto-1].turn
            out=3
            
            window.getAlarm('이동시킬 칸을 선택하시오')
            
            locaa=-1
            
            drawrange(self.zero(players[target].location-5),players[target].location+5)
            while(True):
                locaa=window.waitgodhand()
                lower=players[target].location-5
                if lower<0: lower=0
                upper=players[target].location+5
                
                if lower<=locaa<=upper: break
                window.getAlarm("이동시킬 칸을 선택하시오")
            players[target].effects[2]=0
            obs=players[target].goto(locaa)
            rangepen.clear()
        elif obs==32:
            self.effects[10]+=1
        elif obs==33:
            self.effects[11]=1
        elif obs==34:
            winsound.PlaySound('sound\\crime.wav', winsound.SND_ASYNC)
            self.moneyTaken(30)
            self.giveDamage(players,30, -1)
        elif obs==35:
            winsound.PlaySound('sound\\crime.wav', winsound.SND_ASYNC)
            if self.lastmoney>0:
                self.moneyTaken(self.lastmoney)
        elif obs==36:
            self.effects[6]=1
        elif obs==37:
            self.Shelter()
        elif obs==38:
            self.effects[7]=1
        elif obs==39:
            self.nextdmg=70
        elif obs==40:
            winsound.PlaySound('sound\\knife.wav', winsound.SND_ASYNC)
            self.giveDamage(players,100, -9)
            
        elif obs==41:
            self.effects[0]=1
            self.effects[2]=1
            winsound.PlaySound('sound\\web.wav', winsound.SND_ASYNC)
        elif obs==42 or obs==59:
            winsound.PlaySound('sound\\explode.wav', winsound.SND_ASYNC)
            self.effects[0]=1
            self.giveDamage(players,30, -6)
        elif obs==43:
            winsound.PlaySound('sound\\explode.wav', winsound.SND_ASYNC)
            self.giveDamage(players,50, -10)
            
        elif obs==44:
            winsound.PlaySound('sound\\explode.wav', winsound.SND_ASYNC)
            self.giveDamage(players,50, -10)
            
            self.effects[0]=1
        elif obs==45:
            winsound.PlaySound('sound\\largeexplode.wav', winsound.SND_ASYNC)
            self.effects[0]=1
            self.giveDamage(players,100, -10)
            
            
        elif obs==47:
            self.effects[8]=9999
            self.setPoison()
        elif obs==48:
            winsound.PlaySound('sound\\largeexplode.wav', winsound.SND_ASYNC)
            self.giveDamage(players,int(self.HP/3), -11)
            
        elif obs==49:
            winsound.PlaySound('sound\\largeexplode.wav', winsound.SND_ASYNC)
            self.giveDamage(players,int((self.MaxHP-self.HP)/2), -11)
            
        elif obs==50:
            
            self.effects[0]=1
            self.effects[2]=1
            self.currobs=45
            self.location=163
            self.character.Move(163)
            self.giveDamage(players,100, -10)
        elif obs==51 or obs==60:
            self.effects[9]=2
            winsound.PlaySound('sound\\explode.wav', winsound.SND_ASYNC)
            self.giveDamage(players,30, -6)
            
        elif obs==52:
            if self.isai:
                if self.HP<200: kidnap='yes'
                else: kidnap='no'
            else:
                kidnap = mb.askquestion ('하나만 고르시오','yes:2턴속박, no:4턴 둔화',icon = 'warning')
            
            if kidnap=='yes':
                self.effects[2]=2
            else:
                self.effects[0]=4
        elif obs==53:
            self.effects[12]=9999
        elif obs==54:
            winsound.PlaySound('sound\\knife.wav', winsound.SND_ASYNC)
            self.giveDamage(players,999999, -1)
        elif obs==55:
            self.effects[2]=2
            self.effects[1]=3
        elif obs==56:
            
            dice=chooseSubway()
            if dice==1:
                if not self.isai:    
                    mb.showinfo(None, "상점으로")
                self.location=29
                self.character.Move(29)
                self.Item()
                return -1
            elif dice==2:
                self.giveMoney(50)
                mb.showinfo(None, "+50 골드!")
            elif dice==3:
                self.moneyTaken(50)
                mb.showinfo(None, "-50 골드!")
            elif dice==4:
                mb.showinfo(None, "사망!")
                self.giveDamage(players,4444, -1)
            elif dice==5: 
                mb.showinfo(None, "2등급 재생의열매 지급")
                self.regen+=10
                self.addMaxhp(40)
            elif dice==6: 
                mb.showinfo(None, "34번칸으로 이동")
                self.location=34
                self.character.Move(34)
        elif obs==57:
            
            dice=chooseCasino()
            if dice==1:
                if not self.isai:
                    mb.showinfo(None, "+100 골드")
                self.giveMoney(100)
            elif dice==2:
                if not self.isai:
                    mb.showinfo(None, "돈 2배")
                self.giveMoney(self.money)
            elif dice==3:
                if not self.isai:
                    mb.showinfo(None, "신속2턴!")
                self.effects[1]=2
            elif dice==4:
                if not self.isai:
                    mb.showinfo(None, "체력 반으로!")
                self.giveDamage(players,9999, -1)
            elif dice==5: 
                if not self.isai:
                    mb.showinfo(None, "돈 절반 몰수")
                self.moneyTaken(int(self.money/2))
            elif dice==6: 
                if not self.isai:
                    mb.showinfo(None, "속박,체력 -50")
                self.effects[2]=1
                self.giveDamage(players,50, -12)
            return -1
        elif obs==64:
            dice=chooseJudge()
            
            winsound.PlaySound('sound\\judgement.wav', winsound.SND_ASYNC)
            if dice==1:
                if not self.isai:
                    mb.showinfo(None, "벌금 100골드")
                self.moneyTaken(100)
            elif dice==2:
                if not self.isai:
                    mb.showinfo(None, "체력 반 깎임, 재심을 기다리시오")
                self.giveDamage(players,int(self.HP/2), -1)
                self.effects[2]=1
            elif dice==3:
                if not self.isai:
                    mb.showinfo(None, "성지순례")
                self.effects[0]=1
                self.effects[2]=1
                self.currobs=45
                self.location=121
                self.character.Move(121)
                self.giveDamage(players,100, -10)
            elif dice==4:
                if not self.isai:
                    mb.showinfo(None, "사형!")
                self.giveDamage(players,4444, -1)
            elif dice==5: 
                if not self.isai:
                    mb.showinfo(None, "모든 플레이어 소환명령")
                for o in others:
                    players[o].effects[2]=0
                    players[o].location=self.location
                    players[o].character.Move(self.location)
                    time.sleep(0.3)
            elif dice==6: 
                if self.isai:
                    if self.effects[12]: slavery='yes'
                    else: slavery='no'
                else:
                    slavery = mb.askquestion ('Choose one','Yes:자신의 노예해방 \n, No:다른 모든 플레이어에게 노예계약',icon = 'warning')
            
                if slavery=='yes':
                    self.effects[12]=0
                    mb.showinfo(None, self.name+" 은(는) 이제 자유입니다")
                else:
                    for o in others:
                        players[o].effects[12]=1
                        mb.showinfo(None, self.name+" 은(는) 이제부터 노예입니다")
        if re!=0:
            for pl in players:                 # projectile
                if pl.turn!=self.turn: 
                    pl.Proj(players,self.turn)
            re=0
            died=False
            if self.id==2 and self.duration[0]>0:
                self.yangiQ(players, self)
                
            window.statusupdate(self.turn, self.champ, self.duration, self.effects)
            
        
        if out>0: return players[target].obstacle(out,players,obs)
        else: return 0
            
        
        
        
        
    def move(self, dice,players):
        
        if self.effects[0] > 0:dice -= 2
        if self.effects[1] > 0: dice += 2 
        self.lastloc=self.location
        
        if self.id==2 and self.isBehind(players):
            dice+=1
            
        self.location += dice
        
        if self.location>=int(muststop[len(muststop)-1]):
            if self.effects[12]>0:
                self.location-=7
                self.giveDamage(players,999999, -13)
            else:
                self.End(players)
        
        
        if self.location < 0: self.location = 0     
        for i in range(len(muststop)):
            if self.lastloc<int(muststop[i])<=self.location:
                self.location=int(muststop[i])
                if self.phase<i+1: 
                    self.addMaxhp(100)
                    window.getAlarm(self.name+'` 최대 체력 증가함')
                self.phase=i+1
        
        
        window.getdice(self.name,dice,self.turn)
        return self.character.Move(self.location)
    
    def End(self,players):
            winsound.PlaySound('sound\\victory.wav', winsound.SND_ASYNC)
            mb.showinfo(None, self.name+" 이(가) 승리했습니다!!")
            others=[]
            reportfmt = '{0:<10} ({1:<2}): {2:<6}|{3:<6}|{4:<6}|{5:<5}|{6:<5}|{7:<5}|{8:<7}|{9:<13}'    
            
            for p in players:
                if p!=self:
                    others.append(p)
                   
            if len(others)==1: 
                second=others[0]
                third=others[0]
            elif others[0].kill>=others[1].kill: 
                second=others[0]
                third=others[1]
            elif others[1].kill>others[0].kill:     
                second=others[1]
                third=others[0]
                
            mb.showinfo(None, "2등:"+second.name)
            mb.showinfo(None, "3등:"+third.name)
            
            myfile=open("stats.txt","a")
            myfile.write("----------------------------------------------------- ------------------------\n")
            myfile.write("1등: "+self.name+"("+self.champ+"), 2등:"+second.name+"("+second.champ+"),3등:"+third.name+"("+third.champ+"),\n")
            
            for p in players:
                myfile.write(p.name+"("+p.champ+")-----------------------------------------------\n")
                myfile.write("킬/데스/어시스트:%d/%d/%d \n"% (p.kill,p.death,p.assist))
                myfile.write("준 피해: %d \n"%p.stats[0])
                myfile.write("받은 피해 :%d \n"%p.stats[1])
                myfile.write("회복량:%d  \n"%p.stats[2])
                myfile.write("번 돈:%d gold \n"%p.stats[4])
                myfile.write("소모한 돈:%d gold\n"%p.stats[5])
                myfile.write("빼앗긴 돈:%d gold\n"%p.stats[6])
                
            myfile.write('이름        턴|공격   |주문   |방어   |마저   |방관   |마관   |재생 |생명력흡수 \n')
            for ps in players:
                myfile.write((reportfmt.format(ps.champ, ps.turn + 1, ps.AD, ps.AP, ps.AR, ps.MR, ps.arP, ps.MP, ps.regen, ps.absorb)+'\n'))

            
            raise Exception
                
                
    def playsound(self):
        rand=random.randint(0,2)
        if self.id==8:
            
            if rand==0:
                winsound.PlaySound('sound\\Jellice\\choose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Jellice\\choose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Jellice\\choose3.wav', winsound.SND_ASYNC)  
        if self.id==9:
            
            if rand==0:
                winsound.PlaySound('sound\\Movingshin\\choose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Movingshin\\choose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Movingshin\\choose3.wav', winsound.SND_ASYNC)  
        if self.id==10:
            
            if rand==0:
                winsound.PlaySound('sound\\Blkx\\choose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Blkx\\choose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Blkx\\choose3.wav', winsound.SND_ASYNC)  
        if self.id==11:
            
            if rand==0:
                winsound.PlaySound('sound\\DrMichin\\choose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\DrMichin\\choose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\DrMichin\\choose3.wav', winsound.SND_ASYNC)  
        if self.id==7:
            
            if rand==0:
                winsound.PlaySound('sound\\Jean\\choose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Jean\\choose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Jean\\choose3.wav', winsound.SND_ASYNC)  
        if self.id==3:
            
            if rand==0:
                winsound.PlaySound('sound\\Gorae\\choose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Gorae\\choose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Gorae\\choose3.wav', winsound.SND_ASYNC)  
        if self.id==1:
            
            if rand==0:
                winsound.PlaySound('sound\\Bird\\choose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Bird\\choose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Bird\\choose3.wav', winsound.SND_ASYNC)  
        if self.id==4:
            
            if rand==0:
                winsound.PlaySound('sound\\Creed\\choose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Creed\\choose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Creed\\choose3.wav', winsound.SND_ASYNC)  
        if self.id==2:
            
            if rand==0:
                winsound.PlaySound('sound\\Yangi\\choose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Yangi\\choose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Yangi\\choose3.wav', winsound.SND_ASYNC)  
        if self.id==5:
            
            
            if rand==0:
                winsound.PlaySound('sound\\Silver\\silverchoose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Silver\\silverchoose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Silver\\silverchoose3.wav', winsound.SND_ASYNC)     
        if self.id==6:
            
            if rand==0:
                winsound.PlaySound('sound\\Timo\\timochoose1.wav', winsound.SND_ASYNC)
            if rand==1:
                winsound.PlaySound('sound\\Timo\\timochoose2.wav', winsound.SND_ASYNC)
            if rand==2:
                winsound.PlaySound('sound\\Timo\\timochoose3.wav', winsound.SND_ASYNC)                            
    
    
    def isBehind(self,players): 
        for p in players:
            if p!=self and self.location<p.location:
                return True
            
    def goto(self,change):
        self.location=change
        return self.character.Move(self.location)
        
    def zero(self, a):
        if a >= 0: return a
        if a < 0: return 0     
        
    
    # set section start
    


    def setProj(self,damage,loc,size):
        self.proj[0]=damage
        self.proj[1]=self.zero(loc)
        self.resetOutbattle()
        
#         if self.id==9 and damage==-1:
#             self.projectile.set(self.proj[1],size)
#             self.proj=[0,-1]
#             return 
        
        self.projectile.set(self.proj[1],size)
        
        

    # set setcion end
    
    # cooldown/reset
    def allCooldown(self,players):
        for i in range(0,3):
            self.cooltime[i]=self.zero(self.cooltime[i]-1)
            
        self.effects[0] = self.zero(self.effects[0] - 1)
        self.effects[1] = self.zero(self.effects[1] - 1)
        self.effects[11] = self.zero(self.effects[11] - 1)
        self.resetPoison()
        if self.effects[10] > 0:
            self.giveMoney(20*self.effects[10])
            window.getAlarm("연금 효과로 %d골드 지급"%(20*self.effects[10]))
        self.Potato(players)
        self.Slave(players)
        
        
        if self.effects[11] == 1: self.loanEnd()
        
        self.mregion = False
        
        if self.damagedby[0] > 0: self.damagedby[0] += 1
  
    
        
    def durCooldown(self,players):
        if self.id==2:
            if self.duration[0]>0: self.giveDamage(players,10,-5)
            
            if self.duration[1]>0: 
                self.giveHeal(int(30+0.5*self.AD+0.2*(self.MaxHP-self.HP)))
                self.effects[2]=1
                self.yangiWspeed+=1
            if self.duration[1]==1:
                window.getAlarm('양이 회복 완료')
                self.effects[2]=0
                self.effects[1]=self.yangiWspeed
                self.duration[1]=0
        elif self.id==3:
            if self.duration[1]==1:
                window.getAlarm('고래 쉴드 끝')
                self.addShield(-1*self.shield)
                self.endW(players)
        elif self.id==5:
            if self.duration[2]==1:
                window.getAlarm('실버 궁 끝')
                self.MR-=self.silveru1
                self.AR-=self.silveru1
                self.silveru1=0
        elif self.id==7:
            if self.duration[2]==1:
                window.getAlarm('진 궁 끝')
                self.cooltime[2]=10
        elif self.id==11:
            if self.Wactive:
                self.giveHeal(8)
            if self.duration[2]>0:
                self.giveHeal(int(self.MaxHP*0.08)+4*int((self.MaxHP-self.HP)/10))
        
        for i in range(0,3):
            self.duration[i]=self.zero(self.duration[i]-1)
        
        window.statusupdate(self.turn, self.champ, self.duration, self.effects)
        
    def otherCooldown(self):
        self.marks[0][0] = self.zero(self.marks[0][0] - 1)
        self.marks[1][0] = self.zero(self.marks[1][0] - 1)
        self.marks[2][0] = self.zero(self.marks[1][0] - 1)
        self.effects[5][0] = self.zero(self.effects[5][0] - 1)
        self.effects[3] = self.zero(self.effects[3] - 1)
        self.effects[4] = self.zero(self.effects[4] - 1)
        self.gacool = self.zero(self.gacool - 1)
        self.regeneration()
        self.adamage = 0
        
        window.statusupdate(self.turn, self.champ, self.duration, self.effects)
        
            # potato,slave
    def resetOutbattle(self):
        self.outbattle = 0

    def resetRealshield(self):
        self.effects[7] = 0

    def resetCooltime(self):
        for i in range(0,3):
            self.cooltime[i]=0
        
    # cooldown,reset end    
    
    # increment,give
    def addOutbattle(self):
        self.outbattle += 1

    def addKill(self, skill):
        self.kill += 1
        self.giveMoney(70)
        
        if self.id == 3 and skill == 3: 
            self.HP += 50
            self.MaxHP += 50
            window.getAlarm('고래의 최대체력이 증가했습니다')
            
        if self.id == 2 and skill == 3:
            self.cooltime[1] = 0
            self.cooltime[2] = 0
            window.getAlarm('양이의 쿨타임이 초기화되었습니다')
        
    def addAssist(self):
        self.assist += 1
        self.giveMoney(50)

    def giveMoney(self, m):
        self.money += m
        if m > 0: 
            window.getAlarm(self.name+'  %d 골드 획득' %m)
            self.lastmoney = m
            self.stats[4]+=m
        else: 
            window.getAlarm(self.name+'%d 골드 소모함' %m)
            self.stats[5]+=-1*m
        window.moneyupdate(self.turn,self.money)

    def moneyTaken(self, m):
        self.money -= m
        window.moneyupdate(self.turn,self.money)
        self.stats[6]+=m
        
    def giveHeal(self, h):
        self.HP += h
        if self.HP > self.MaxHP: self.HP = self.MaxHP
        window.hpupdate(self.turn,self.MaxHP,self.HP,self.shield,True,h)
        self.stats[2]+=h

    def addMaxhp(self, h):
        self.MaxHP += h
        self.HP += h
        if self.id==11 and self.phase>1:
            self.MaxHP-=self.additionalHP
            self.additionalHP=int(self.MaxHP*0.3)
            self.MaxHP+=self.additionalHP
        window.hpupdate(self.turn,self.MaxHP,self.HP,self.shield,True,h)
    
    # increment,give end
    
    # obstacle stuff
    
    def thief(self):
        itemlist=[]
        for i in range(2,15,3):
            if self.items[i]>0:
                itemlist.append(i)
        
        l=[20,26]
        for i in l:
            if self.items[i]>0:
                itemlist.append(i)
                
        if len(itemlist)==0: return 0
        item=random.choice(itemlist)
        self.items[item]-=1
        
        if item==2:
            window.getAlarm(self.name+'이(가) 3등급 검을 도둑맞았습니다!')
            self.AD-=10
        elif item==5:
            window.getAlarm(self.name+' 이(가) 3등급 구슬을 도둑맞았습니다!')
            self.AP-=20
        elif item==8:
            window.getAlarm(self.name+'이(가) 3등급 방패을 도둑맞았습니다!')
            self.AR-=10
            self.MaxHP-=10
        elif item==11:
            window.getAlarm(self.name+'이(가) 3등급 재생의 열매를 도둑맞았습니다!')
            self.regen-=5
        elif item==14:
            window.getAlarm(self.name+'이(가) 3등급 갑옷을 도둑맞았습니다!')
            self.MR-=10
            self.MaxHP-=10
        elif item==20:
            window.getAlarm(self.name+'이(가) 태초의 힘을 도둑맞았습니다!')
            self.skilldmgReduction-=5
        elif item==26:
            window.getAlarm(self.name+'이(가) 초급 마법의 무기를 도둑맞았습니다!')
            self.adStat-=10
            if self.adStatAD:
                self.AD-=10
            else:
                self.AP-=10
        
            
    def Loan(self):
        if self.effects[11] == 0: self.money += 100
        self.effects[11] = 6
        window.moneyupdate(self.turn,self.money)
        
        
    def loanEnd(self):
        self.money -= 100
        if self.money < 0: self.money = 0
        window.getAlarm(self.name+'의 대출금 회수됨')
        window.moneyupdate(self.turn,self.money)
        
    def srCooldown(self):
        self.effects[2] = self.zero(self.effects[2] - 1)
        self.effects[9] = self.zero(self.effects[9] - 1)
        
    def Shelter(self):
        self.giveHeal(70)
        self.effects[7] = 1
        
        self.effects[0] = 0
        self.effects[3] = 0
        self.effects[4] = 0
        self.effects[5] = [0,-1]
        
        self.effects[8] = 0
        self.effects[9] = 0
        window.statusupdate(self.turn, self.champ,self.duration, self.effects)
        
    def setPoison(self):
        self.temp[0] = self.AR
        self.temp[1] = self.MR
        self.AR = self.MR = 0

    def resetPoison(self):
        if (self.temp[0] == 0 and self.temp[1] == 0) == False:
            self.AR += self.temp[0]
            self.MR += self.temp[1]
            self.temp[0] = self.temp[1] = 0

    def Bankrupt(self):
        self.effects[6] = 0
        self.moneyTaken(self.money)

    def Potato(self,players):
        if self.effects[8] > 0: self.giveDamage(players,30, -1)
        
    def Slave(self,players):
        if self.effects[12] > 0: self.giveDamage(players,80, -3)
    
    # obs stuff end
    def nextDmg(self,players):
        died = False
        if self.nextdmg > 0:
            winsound.PlaySound('sound\\explode.wav', winsound.SND_ASYNC)
            died = self.giveDamage(players,self.nextdmg, -4)
            self.nextdmg = 0
            return died

    def regeneration(self):
        if self.regen > 0: 
            self.HP += self.regen
            self.stats[2]+=self.regen
            if self.HP > self.MaxHP: self.HP = self.MaxHP
            window.hpupdate(self.turn,self.MaxHP,self.HP,self.shield,True,self.regen)
            
        if self.outbattle > 8 and self.items[9] > 0 :
            self.HP += int(self.MaxHP * 0.1)
            self.stats[2]+=int(self.MaxHP * 0.1)
            if self.HP > self.MaxHP: self.HP = self.MaxHP
            window.hpupdate(self.turn,self.MaxHP,self.HP,self.shield,True,int(self.MaxHP * 0.1))
            
        
    def Absorb(self):
        self.HP += self.absorb
        if self.HP > self.MaxHP: self.HP = self.MaxHP
        
        if self.absorb>0: 
            self.stats[2]+=self.absorb
            window.hpupdate(self.turn,self.MaxHP,self.HP,self.shield,True,self.absorb)
    def constDamage(self,players):
        
        if self.effects[5][0]>0 and self.effects[5][1]>=0:       #mushroom
            source=self.effects[5][1]
            totaldamage=int(20+0.5*players[source].AP)
            players[source].stats[0]+=totaldamage
            self.effects[0]=1
            died=self.giveDamage(players,totaldamage,source)
            
            
            if self.effects[5][0]==1:
                self.effects[5]=[0,-1]
            if died:
                players[source].addKill(3)
                
                
        if self.id==3 and self.duration[0]>0:           #goraewave
            self.proj.setproj(self.proj.damage,self.proj.location+5,3)
            self.goraeProj(players)        
        
        for p in players: 
            if p.id==2 and p.duration[0]>0 and p.currobs!=0 and self.currobs!=0: self.yangiQ(players,p)    #mover=self
        
        
         
    def yangiQ(self,players,yangi):
        died=False
        if yangi.turn==self.turn:        #mover is yangi
            for p in players:
                if abs(self.location-p.location)<=3 and p.turn != self.turn:
                    pdmg=int(10+0.5*self.AD)
                    window.getAlarm('양이 Q 효과:'+self.name+' hit '+p.name)
                    
                    
                    died=self.skillHit(players, [pdmg,0,self.adamage], self.turn, p.turn, 1)
                    
                    p.resetOutbattle()
                    self.resetOutbattle()
                    if died:
                        self.addKill(1)
#         else:    #mover is not yangi
#             if abs(self.location-yangi.location)<=3:
#                 pdmg=int(10+0.5*yangi.AD)
#                 arP=self.arP
#                 yangi.stats[0]+=(pdmg)
#                 totaldamage=self.totalDamage(pdmg,0,arP,0)
#                 totaldamage+=yangi.adamage
#                 window.getAlarm('양이 Q 효과:' +yangi.name+' hit '+self.name)
#                 winsound.PlaySound('sound\\hit.wav', winsound.SND_ASYNC)
#                 died=self.giveDamage(players,totaldamage,yangi.turn)
#                 yangi.resetOutbattle()
#                 self.resetOutbattle()   
#                 if died:
#                     yangi.addKill(1)
#                     self.Assist(players,self.turn)    
                    
        
    def addShield(self,amt):
        print("shield %d"%amt)
        self.shield+=amt
        if amt<0:
            window.hpupdate(self.turn, self.MaxHP, self.HP, self.shield, False, amt)
        else:
            window.hpupdate(self.turn, self.MaxHP, self.HP, self.shield, True, -1*amt)
    def giveDamage(self, players,damage,skfrom):
        died = False
        for m in muststop:
            if self.location==int(m):
                if damage<4444: return False
            
        if damage==9999: damage=int(self.HP/2)      #카지노 전용
        
        temp = -1
        if self.effects[9] > 0: damage *= 2  # radiation 
        
        if damage <= 1 and skfrom > 0: damage = 1  # minimum damage
        
        if self.id == 6 and self.duration[1] > 0: return False  # timo W
        if self.Invulnerable: return False
        
        
        if self.id == 1 and self.duration[2] > 0: damage=int(damage / 2)  # bird u
        
        if skfrom > -1:  # assist saving
            
            if skfrom != self.damagedby[1]:
                temp = self.damagedby[1]
                self.damagedby[1] = skfrom
                self.damagedby[0] = 1
        
       
        damage-=self.shield
        if damage<=0:
            self.addShield(damage)
            damage=0
        
        
        self.HP -= damage
        if damage<4444:
            self.stats[1]+=damage
        
        if self.id==5: self.passive()
        window.hpupdate(self.turn,self.MaxHP,self.HP,self.shield,False,damage)
        #window.getAlarm(self.name+' health -%d, %d left'%(damage,self.HP))
        
        if self.HP <= 0: 
            if self.items[15] > 0 and self.gacool == 0:
                self.gacool = 10
                self.HP = self.MaxHP / 2
                window.getAlarm('수호 천사 발동!')
                window.hpupdate(self.turn,self.MaxHP,self.HP,self.shield,True,self.MaxHP/2)
                window.statusupdate(self.turn, self.champ, self.duration, self.effects)
            else:
                if skfrom<0:
                    winsound.PlaySound('sound\\execute.wav', winsound.SND_ASYNC)
                
                if skfrom == -1:
                    window.getAlarm((self.name+' 이(가) 처형되었습니다'))
                elif skfrom == -2:
                    window.getAlarm((self.name+'이(가) 독버섯을 먹었습니다'))
                elif skfrom == -3:
                    window.getAlarm((self.name+'이(가) 과로사했습니다'))
                elif skfrom == -4:
                    window.getAlarm((self.name+'이(가) 한시도 가만히 있지를 못했습니다'))
                elif skfrom ==-5:
                    window.getAlarm((self.name+'이(가) 자살했습니다'))
                elif skfrom ==-6:
                    window.getAlarm((self.name+'이(가) 무리한 포탑 다이브로 사망했습니다'))
                elif skfrom==-7:
                    window.getAlarm((self.name+'이(가) 흉기에 찔려 살해당했습니다'))
                elif skfrom==-8:
                    window.getAlarm((self.name+'이(가) 돈의 노예가 되었습니다'))
                elif skfrom==-9:
                    window.getAlarm((self.name+'이(가) 살해당했습니다'))
                elif skfrom==-10:
                    window.getAlarm((self.name+'이(가)  처형당했습니다'))
                elif skfrom==-11:
                    window.getAlarm((self.name+'이(가) 폭파당했습니다'))
                elif skfrom==-12:
                    window.getAlarm((self.name+'이(가) 도박에 중독되었습니다'))
                elif skfrom==-13:
                    window.getAlarm((self.name+'이(가) 죽음으로써 마침내 노예에서 해방되었습니다'))
                else:
                    window.getAlarm((self.name+'이(가) 처치되었습니다'))
                    winsound.PlaySound('sound\\kill.wav', winsound.SND_ASYNC)
                time.sleep(2)
                self.damagedby[1] = temp
                self.HP = self.MaxHP
                window.hpupdate(self.turn,self.MaxHP,self.HP,self.shield,True,self.MaxHP)
                store=-1
                for i in range(len(respawn)-1):
                    if int(respawn[i])<=self.location<int(respawn[i+1]):
                        store=self.character.Move(int(respawn[i]))
                        self.location=int(respawn[i])
                        
                        break
                
                self.resetProjectile()
                
                self.death += 1
                self.nextdmg = 0
                
                died = True
                if store==0:
                    self.Item()
                
                for i in range(0,len(self.effects)):
                    self.effects[i]=0
                self.effects[5]=[0,-1]
                for i in range(0,3):
                    self.duration[i]=0
                self.Invulnerable=True
                self.Assist(players, skfrom)
        return died 
    
    def totalDamage(self, source,Pdamage, Mdamage, arP, MP):
        totaldamage = 0
        
        Mdamage+=int(0.01*source.addMdmg*self.HP)
        
        if arP <= self.AR:  # arP<=AR
            if Pdamage - (self.AR - arP) > 0:
                totaldamage += (Pdamage - (self.AR - arP))
        else:
            totaldamage += Pdamage  # arP>AR

        if (MP <= self.MR): 
            if Mdamage - (self.MR - MP) > 0:
                totaldamage += (Mdamage - (self.MR - MP))
        else:
            totaldamage += Mdamage

        return totaldamage;
    
    @staticmethod
    def skillHit(p, damage, skfrom, to, skill):
       
        p[to].resetOutbattle()
        
        
        if p[to].id == 6 and p[to].duration[1]:  return False  # timo w
           
        if p[to].effects[7]: 
            p[to].resetRealshield()
            return False  # realshield
        
        if p[skfrom].id == 6 and skill == 1: p[to].effects[3] += 2  # timo q
        
        if p[skfrom].id == 5 and skill == 2: 
            p[to].marks[0][0] = 3          # silver w
            p[to].marks[0][1]=skfrom+1
            window.getAlarm((p[to].name+'이(가) 실버 인장을 받았습니다'))
            return False
        
        if p[skfrom].id == 5 and skill == 1 and skfrom+1==p[to].marks[0][1]:  # silver q
            damage[2] += 30
            window.getAlarm(('추가 피해:30'))
            p[to].marks[0] = [0,0]
        
        if p[skfrom].id == 7 and skill == 1 and p[to].marks[1][0] > 0 and skfrom+1==p[to].marks[1][1]:  # jean q
            p[to].effects[2] += 1
            p[to].marks[1] = [0,0]
            
            
        if p[skfrom].id == 7 and skill == 3:  # jean u
            p[to].effects[0] += 1

        totaldamage = p[to].totalDamage(p[skfrom],damage[0], damage[1], p[skfrom].arP, p[skfrom].MP)
        
                                                            #skilldmgReduction
        totaldamage-=totaldamage*p[to].skilldmgReduction*0.01
        
        
        if p[to].id == 6 and p[skfrom].effects[5][0] > 0 and p[skfrom].effects[5][1]>=0 and p[skfrom].effects[5][1] > p[to].turn: totaldamage /= 2  # timo u
        
        totaldamage += damage[2]  # fdamage
        
        if p[skfrom].id==9 and skill==2: 
            p[skfrom].giveHeal(int(totaldamage/2))               #movingshin w
        
        
        
        winsound.PlaySound('sound\\hit.wav', winsound.SND_ASYNC)
        died = p[to].giveDamage(p,totaldamage, skfrom)

        return died
        
    def Assist(self, p, skfrom):
        if (0 < self.damagedby[0] < 3) and self.damagedby[1]>=0 and (skfrom != self.damagedby[1]) and self!=self.damagedby[1]:  # assist
            p[self.damagedby[1]].addAssist()
            self.damagedby[0] = 0
            print('어시스트!%d %d'%(self.damagedby[1],skfrom))
            
#     def recAIstore(self,itemwant,temitemlist,toremove):        
            
            
            
            
    
    def AIstore(self):
        while(self.money>=30):                         # 돈이 30원 미만일시 자동 아웃
            Itemwant=self.itemtree[self.itemtree[0]+1]
#             getitem=False
#             self.recAIstore(itemwant)
            
            
            
            
            
            
            
            while(True):                               #아이템 못얻은 동안은 계속돌림
                price = 0;
                remove2 = 0;
                remove3 = 0;
                remove4 = 0;
                remove5 = 0;
                zero=False
                
                if Itemwant==0:
                    price=300
                    if self.items[1]>1:
                        price-=160
                        remove2=2
                    elif self.items[1]==0 and self.items[2]>4:
                        price-=120
                        remove3=4
                    elif self.items[1]==1 and self.items[2]>2:
                        price-=140
                        remove2=1
                        remove3=2
                    else:
                        price -= (80 * self.items[1] + 30 * self.items[2])
                        zero=True
                        
                    if price>self.money:     #1등급 살 돈이 안됨
                        if self.items[1]>=2: return        #3등급검 2개이상 보유시 아무것도 안사고 2등급검  돈 될때까지 기다림
                        
                        price=80                         #2등급검 구입 시도
                        if self.items[2]>1:
                            price-=60
                            remove3=2
                        elif self.items[2]==1:
                            price-=30*self.items[2]
                            remove3=1
                        if price>self.money:               #2등급검 살돈도 없고 3등급검 2개이상 보유하지 않았을때
                            if self.items[2]>=2: return        #3등급검 2개이상 보유시 아무것도 안사고 2등급검  돈 될때까지 기다림
                            
                            price=30                         #3등급 구입시도
                            if price>self.money:  
                                return                        #3등급도 못사면 나감
                            else:
                                self.items[2]+=1
                                self.giveMoney(-1*price)
                                self.AD+=10
                                window.getAlarm(self.name+"bought 3rd sword")
                            
                            
                        else:            #2등급 살돈 됨
                            self.items[1]+=1
                            self.items[2]-=remove3
                            self.giveMoney(-1*price)
                            self.AD+=30
                            window.getAlarm(self.name+"bought 2nd sword")
                        
                    else:              #1등급 살 돈이 될때
                        self.items[0]+=1
                        self.items[1]-=remove2
                        self.items[2]-=remove3
                        if zero: self.items[1]=self.items[2]=0
                        
                        self.giveMoney(price*-1)
                        self.AD+=80
                        self.arP+=20
                        window.getAlarm(self.name+"bought 1st sword")
                        if self.itemtree[0]<len(self.itemtree)-2: self.itemtree[0]+=1
                        break
        
                if Itemwant==3:                    #marble
                    price=320
                    if self.items[4]>1:
                        price-=240
                        remove2=2
                    elif self.items[4]==0 and self.items[5]>4:
                        price-=160
                        remove3=4
                    elif self.items[4]==1 and self.items[5]>2:
                        price-=200
                        remove2=1
                        remove3=2
                    else:
                        price -= (120 * self.items[4] + 40 * self.items[5])
                        zero=True
                        
                    if price>self.money:     #1등급 살 돈이 안됨
                        if self.items[4]>=2: return        #2등급 2개이상 보유시 아무것도 안사고 2등급검  돈 될때까지 기다림
                        
                        price=120                         #2등급검 구입 시도
                        if self.items[5]>1:
                            price-=80
                            remove3=2
                        elif self.items[5]==1:
                            price-=40*self.items[5]
                            remove3=1
                        if price>self.money:               #2등급 살돈도 없고 3등급검 2개이상 보유하지 않았을때
                            if self.items[5]>=2: return        #3등급 2개이상 보유시 아무것도 안사고 2등급검  돈 될때까지 기다림
                            
                            price=40                         #3등급 구입시도
                            if price>self.money:  
                                return                        #3등급도 못사면 나감
                            else:
                                self.items[5]+=1
                                self.giveMoney(-1*price)
                                self.AP+=20
                                window.getAlarm(self.name+"bought 3rd marble")
                            
                            
                        else:            #2등급 살돈 됨
                            self.items[4]+=1
                            self.items[5]-=remove3
                            self.giveMoney(-1*price)
                            self.AP+=50
                            window.getAlarm(self.name+"bought 2nd marble")
                        
                    else:              #1등급 살 돈이 될때
                        self.items[3]+=1
                        self.items[4]-=remove2
                        self.items[5]-=remove3
                        if zero: self.items[4]=self.items[5]=0
                        
                        self.giveMoney(price*-1)
                        self.AP+=120
                        
                        window.getAlarm(self.name+"bought 1st marble")
                        if self.itemtree[0]<len(self.itemtree)-2: self.itemtree[0]+=1
                        break    
                if Itemwant==9:                    #fruit
                    price=400
                    if self.items[10]>1:
                        price-=240
                        remove2=2
                    elif self.items[10]==0 and self.items[11]>4:
                        price-=160
                        remove3=4
                    elif self.items[10]==1 and self.items[11]>2:
                        price-=200
                        remove2=1
                        remove3=2
                    else:
                        price -= (120 * self.items[10] + 40 * self.items[11])
                        zero=True
                        
                    if price>self.money:     #1등급 살 돈이 안됨
                        if self.items[10]>=2: return        #2등급 2개이상 보유시 아무것도 안사고 2등급검  돈 될때까지 기다림
                        
                        price=120                         #2등급검 구입 시도
                        if self.items[11]>1:
                            price-=80
                            remove3=2
                        elif self.items[11]==1:
                            price-=40*self.items[11]
                            remove3=1
                        if price>self.money:               #2등급 살돈도 없고 3등급검 2개이상 보유하지 않았을때
                            if self.items[11]>=2: return        #3등급 2개이상 보유시 아무것도 안사고 2등급검  돈 될때까지 기다림
                            
                            price=40                         #3등급 구입시도
                            if price>self.money:  
                                return                        #3등급도 못사면 나감
                            else:
                                self.items[11]+=1
                                self.giveMoney(-1*price)
                                self.regen+=10
                                window.getAlarm(self.name+"bought 3rd fruit")
                            
                            
                        else:            #2등급 살돈 됨
                            self.items[10]+=1
                            self.items[11]-=remove3
                            self.giveMoney(-1*price)
                            self.regen+=10
                            self.addMaxhp(40)
                            window.getAlarm(self.name+"bought 2nd fruit")
                        
                    else:              #1등급 살 돈이 될때
                        self.items[9]+=1
                        self.items[10]-=remove2
                        self.items[11]-=remove3
                        if zero: self.items[10]=self.items[11]=0
                        
                        self.giveMoney(price*-1)
                        self.regen+=30
                        self.addMaxhp(100)
                        
                        window.getAlarm(self.name+"bought 1st fruit")
                        if self.itemtree[0]<len(self.itemtree)-2: self.itemtree[0]+=1
                        break    
                    
    def calcPrice(self,tobuy,tempitemlist,toremove):
        if tobuy.child1==None:
            return 0

        if tempitemlist[tobuy.child1.id]==0:
            discount1=self.calcPrice(tobuy.child1,tempitemlist,toremove)
        else:
            discount1=tobuy.child1.price
            toremove.append(tobuy.child1.id)
            tempitemlist[tobuy.child1.id]-=1
        
        if  tempitemlist[tobuy.child2.id]==0:
            discount2=self.calcPrice(tobuy.child2,tempitemlist,toremove) 
        else:
            discount2=tobuy.child2.price  
            toremove.append(tobuy.child2.id)
            tempitemlist[tobuy.child2.id]-=1
            
        return discount1+discount2
                    
    def Item(self):
        if self.isai:
            self.AIstore()
            return
        self.effects[6]=0
        self.effects[10]=0
        while(self.money>=30):
            winsound.PlaySound('sound\\store.wav', winsound.SND_ASYNC)
            Item=window.itemchoose((self.name+' ('+self.champ+'), 남은 골드:%d'%self.money),self.items)-1
            if Item<0: break
            tobuy=allItem[Item]
            toremove=[]
            tempitemlist=[]
            for i in self.items:
                tempitemlist.append(i)
            
            price=tobuy.price-self.calcPrice(tobuy,tempitemlist,toremove)
            
            if price<=self.money: 
                self.giveMoney(price*-1)
                for a in tobuy.ability:
                    if a.id==0:
                        self.addMaxhp(a.value)
                    elif a.id==1:
                        self.AD +=a.value
                        if self.AD>self.AP and self.adStat>0 and not self.adStatAD:
                            self.AP-=self.adStat
                            self.AD+=self.adStat
                            self.adStatAD=True
                    elif a.id==2:
                        self.AP +=a.value
                        if self.AD<self.AP and self.adStat>0 and self.adStatAD:
                            self.AD-=self.adStat
                            self.AP+=self.adStat
                            self.adStatAD=False
                    elif a.id==3:
                        self.AR +=a.value
                    elif a.id==4:
                        self.MR +=a.value
                    elif a.id==5:
                        self.arP +=a.value
                    elif a.id==6:
                        self.MP +=a.value
                    elif a.id==7:
                        self.absorb +=a.value
                    elif a.id==8:
                        self.regen +=a.value
                    elif a.id==9:
                        self.adStat+=a.value
                        if self.AD>=self.AP:
                            self.AD+=self.adStat
                            self.adStatAD=True
                        else:
                            self.AP+=self.adStat
                            self.adStatAD=False
                    elif a.id==10:
                        self.basicattackRange+=a.value
                    elif a.id==11:
                        self.addMdmg+=a.value
                    elif a.id==12:
                        if self.skilldmgReduction+a.value<=50:
                            self.skilldmgReduction+=a.value
                            
                for r in toremove:
                    self.items[r]-=1;
                
                self.items[Item]+=1
                #mb.showinfo(None, "%s 구매"%tobuy.name)
        
       
            
    def AIproj(self,front,back,players):
        if self.adamage==30:
            front*=3
            back*=3
        lower=self.location-back    
        if lower<0: lower=0
        upper=self.location+front         
        if upper>int(muststop[len(muststop)-1]): upper=int(muststop[len(muststop)-1])
        
        target=self
        for i in range(lower-3,upper):   #범위 뒤에있는 플레이어도 맞을 수 있음,범위 끝에 있는 플레이어는 맞을확율 낮음
            for p in players:
                if p.location==i and p!=self:
                    if p.effects[2]>0: 
                        return [True,p.location]
                    
                    target=p
            
        if target!=self: return [True,target.location+1]
                
        return 0
        
            
    def testProj(self,front,back):
        if self.adamage==30:
            front*=3
            back*=3
        locaa=window.waitproj()
        if locaa==-1:
            return 0
        lower=self.location-back
        if lower<0: lower=0
        upper=self.location+front
        
        return [lower<=locaa<=upper,locaa]
        
        
    def projCheck(self,p,skillfrom,skillto,pr):
        
        r=False
        upperloc=pr.location+(pr.size-1)
        for i in range(len(muststop)):
                if p[skillto].location==int(muststop[i]):
                    return False
        
        if pr.location<=p[skillto].location <=upperloc:
            if p[skillto].effects[7]==1: 
                p[skillto].effects[7]=0
            elif p[skillto].id==6 and p[skillto].duration[1]>1:
                print('timo w')
            else:
                r=True
        
        return r
        
    def hitbasicAttack(self,players,target):    
        pdmg=self.AD+10
        arP=self.arP
        mdmg=0
        MP=0
        died=False
        self.Absorb()
        
        if(self.id==1):                  #버드 스킬
            if self.duration[2]>0:
                pdmg=int(1.5*self.AD+10)
            if self.duration[1]>0:
                mdmg=int(10+0.5*self.AP)
                MP=self.MP
        self.stats[0]+=(pdmg+mdmg)
        if self.items[18]>0:         #살의의채찍
            mdmg+=int((self.adStat)*0.3)
        totaldamage=target.totalDamage(self,pdmg,mdmg,arP,MP)
        if self.adamage==20: totaldamage+=20
        
        if self.effects[3]==0:
            window.getAlarm(self.name+' hit '+target.name)
            winsound.PlaySound('sound\\normalhit.wav', winsound.SND_ASYNC)
            died=target.giveDamage(players,totaldamage,self.turn)
            self.resetOutbattle()
            target.resetOutbattle()
        if died:
            self.addKill(0)
        return died
    
    def basicAttack(self,players):
        range=self.basicattackRange
        died=False
       
        if self.id==1 and self.duration[2]>0 and range<3:     #버드궁
            range=3
        
        
        for p in players:
            if abs(self.location-p.location)<=range and p.turn != self.turn:
                died=self.hitbasicAttack(players, p)
                if not died and  p.effects[3]==0 and p.location==self.location and p.turn!=self.turn:
                    died=p.hitbasicAttack(players, self)
                    if died:
                        p.addKill(0)
        return died
    def multitarget(self,players,lower,upper,skill):
        targets=[]
        
        for p in players:
            if lower<=p.location<=upper and self!=p:
                for m in muststop:
                    if p.location==int(m):
                        break
                else:
                    targets.append(p.turn)
        if len(targets)==0: 
            window.getAlarm('범위내에 플레이어 없음')
            return None
            
        return targets
        
    def hitoneTarget(self,index,players,output,skillfrom,skill):
        wn.update()
        skillto = output[3][index]
        # 0.pdmg    1.mdmg    2.fdmg    3.skillto
         
        self.resetOutbattle()
                        
        
        output[2] += self.adamage
        
        window.getAlarm('물리피해:%d, 마법피해: %d, 고정피해:%d' %( output[0], output[1], output[2]))
        
        damage = [output[0], output[1], output[2]]
        
        self.stats[0]+=(output[0]+output[1]+output[2])
        
        died = players[skillto].skillHit(players, damage, skillfrom, skillto, skill)
        wn.update()
        if died: self.addKill(skill)
        
        
    def choosetarget(self,players,range,skill):
        targets=[]
        if self.adamage==30:
            range*=3
            
        for p in players:
            if abs(self.location-p.location)<=range and self!=p:
                for m in muststop:
                    if p.location==int(m):
                        break
                else:
                    targets.append(p)
            elif abs(self.location-p.location)<=range+5 and p.marks[0][1]==self.turn+1 and skill==1:   #silver q range increase by 5
                for m in muststop:
                    if p.location==int(m):
                        break
                else:
                    targets.append(p)
                
        if len(targets)==0: 
            window.getAlarm('범위내에 플레이어 없음')
            return -1
        
        
        if self.isai:
            hp=10000
            num=0
            
                
            
            for t in targets:
                if t.HP<hp:
                    skillto=num
                num+=1
                
            return targets[skillto].turn
                    
            
        else:
            skillto=window.skillchoose(targets)
            if skillto==0: return -1
            else: return targets[skillto-1].turn
                    
    
    def isbehindof(self,target):
        if self.location>target.location:
            return False
        else: return True
    
    
from tkinter import *


def chooseSubway():
    subway.deiconify()
    subway.overrideredirect(True)
    winsound.PlaySound('sound\\random.wav', winsound.SND_ASYNC)
    for i in range(30):
        d=random.randint(1,6)
        dicel['text']=d
        subway.update()
        time.sleep(0.1)
    for i in range(5):
        d=random.randint(1,6)
        dicel['text']=d
        subway.update()
        time.sleep(0.4)
    time.sleep(0.5)
    subway.withdraw()
    return d
    
subway = Tk()
subway.title("지하철")

label=Label(subway, text=""" 1.상점으로 \n2.  -50 골드\n3. +50 골드\n4. 사망\n5. 2등급 재생의 열매 지급\n6. 34번칸으로""",fg="black",font="none 13")

label.grid(column=0,row=0,sticky=W)

dicel=Label(subway,text="5",fg="black",font= "none 40 bold")
dicel.grid(column=1,row=0,sticky=N)


def chooseCasino():
    casino.deiconify()
    winsound.PlaySound('sound\\random.wav', winsound.SND_ASYNC)
    for i in range(30):
        di=random.randint(1,6)
        cdicel['text']=di
        casino.update()
        time.sleep(0.1)
    for i in range(5):
        di=random.randint(1,6)
        cdicel['text']=di
        casino.update()
        time.sleep(0.4)
    time.sleep(0.5)
    casino.withdraw()
    return di
    
casino = Tk()
casino.title("카지노")
casino.configure(background="#ffb20c")
clabel=Label(casino, text=""" 1.+100 골드 \n2.  골드 x2\n3. 2턴 신속\n4. 체력 절반으로\n5.돈 절반 몰수 \n6. 속박, 체력-50""",fg="black",bg="#ffb20c",font="none 13")

clabel.grid(column=0,row=0,sticky=W)

cdicel=Label(casino,text="5",fg="black",bg="#ffb20c",font= "none 40 bold")
cdicel.grid(column=1,row=0,sticky=N)

def chooseJudge():
    judge.deiconify()
    winsound.PlaySound('sound\\random.wav', winsound.SND_ASYNC)
    for i in range(30):
        di=random.randint(1,6)
        jdicel['text']=di
        judge.update()
        time.sleep(0.1)
    for i in range(5):
        di=random.randint(1,6)
        jdicel['text']=di
        judge.update()
        time.sleep(0.4)
    time.sleep(0.5)
    judge.withdraw()
    return di
    
judge = Tk()
judge.title("인민 재판")
judge.configure(background="red")
Jlabel=Label(judge,text="인민 재판",fg="yellow",bg="red",font="none 20 bold")
jlabel=Label(judge, text=""" 1.-100 골드 \n2.  속박, 체력 1/2\n3. 성지 순례!!\n4. 사형 선고 \n5.모든 플레이어 소환\n6. 2개 옵션중 선택""",fg="black",bg="red",font="none 13")
Jlabel.grid(column=0,row=0,sticky=W)
jlabel.grid(column=0,row=1,sticky=W)

jdicel=Label(judge,text="5",fg="black",font= "none 40 bold")
jdicel.grid(column=1,row=0,sticky=N)
    
