#-*- coding: ms949 -*-
from tkinter import *
from tkinter import ttk
from tkinter import tix
from tkinter.constants import *
from board import *
import time
import random
import winsound
skill = -1
dice = 0
projlaunch=0
skillto=-1

def close_window():
    window.destroy()
def passturn(name):
    global dicelabel
    skipbtn.grid(row=14, column=0, sticky=N)
    qbtn.grid(row=14, column=1, sticky=N)
    wbtn.grid(row=14, column=2, sticky=N)
    ubtn.grid(row=14, column=3, sticky=N)
    dicelabel['text']=(name,'�ӹ�')
    window.update()
    
def getdice(name, dice,num):
    global dicelabel
    dicelabel.grid_forget()
    if num==0:
        dicelabel = Label(window, text=(name, "dice:", dice),fg="blue", bg="#baffde", font="none 20")
    elif num==1:
        dicelabel = Label(window, text=(name, "dice:", dice),fg="red", bg="#baffde", font="none 20")
    elif num==2:
        dicelabel = Label(window, text=(name, "dice:", dice),fg="green", bg="#baffde", font="none 20")
    elif num==3:
        dicelabel = Label(window, text=(name, "dice:", dice),fg="purple", bg="#baffde", font="none 20")
                          
                          
    dicelabel.grid(row=13, column=0, columnspan=7, sticky=W)
    skipbtn.grid(row=14, column=0, sticky=N)
    qbtn.grid(row=14, column=1, sticky=N)
    wbtn.grid(row=14, column=2, sticky=N)
    ubtn.grid(row=14, column=3, sticky=N)
    window.update()

    
def hpupdate(num, ma, hp,shield,increase,value):
    global pb
    global Hlabel
    global indicatelabel
    pb[num]['value'] = hp
    pb[num]['maximum'] = ma
    if ma>600: pb[num]['length'] = 600
    else: pb[num]['length'] = ma
    if shield==0:
        Hlabel[num]['text']=(ma, "/", hp)
    else:
        Hlabel[num]['text']=(ma, "/", hp,"+",shield)
    
    if 3*(float(hp)/float(ma))>2:
        Hlabel[num]['bg']='lime'
    elif 3*(float(hp)/float(ma))>1:
        Hlabel[num]['bg']='yellow'
    elif 3*(float(hp)/float(ma))<1:
        Hlabel[num]['bg']='red'
    
    if value<0:
        if increase:
            indicatelabel[num]['fg']='lightgray'
            indicatelabel[num]['text']=('+',-1*value)
        else:
            indicatelabel[num]['fg']='lightgray'
            indicatelabel[num]['text']=('-',-1*value)
        indicatelabel[num].grid(row=(num+1)*3, column=2, sticky=N)
        window.update()
        time.sleep(0.4)
        indicatelabel[num].grid_forget()
        return;
    
    if increase:
        indicatelabel[num]['fg']='green'
        indicatelabel[num]['text']=('+',value)
    else:
        indicatelabel[num]['fg']='red'
        indicatelabel[num]['text']=('-',value)
    indicatelabel[num].grid(row=(num+1)*3, column=2, sticky=N)
    window.update()
    time.sleep(0.55)
    indicatelabel[num].grid_forget()
    window.update()
    
def moneyupdate(num,money):
    global Mlabel
    Mlabel[num]['text']=("money:",money)
    
def statusupdate(num,champion,dur,effects):
    
    global label
    label[num]['text']=('player',num+1,"(",champion,")")
    if dur[2]!=0:
        label[num]['text']+="[U]"
    if dur[1]!=0:
        label[num]['text']+="[W]"
    if dur[0]!=0:
        label[num]['text']+="[Q]"
    if effects[12]!=0:
        label[num]['text']+="[�뿹���]"
    if effects[9]!=0:
        label[num]['text']+="[����]"
    if effects[8]!=0:
        label[num]['text']+="[��]"
    if effects[7]!=0:
        label[num]['text']+="[��]"
    if effects[5][0]!=0:
        label[num]['text']+="[Ƽ�� ����]"
    if effects[4]!=0:
        label[num]['text']+="[ħ��]"
    if effects[3]!=0:
        label[num]['text']+="[�Ǹ�]"
    if effects[2]!=0:
        label[num]['text']+="[�ӹ�]"
    if effects[1]!=0:
        label[num]['text']+="[�ż�]"
    if effects[0]!=0:
        label[num]['text']+="[��ȭ]"
   
    
def getReport(reports):
    global report
    
    report.insert(END, reports)
    
    
def reportReset():
    global report
    report.delete(0.0,END)

def getAlarm(alarms):
    global alarm
    alarms=str(alarms)
    alarm.insert(END, alarms)
    alarm.insert(END,'\n')
    
def alarmReset():
    global alarm
    alarm.delete(0.0,END)
    
def skip():
    global skill
    global projlaunch
    skipbtn.grid_forget()
    projlaunch=0
    qbtn.grid_forget()
    wbtn.grid_forget()
    ubtn.grid_forget()
    skill = 0
    window.update()

    
def useq():
    global skill
    skill = 1
    

def usew():
    global skill
    skill = 2

def useu():
    global skill
    skill = 3
def skillp1():
    global skillto
    skillto=1
def skillp2():
    global skillto
    skillto=2
def skillp3():
    global skillto
    skillto=3
def cancel():
    global skillto
    skillto=0
def cancelproj():
    global projlaunch
    projlaunch=-1
def launched():
    global projlaunch
    projlaunch=1
def buttonupdate(cooltime):
    if cooltime[0]==0:
        qbtn["background"]="#499eff"
    else:
        qbtn["background"]="gray"
    if cooltime[1]==0:
        wbtn["background"]="#499eff"
    else:
        wbtn["background"]="gray"
    if cooltime[2]==0:
        ubtn["background"]="#499eff"
    else:
        ubtn["background"]="gray"
    
    window.update()


def skillupdate(tooltips):
    global skill
    window.lift()
    bal.bind_widget(qbtn,balloonmsg=tooltips[0])    
    bal.bind_widget(wbtn,balloonmsg=tooltips[1])    
    bal.bind_widget(ubtn,balloonmsg=tooltips[2])    
    
    
    
    while(True):
        window.update()
        window.update_idletasks()
        if skill != -1:
            sk = skill
            skill = -1
            return sk
        
def skillchoose(opponents):
    global skillto
    chooselabel.grid(row=15, column=0, columnspan=7, sticky=W)
    choosebtn1.grid(row=16, column=0, sticky=W)
    choosebtn1['text']=(opponents[0].name,"(",opponents[0].champ,")")
    cancelbtn.grid(row=16, column=3, sticky=W)
    
    
    
    if len(opponents)==2: 
        choosebtn2.grid(row=16, column=1, sticky=W)
        choosebtn2['text']=(opponents[1].name,"(",opponents[1].champ,")")
    
    if len(opponents)==3:
        choosebtn2.grid(row=16, column=1, sticky=W)
        choosebtn2['text']=(opponents[1].name,"(",opponents[1].champ,")")
        
        choosebtn3.grid(row=16, column=2,sticky=W)
        choosebtn3['text']=(opponents[2].name,"(",opponents[2].champ,")")
        
    while(True):
        window.update()
        window.update_idletasks()
        if skillto != -1:
            sk = skillto
            skillto = -1
            chooselabel.grid_forget()
            choosebtn1.grid_forget()
            choosebtn2.grid_forget()
            choosebtn3.grid_forget()
            cancelbtn.grid_forget()
            return sk
        
def waitproj():
    loca=-1
    pbtn.grid(row=15, column=7, sticky=W)
    cbtn.grid(row=15, column=8, sticky=W)
    global projlaunch
    while projlaunch==0:
        window.update()
        time.sleep(0.1)
        window.update()
        if projlaunch==1: 
            loca=getloc()
            pbtn.grid_forget()
            cbtn.grid_forget()
            projlaunch=0
            window.lift()
            return loca
        elif projlaunch==-1:
            projlaunch=0
            cbtn.grid_forget()
            pbtn.grid_forget()
            rangepen.clear()
            return -1
def waitgodhand():
    loca=-1
    gbtn.grid(row=15, column=7, sticky=W)

    global projlaunch
    while projlaunch==0:
        window.update()
        time.sleep(0.1)
        window.update()
        if projlaunch==1: 
            loca=getloc()
            gbtn.grid_forget()
            projlaunch=0
            window.lift()
            return loca
    
    

window = tix.Tk()

window.configure(background="#baffde")

label = []
pb = []
Hlabel = []
Mlabel = []
indicatelabel=[]
choosebtn=[]
skillbtn=[]
c = 0  
bal=tix.Balloon(window)
PNUM=3

for i in range(1,PNUM*3+1 , 3):
    
    if c == 0:
        label.append(Label(window, text=("player",c+1),fg="blue", bg="#baffde", font="none 10"))
        pb.append(ttk.Progressbar(window, style="Horizontal.TProgressbar", orient='horizontal', length=200,mode='determinate', maximum=200, value=200))
    elif c == 1: 
        label.append(Label(window, text=("player",c+1),fg="red", bg="#baffde", font="none 10"))
        pb.append(ttk.Progressbar(window, style="Horizontal.TProgressbar", orient='horizontal', length=200, mode='determinate', maximum=200, value=200))
    elif c == 2:
        label.append(Label(window, text=("player",c+1),fg="green", bg="#baffde", font="none 10"))
        pb.append(ttk.Progressbar(window, style="Horizontal.TProgressbar", orient='horizontal', length=200, mode='determinate', maximum=200, value=200))
    elif c == 3:
        label.append(Label(window, text=("player",c+1),fg="purple", bg="#baffde", font="none 10"))
        pb.append(ttk.Progressbar(window, style="Horizontal.TProgressbar", orient='horizontal', length=200, mode='determinate', maximum=200, value=200))
    
    label[c].grid(row=i, column=0, columnspan=7, sticky=W)
    pb[c].grid(row=i + 2, column=0, columnspan=7, sticky=W)
    Mlabel.append(Label(window, text=("money:0"),fg="black", bg="#baffde", font="none 10"))
    Mlabel[c].grid(row=i + 1, column=0, columnspan=3, sticky=W)
    Hlabel.append(Label(window, text=(pb[c]["maximum"], "/", pb[c]["value"]), bg='lime',fg="black", font="none 10"))
    Hlabel[c].grid(row=i + 1, column=3, columnspan=4, sticky=W)
    indicatelabel.append(Label(window, text=(""), fg="red",font="none 12 bold"))
    indicatelabel[c].grid(row=i+2, column=2, sticky=N)
    indicatelabel[c].grid_forget()

    c += 1

dicelabel = Label(window, text=("player1 dice:6"),fg="black", bg="#baffde", font="none 20")
dicelabel.grid(row=13, column=0, columnspan=7, sticky=W)
skipbtn = Button(window, text="next turn", width=6, height=3, command=skip,background="#499eff")
skipbtn.grid(row=14, column=0, sticky=N)
qbtn = Button(window, text="Q", width=6, height=3, command=useq,background="#499eff")
qbtn.grid(row=14, column=1, sticky=N)
wbtn = Button(window, text="W", width=6, height=3, command=usew,background="#499eff")
wbtn.grid(row=14, column=2, sticky=N)
ubtn = Button(window, text="U", width=6, height=3, command=useu,background="#499eff")
ubtn.grid(row=14, column=3, sticky=N)




skilllabel = Label(window, text=("player1 dice:6"), fg="#baffde", font="none 20")
skilllabel.grid(row=13, column=0, columnspan=7, sticky=W)
pbtn = Button(window, text="Location selected", width=12, height=3, command=launched,background="#499eff")
pbtn.grid(row=14, column=7, sticky=W)
pbtn.grid_forget()

gbtn = Button(window, text="godhand selected", width=15, height=3, command=launched,background="#499eff")
gbtn.grid(row=14, column=7, sticky=W)
gbtn.grid_forget()

cbtn = Button(window, text="cancel", width=15, height=3, command=cancelproj,background="#499eff")
cbtn.grid(row=14, column=8, sticky=W)
cbtn.grid_forget()

chooselabel=Label(window, text=("�÷��̾� ����"), fg="black",bg="#baffde", font="none 16")
chooselabel.grid(row=15, column=0, columnspan=7, sticky=W)
chooselabel.grid_forget()


choosebtn1=Button(window, text=("player",1), width=18, height=3,command=skillp1,background="#499eff")
choosebtn1.grid(row=13, column=0, columnspan=3, sticky=W)
choosebtn1.grid_forget()
choosebtn2=Button(window, text=("player",1), width=18, height=3,command=skillp2,background="#499eff")
choosebtn2.grid(row=13, column=3,columnspan=3 , sticky=W)
choosebtn2.grid_forget()
choosebtn3=Button(window, text=("player",1), width=18, height=3,command=skillp3,background="#499eff")
choosebtn3.grid(row=13, column=6,columnspan=3 , sticky=W)
choosebtn3.grid_forget()
cancelbtn=Button(window, text=("���"), width=8, height=3, command=cancel,background="#499eff")
cancelbtn.grid(row=13, column=10, sticky=W)
cancelbtn.grid_forget()



# reportlabel = Label(window, text=("����Ʈ"), fg="black",bg="#baffde", font="none 12").grid(row=0, column=0, sticky=N)
report = Text(window, width=80, height=14, wrap=WORD,background="#fff9c9")
report.grid(row=17, column=0,columnspan=9, sticky=W)

alarm = Text(window, width=40, height=20, background="#fff9c9")
alarm.grid(row=1, column=7,rowspan=12,columnspan=2, sticky=E)

dicenum=0

def choosedice(name):
    global dicenum
    dicebtn["text"]=(name," �ֻ��� ������")
    dicewin.deiconify()
    while(dicenum==0):
        dicewin.update()
         
    dicewin.withdraw()
    d=dicenum
    dicenum=0
    return d
def throwdice():
    global dicenum
    
    for i in range(10):
        dice=random.randint(0,5)
        display['image']=dicelist[dice]
        display.photo=dicelist[dice]
        dicewin.update()
        time.sleep(0.05)
        if i==5: winsound.PlaySound('sound\\dice.wav', winsound.SND_ASYNC)
    time.sleep(0.4)
    print(dice+1)
    dicenum=dice+1
# window.update()
# window.update_idletasks()
#window.mainloop()
dicewin=Tk()
dicewin.title("�ֻ���")
dicewin.configure(background='black')
dicewin.overrideredirect(True)
dicewin.wm_attributes("-topmost", True)
dicewin.geometry("+300+200")
dicebtn=Button(dicewin, text=("�ֻ��� ������"), width=30, height=5, command=throwdice,background="white")
dicelist=[PhotoImage(file="dice\\Side1.gif",master=dicewin),
          PhotoImage(file="dice\\Side2.gif",master=dicewin),
          PhotoImage(file="dice\\Side3.gif",master=dicewin),
          PhotoImage(file="dice\\Side4.gif",master=dicewin),
          PhotoImage(file="dice\\Side5.gif",master=dicewin),
          PhotoImage(file="dice\\Side6.gif",master=dicewin)]

dicewin.lift()
display = Label(dicewin,image=dicelist[0],borderwidth=0,compound="center",highlightthickness = 0)
dicebtn.grid(row=0, column=1, sticky=N)
display.grid(row=1, column=1, sticky=N)



storewin = Tk()
storewin.title("����")
storewin.configure(background='#a04d00')
storewin.overrideredirect(True)
storewin.geometry("+500+0")
item=0
tabcontrol=ttk.Notebook(storewin)

tab1=Frame(tabcontrol,background='#a04d00')
tabcontrol.add(tab1,text="���ݷ�")

tab2=Frame(tabcontrol,background='#a04d00')
tabcontrol.add(tab2,text="�ֹ���")

tab3=Frame(tabcontrol,background='#a04d00')
tabcontrol.add(tab3,text="����")
tab4=Frame(tabcontrol,background='#a04d00')
tabcontrol.add(tab4,text="�������׷�")
tab5=Frame(tabcontrol,background='#a04d00')
tabcontrol.add(tab5,text="ü�����")
tab6=Frame(tabcontrol,background='#a04d00')
tabcontrol.add(tab6,text="��ų����������")
tab7=Frame(tabcontrol,background='#a04d00')
tabcontrol.add(tab7,text="��Ÿ��ȭ")
tab8=Frame(tabcontrol,background='#a04d00')
tabcontrol.add(tab8,text="�������ɷ�ġ")
tab9=Frame(tabcontrol,background='#a04d00')
tabcontrol.add(tab9,text="empty")

tabcontrol.pack(expan=3,fill="both")
tablist=[tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9]



def s1():
    global item
    item=1
def s2():
    global item
    item=2
def s3():
    global item
    item=3
def m1():
    global item
    item=4
def m2():
    global item
    item=5
def m3():
    global item
    item=6
def sh1():
    global item
    item=7
def sh2():
    global item
    item=8
def sh3():
    global item
    item=9
def f1():
    global item
    item=10
def f2():
    global item
    item=11
def f3():
    global item
    item=12
def a1():
    global item
    item=13
def a2():
    global item
    item=14
def a3():
    global item
    item=15
def ga():
    global item
    item=16
def sa():
    global item
    item=17
def bs():
    global item
    item=18
def i19():
    global item
    item=19
def i20():
    global item
    item=20
def i21():
    global item
    item=21
def i22():
    global item
    item=22
def i23():
    global item
    item=23
def i24():
    global item
    item=24
def i25():
    global item
    item=25
def i26():
    global item
    item=26
def i27():
    global item
    item=27
def i28():
    global item
    item=28
def nobuy():
    global item
    item=-1
def itemchoose(string,items):
    global item
    global indicate
    global itemhave
    tabcontrol.tab(tab9,text=("���� %s"% string))
    #indicate['text']=string
    itemhave['text']=""
    Items=["  ��1 x","  ��2 x","  ��3 x","  ����1 x","  ����2 x","  ����3 x","  ����1 x","  ����2 x","  ����3 x",
           "  ����ǿ���1 x","  ����ǿ���2 x","  ����ǿ���3 x","  ����1 x","  ����2 x","  ����3 x","  ��ȣõ�� x","  �����ǰ� x","  �Ǻ񸰰� x",  "���ڿ����� x","  �ڿ����� x","  ��������  x",
           "��� ���� x","  �����â x","  ������ ä��  x","��Ȱ��ä�� x","  �߱� �����ǹ��� x","  �ʱ� �����ǹ���  x","���� ���� x"]
    for i in range(len(items)):
        if items[i]>0:
            itemhave['text']+=Items[i]
            itemhave['text']+=str(items[i])
    
    storewin.deiconify()
    while(True):
        time.sleep(0.1)
        storewin.update()
        storewin.update_idletasks()
        
            
        if item!=0:
            i=item
            item=0
            storewin.withdraw()
            return i

itemfunctions=[s1,s2,s3,m1,m2,m3,sh1,sh2,sh3,f1,f2,f3,a1,a2,a3,ga,sa,bs,i19,i20,i21,i22,i23,i24,i25,i26,i27,i28]

itembtn=[]
itemnames=['1��� ��\n(����:300,���ݷ�+80,\n�� ����+20)','2��� ��\n(����:80,���ݷ�+30)','3��� ��\n(����:30,���ݷ�+10)','1��� ����\n(����:320,�ֹ���+120)',
           '2��� ����\n(����:120,�ֹ���+50)','3��� ����\n(����:40,�ֹ���+20)','1��� ����\n(����:300,����+80,\n�ִ�ü��+100)','2��� ����\n(����:120,����+30,\n�ִ�ü��+30)',
           '3��� ����\n(����:30,����+10,\n�ִ�ü��+10)','1��� ����ǿ���\n(����:400,ü�����+30,\n�ִ�ü��+100)','2��� ����ǿ���\n(����:120,ü�����+10,\n�ִ�ü��+60)','3��� ����ǿ���\n(����:40,ü�����+5)',
           '1��� ����\n(����:300,�������׷�+100,\n�ִ�ü��+120)','2��� ����\n(����:100,�������׷�+40,\n�ִ�ü��+30)','3��� ����\n(����:40,�������׷�+10,\n�ִ�ü��+10)','��ȣ õ�� \n(����:350,�������׷�+70,\n����+50,�ִ�ü��+60)',
           '�����ǰ�\n(����:40,��������+10)','�Ǻ񸰰�\n(����:250,���ݷ�+30,\n��������+30)','���ڿ��� ��\n(����:300,ü��+50,\n��ų����������+40)','�ڿ�����\n(����:70,��ų����������+10)','��������\n(����:40,��ų����������+5)','��� ����\n(����:35,ü��+40)',
           '����� â\n(����:300,�߰� �������� 25% \n ������ �ɷ�ġ+30)','������ ä��\n(����:340,�⺻���� ��Ÿ�+2 \n ������ �ɷ�ġ+80 ,\n�⺻���ݽ� 30% ��������)','��Ȱ�� ä��\n(����:45,�⺻���� ��Ÿ�+1)','�߱� �����ǹ���\n(����:50,������ �ɷ�ġ+50)',
           '�ʱ� ������ ����\n(����:35,������ �ɷ�ġ+10)','���� ����\n(����:60,�߰� �������� 5% )']
indicate= Label(tab1, text="", fg="black", font="none 20")
indicate.grid(row=0, column=1, sticky=N)
indicate.configure(background='#a04d00')
nobuybtn=Button(tab1, text="buy nothing", width=23, height=3, command=nobuy)
nobuybtn2=Button(tab2, text="buy nothing", width=23, height=3, command=nobuy)
nobuybtn3=Button(tab3, text="buy nothing", width=23, height=3, command=nobuy)
nobuybtn4=Button(tab4, text="buy nothing", width=23, height=3, command=nobuy)
nobuybtn5=Button(tab5, text="buy nothing", width=23, height=3, command=nobuy)
nobuybtn6=Button(tab6, text="buy nothing", width=23, height=3, command=nobuy)
nobuybtn7=Button(tab7, text="buy nothing", width=23, height=3, command=nobuy)
nobuybtn8=Button(tab8, text="buy nothing", width=23, height=3, command=nobuy)
nobuybuttons=[nobuybtn,nobuybtn2,nobuybtn3,nobuybtn4,nobuybtn5,nobuybtn6,nobuybtn7,nobuybtn8]

for i in range(8):
    nobuybuttons[i].grid(row=0, column=2, sticky=E)
    nobuybuttons[i].configure(background='white')


itemhave=Label(tab9, text=(""), fg="white", font="none 13")
itemhave.grid(row=0,column=0,sticky=N)
itemhave.configure(background='#a04d00')

#���ݷ�
k=16
for j in range(0,2):
    
    btn=Button(tab1, text=itemnames[k], width=30, height=4, command=itemfunctions[k])
    btn.grid(row=2, column=j, sticky=N)
    btn.configure(background='#ffbb00')
    k+=1
k=0
for j in range(0,3):
    
    btn=Button(tab1, text=itemnames[k], width=30, height=4, command=itemfunctions[k])
    btn.grid(row=1, column=j, sticky=N)
    btn.configure(background='#ffbb00')
    k+=1
    
#�ֹ���
k=3
for j in range(0,3):
    
    btn=Button(tab2, text=itemnames[k], width=30, height=4, command=itemfunctions[k])
    btn.grid(row=1, column=j, sticky=N)
    btn.configure(background='#ffbb00')
    k+=1
#����
k=6
for j in range(0,3):
    
    btn=Button(tab3, text=itemnames[k], width=30, height=4, command=itemfunctions[k])
    btn.grid(row=1, column=j, sticky=N)
    btn.configure(background='#ffbb00')
    k+=1
btn=Button(tab3, text=itemnames[15], width=30, height=4, command=itemfunctions[15])
btn.grid(row=2, column=0, sticky=N)
btn.configure(background='#ffbb00')
#�������׷�
k=12
for j in range(0,3):
    
    btn=Button(tab4, text=itemnames[k], width=30, height=4, command=itemfunctions[k])
    btn.grid(row=1, column=j, sticky=N)
    btn.configure(background='#ffbb00')
    k+=1
btn=Button(tab4, text=itemnames[15], width=30, height=4, command=itemfunctions[15])
btn.grid(row=2, column=0, sticky=N)
btn.configure(background='#ffbb00')
#ü�����
k=9
for j in range(0,3):
    
    btn=Button(tab5, text=itemnames[k], width=30, height=4, command=itemfunctions[k])
    btn.grid(row=1, column=j, sticky=N)
    btn.configure(background='#ffbb00')
    k+=1
btn=Button(tab5, text=itemnames[21], width=30, height=4, command=itemfunctions[21]) #������
btn.grid(row=2, column=0, sticky=N)
btn.configure(background='#ffbb00')
#��ų����������
k=18
for j in range(0,3):
    
    btn=Button(tab6, text=itemnames[k], width=30, height=4, command=itemfunctions[k])
    btn.grid(row=1, column=j, sticky=N)
    btn.configure(background='#ffbb00')
    k+=1
#��Ÿ��ȭ
k=23
for j in range(0,2):
    
    btn=Button(tab7, text=itemnames[k], width=30, height=4, command=itemfunctions[k])
    btn.grid(row=1, column=j, sticky=N)
    btn.configure(background='#ffbb00')
    k+=1
#�������ɷ�ġ
k=25
for j in range(0,2):
    
    btn=Button(tab8, text=itemnames[k], width=30, height=4, command=itemfunctions[k])
    btn.grid(row=1, column=j, sticky=N)
    btn.configure(background='#ffbb00')
    k+=1
btn=Button(tab8, text=itemnames[22], width=30, height=4, command=itemfunctions[22]) #�����â
btn.grid(row=2, column=1, sticky=N)
btn.configure(background='#ffbb00')
btn=Button(tab8, text=itemnames[27], width=30, height=4, command=itemfunctions[27]) #���Ǳ���
btn.grid(row=2, column=2, sticky=N)
btn.configure(background='#ffbb00')
btn=Button(tab8, text=itemnames[23], width=30, height=4, command=itemfunctions[23]) #������ä��
btn.grid(row=2, column=0, sticky=N)
btn.configure(background='#ffbb00')
#window.mainloop()



