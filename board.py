import turtle
import glob

wn=turtle.Screen()
wn.setup(800,700)
wn.bgcolor("lightgray")
wn.title("board")


for i in glob.glob('obstacle_eng\\*.gif'):
    turtle.register_shape(i)
for i in glob.glob('projectiles\\*.gif'):
    turtle.register_shape(i)
    

class arrow(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("projectiles\\arrow.gif")
        self.penup()
        self.speed(0)
        self.hideturtle()
    
    
    
class Projgraphic(turtle.Turtle):
    def __init__(self,id):
        turtle.Turtle.__init__(self)
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
        if id==1:
            self.shape("projectiles\\birdproj.gif")
        elif id==5:
            self.shape("projectiles\\jeanproj.gif")
        elif id==2:
            self.shape("projectiles\\goraeproj.gif")
        elif id==3:
            self.shape("projectiles\\creedproj.gif")
        elif id==4:
            self.shape("projectiles\\timoproj.gif")
        elif id==6:
            self.shape("projectiles\\jelliceproj.gif")
        elif id==7:
            self.shape("projectiles\\movingshinproj1.gif")
        elif id==8:
            self.shape("projectiles\\movingshinproj2.gif")
        elif id==9:
            self.shape("projectiles\\blkxproj1.gif")
        elif id==10:
            self.shape("projectiles\\blkxproj2.gif")
        elif id==11:
            self.shape("projectiles\\blkxproj3.gif")
        elif id==12:
            self.shape("projectiles\\drmichinproj.gif")
        
        
        
        self.penup()
        self.speed(0)
        self.hideturtle()
    
    def set(self,loca,size):
        self.showturtle()
        
        rangepen.clear()
        sizepen.clear()
        self.goto(boardlist[loca][1],boardlist[loca][2])
        for i in range(loca,loca+size):
            sizepen.shape("projectiles\\projsize.gif")
            if i<len(boardlist):
                sizepen.goto(boardlist[i][1],boardlist[i][2])
                sizepen.stamp()
        
        
        
        
    def hide(self):
        self.hideturtle()
        sizepen.clear()
                            

    



class player(turtle.Turtle):
    
    
    def __init__(self,turn):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.turn=turn        
    def show(self):
        if self.turn==0:
            self.color("blue")
            self.shape("square")
        elif self.turn==1:
            self.color("red")
            self.shape("circle")
        elif self.turn==2:
            self.color("green")
            self.shape("triangle")
        elif self.turn==3:
            self.color("purple")
            self.shape("arrow")
        self.goto(-400,300)
        
    def changecolor(self,thisturn):
        if self.turn==0 :
            if self.turn!=thisturn:
                self.color("#478dff")
            else:
                self.color("blue")
        if self.turn==1 :
            if self.turn!=thisturn:
                self.color("#ff6060")
            else:
                self.color("red")
        if self.turn==2 :
            if self.turn!=thisturn:
                self.color("#91ff91")
            else:
                self.color("green")
        if self.turn==3 :
            if self.turn!=thisturn:
                self.color("#ce8eff")
            else:
                self.color("purple")
        arrow.showturtle()
        if self.turn==thisturn:
            arrow.goto(self.xcor(),self.ycor()+25)
        
    def Move(self,loca):
#         for y in range(len(dlist)):
#             for x in range(len(dlist[y])):
#                 if dlist[y][x][0]==loca:
#                         self.goto(dlist[y][x][2],dlist[y][x][3])
#                         return dlist[y][x][1]
        self.goto(boardlist[loca][1],boardlist[loca][2])
        arrow.goto(self.xcor(),self.ycor()+25)
        return boardlist[loca][0]
            
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(10)
        self.hideturtle()
        self._delay(0)

    
dlist=[]
l=[]
distin=[]
oneline=[]
oneline2=[]
muststop=[]
respawn=[]
location=-1
boardlist=[]


f=(open("map2.txt", "r").read())
distin=str(f).split('@')
muststop=distin[1].split()
respawn=distin[2].split()

oneline=distin[0].split("*")

for oneline2 in oneline:
    l=oneline2.split("/")
    d = []
    for oneset in l:
    
        (key, val) = oneset.split()
        temp=[int(key),int(val)]
        d.append(temp)
        
        
  
    dlist.append(d)

for i in range(int(muststop[len(muststop)-1])+1):
    boardlist.append([-1,0,0])
    
    
        


exec_x=0
exec_y=0
def setup(dlist):
    execution=False
    for y in range(len(dlist)):
        onelinelist=dlist[y];
        #print(charlist)
        for x in range(len(dlist[y])):
            
            screen_x=-400+(x*27)
            screen_y=300-(y*27)
            char=onelinelist[x][1]  
            
            if char!=-1:
                boardlist[onelinelist[x][0]]=[onelinelist[x][1],screen_x,screen_y] 
                pen.goto(screen_x,screen_y)
#                 onelinelist[x].append(screen_x)
#                 onelinelist[x].append(screen_y)
            if 0< char<3:
                pen.shape("obstacle_eng\\1.gif")
            elif 2< char<7:
                pen.shape("obstacle_eng\\2.gif")
            elif 6< char<11:
                pen.shape("obstacle_eng\\3.gif")
            elif char==0:
                 
                pen.shape("obstacle_eng\\0.gif")
            elif char==11:
                 
                pen.shape("obstacle_eng\\11.gif")
                 
            elif char==12:
                 
                pen.shape("obstacle_eng\\12.gif")
                 
            elif char==13:
                 
                pen.shape("obstacle_eng\\13.gif")
                 
            elif char==14:
                 
                pen.shape("obstacle_eng\\14.gif")
                 
            elif char==15:
                 
                pen.shape("obstacle_eng\\15.gif")
                 
            elif char==16:
                 
                pen.shape("obstacle_eng\\16.gif")
                 
            elif char==17:
                 
                pen.shape("obstacle_eng\\17.gif")
                 
            elif char==18:
                 
                pen.shape("obstacle_eng\\18.gif")
                 
            elif char==19:
                 
                pen.shape("obstacle_eng\\19.gif")
                 
            elif char==20:
                 
                pen.shape("obstacle_eng\\20.gif")
                 
            elif char==21:
                 
                pen.shape("obstacle_eng\\21.gif")
                 
            elif char==22:
                 
                pen.shape("obstacle_eng\\22.gif")
                 
            elif char==23:
                 
                pen.shape("obstacle_eng\\23.gif")
            elif char==24:
                pen.shape("obstacle_eng\\24.gif")
            elif char==25:
                pen.shape("obstacle_eng\\25.gif")
            elif char==26:
                pen.shape("obstacle_eng\\26.gif")
            elif char==27:
                pen.shape("obstacle_eng\\27.gif")
            elif char==28:
                pen.shape("obstacle_eng\\28.gif")
            elif char==29:
                pen.shape("obstacle_eng\\29.gif")
            elif char==30:
                pen.shape("obstacle_eng\\30.gif")
            elif char==31:
                pen.shape("obstacle_eng\\31.gif")
            elif char==32:
                pen.shape("obstacle_eng\\32.gif")
            elif char==33:
                pen.shape("obstacle_eng\\33.gif")
            elif char==34:
                pen.shape("obstacle_eng\\34.gif")
            elif char==35:
                pen.shape("obstacle_eng\\35.gif")
            elif char==36:
                pen.shape("obstacle_eng\\36.gif")
            elif char==37:
                pen.shape("obstacle_eng\\37.gif")
            elif char==38:
                pen.shape("obstacle_eng\\38.gif")
            elif char==39:
                pen.shape("obstacle_eng\\39.gif")    
            elif char==40:
                pen.shape("obstacle_eng\\40.gif")
            elif char==41:
                pen.shape("obstacle_eng\\41.gif")
            elif char==42:
                pen.shape("obstacle_eng\\42.gif")
            elif char==43:
                pen.shape("obstacle_eng\\13.gif")
            elif char==44:
                pen.shape("obstacle_eng\\42.gif")
            elif char==45:
                pen.shape("obstacle_eng\\45.gif")
            elif char==47:
                pen.shape("obstacle_eng\\47.gif")
            elif char==48:
                pen.shape("obstacle_eng\\48.gif")
            elif char==49:
                pen.shape("obstacle_eng\\49.gif")
            elif char==50:
                pen.shape("obstacle_eng\\50.gif")
            elif char==51:
                pen.shape("obstacle_eng\\51.gif")
            elif char==52:
                pen.shape("obstacle_eng\\52.gif")
            elif char==53:
                pen.shape("obstacle_eng\\53.gif")
            elif char==54:
                exec_x=screen_x
                exec_y=screen_y
                execution=True
            elif char==55:
                pen.shape("obstacle_eng\\55.gif")
            elif char==56:
                pen.shape("obstacle_eng\\56.gif")
            elif char==57:
                pen.shape("obstacle_eng\\57.gif")
            elif char==58:
                pen.shape("obstacle_eng\\58.gif")
            elif char==59:
                pen.shape("obstacle_eng\\59.gif")    
            elif char==60:
                pen.shape("obstacle_eng\\60.gif")    
            elif char==61:
                pen.shape("obstacle_eng\\61.gif")    
            elif char==63:
                pen.shape("obstacle_eng\\63.gif")    
            elif char==64:
                pen.shape("obstacle_eng\\64.gif") 
                  
                
            pen.stamp()
        if execution:
            pen.goto(exec_x,exec_y)
            pen.shape("obstacle_eng\\54.gif")
            pen.stamp()
    
def drawrange(start,end):
    if end>int(muststop[len(muststop)-1]):
        end=int(muststop[len(muststop)-1])
    
    for i in range(start,end+1):
        for m in muststop:
            if i==m:
                break;
        else:
            rangepen.goto(boardlist[i][1],boardlist[i][2])
            rangepen.shape("obstacle_eng\\projrange.gif")
            rangepen.stamp()
    
    
    
def clicked(x,y):
    
    global location
    location=-1
#     for yi in range(len(dlist)):
#             for xi in range(len(dlist[yi])):
#                 if dlist[yi][xi][0]!=-1:
#                     if int(x)-13<=dlist[yi][xi][2]<=int(x)+13 and  int(y)-13<=dlist[yi][xi][3]<=int(y)+13:
#                         location=dlist[yi][xi][0]
    for i in range(len(boardlist)):
        if int(x)-13<=boardlist[i][1]<=int(x)+13 and  int(y)-13<=boardlist[i][2]<=int(y)+13:
            location=i
def getloc():
    global location
    
        
    lc=location
    location=-1
    return lc

    

pen=Pen()
rangepen=Pen()
sizepen=Pen()
setup(dlist)


# pen.shape("obstacle_eng\\62.gif")
# pen.goto(-170,70)
# pen.stamp()
pen.speed(10)
arrow=arrow()


turtle.onscreenclick(clicked)


#wn.tracer(0)
# while True:
#     wn.update()


                
    

