#-*- coding: ms949 -*-
from tkinter import *
# from PIL import Image

def closedisplay():
    global l
    l.withdraw()

def textdisplay(num):
    global display
    global l
    l.withdraw()
    photo=photolist[num]
    display['image']=photo
    display.photo=photo

    l.update()
    if(num!=0): l.deiconify()
    

l=Tk()
display = Label(l,image=None,borderwidth=0,compound="center",highlightthickness = 0)
photolist=[None,PhotoImage(file="obstacleimages\\gold1.gif",master=l),PhotoImage(file="obstacleimages\\gold2.gif",master=l),
           PhotoImage(file="obstacleimages\\gold3.gif",master=l),PhotoImage(file="obstacleimages\\gold4.gif",master=l),
           PhotoImage(file="obstacleimages\\gold5.gif",master=l),PhotoImage(file="obstacleimages\\gold6.gif",master=l),
           PhotoImage(file="obstacleimages\\gold7.gif",master=l),PhotoImage(file="obstacleimages\\gold8.gif",master=l),
           PhotoImage(file="obstacleimages\\gold9.gif",master=l),PhotoImage(file="obstacleimages\\gold10.gif",master=l),
           PhotoImage(file="obstacleimages\\obs11.gif",master=l),PhotoImage(file="obstacleimages\\obs12.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs13.gif",master=l),PhotoImage(file="obstacleimages\\obs14.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs15.gif",master=l),PhotoImage(file="obstacleimages\\obs16.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs17.gif",master=l),PhotoImage(file="obstacleimages\\obs18.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs19.gif",master=l),PhotoImage(file="obstacleimages\\obs20.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs21.gif",master=l) ,PhotoImage(file="obstacleimages\\obs22.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs23.gif",master=l),PhotoImage(file="obstacleimages\\obs24.gif",master=l)
           ,None,PhotoImage(file="obstacleimages\\obs26.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs27.gif",master=l),PhotoImage(file="obstacleimages\\obs28.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs29.gif",master=l),None
           ,PhotoImage(file="obstacleimages\\obs31.gif",master=l),PhotoImage(file="obstacleimages\\obs32.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs33.gif",master=l),PhotoImage(file="obstacleimages\\obs34.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs35.gif",master=l),PhotoImage(file="obstacleimages\\obs36.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs37.gif",master=l),PhotoImage(file="obstacleimages\\obs38.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs39.gif",master=l),PhotoImage(file="obstacleimages\\obs40.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs41.gif",master=l),PhotoImage(file="obstacleimages\\obs42.gif",master=l)
           ,None,None,None,None
           ,PhotoImage(file="obstacleimages\\obs47.gif",master=l),PhotoImage(file="obstacleimages\\obs48.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs49.gif",master=l),None,PhotoImage(file="obstacleimages\\obs51.gif",master=l)
           ,PhotoImage(file="obstacleimages\\obs52.gif",master=l),PhotoImage(file="obstacleimages\\obs53.gif",master=l)
           ,None,PhotoImage(file="obstacleimages\\obs55.gif",master=l),None,None,None,None,None,None,None,None,None,None,None,None,None,None]
display.master.overrideredirect(True)
display.master.geometry("+200+50")
display.master.lift()
display.master.wm_attributes("-topmost", True)
display.master.wm_attributes("-disabled", True)
display.master.wm_attributes("-transparentcolor", "white")
display.pack()
l.withdraw()
#mainloop()
