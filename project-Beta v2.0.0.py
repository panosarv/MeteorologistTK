#------Modules------
import tkinter as tk
import weatherLive as wL
from tkinter import ttk
from PIL import ImageTk
import unidecode as uni#**
from transliterate import translit#**
import time
import pygame #**
import os
import inspect

class Map():
    #Main Function
    def __init__(self,parent):
        #------Canvas------
        self.parent=parent
        self.canvas=tk.Canvas(parent,width=746,height=728)
        self.canvas.pack(side='left',expand=0)
        self.gif=tk.PhotoImage(file=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+'\\Images\\poleis746x728.gif')
        self.canvas.create_image(373,364, image = self.gif)
        self.canvas.bind('<Button-1>',self.callback)
        self.canvas.bind('<Motion>',self.mouseChanger)
        self.point=None
        self.soundPlayer=None
        self.volume=1.0
        #------Main-Frames------
        self.frame=tk.Frame(parent,height=670,bg='black')
        self.frame.pack(expand=1,fill='both')
        self.frame2=tk.Frame(parent,height=58,bg='pink')
        self.frame2.pack(expand=1,fill='both')
        
        self.frame.propagate(0)
        self.frame2.propagate(0)
        #------Label/ComboBox/MapButton(Frame1)------
        self.comboBox()
        self.label=tk.Label(self.frame,text='Kαιρός!',bg='light blue',fg='black',font='Consolas 20',relief='ridge',width=500,height=500)
        self.label.pack()
        self.muteButton=tk.Button(self.canvas,text='◀⚟',font='Consolas 20',bg='grey',fg='yellow',command=self.muteButton,relief='raised',width=3)
        self.muteButton.place(x=15,y=660)
        self.muteButton.bind('<Enter>',self.buttonChange)
        self.prevText='Καιρός!'
        self.currText='Καιρός!'
        #------Buttons(Frame2)------
        
        self.circleButton=tk.Button(self.frame2,text='웃',font='Consolas 24',fg='white',bg='dark grey',relief='raised',width=3,command=self.showUS)
        self.circleButton.pack(side='left',expand=0,fill='y')
        self.circleButton.bind('<Enter>',self.buttonChange)
        self.exitButton=tk.Button(self.frame2,text='❌',font='Consolas 20',fg='red',bg='dark grey',relief='raised',width=3,command=self.exitButton)
        self.exitButton.pack(side='right',expand=0,fill='y')
        self.exitButton.bind('<Enter>',self.buttonChange)
        #------Extra-Frame------
        self.frame3=tk.Frame(self.frame2,height=58,width=200,bg='white')
        self.frame3.pack(expand=1,fill='both')
        #------Buttons(Frame3)------
        self.prevButton=tk.Button(self.frame3,text='◀',font='Consolas 27',bg='dark grey',relief='raised',command=self.prevCity)
        self.nextButton=tk.Button(self.frame3,text='▶',font=',Consolas 33',bg='dark grey',relief='raised',command=self.nextCity)
        self.prevButton.bind('<Enter>',self.buttonChange)
        self.nextButton.bind('<Enter>',self.buttonChange)
        self.parent.bind('<Left>',self.leftKey)
        self.parent.bind('<Right>',self.rightKey)
        self.prevButton.pack(side='left',fill='both',expand=1)
        self.nextButton.pack(side='right',fill='both',expand=1)
        
    

    #------ButtonFunctions------
    def leftKey(self,event):
        self.prevCity()

    def rightKey(self,event):
        self.nextCity()


    def exitButton(self):
        self.parent.destroy()
        pygame.quit()


    def muteButton(self):
        if self.volume==1.0:
            self.volume=0.0
            self.muteButton.config(text='◀▏')
        elif self.volume==0.0:
            self.volume=1.0
            self.muteButton.config(text='◀⚟')


    def showUS(self):
        names='Μέλη ομάδας:\n•Αρβανίτης Παναγιώτης \n•Δημητροπούλου Μαρία \n•Καραδήμας Σπυρίδων Αλέξανδρος \n•Παυλίδης Κωνσταντίνος \n•Σταθάτος Αντώνιος \n•Σταυρογιαννόπουλος Ιωάννης \n•Χιώτης Χρήστος '
        if self.prevText!='Καιρός!':
            self.soundPlayer.stop()
        if self.currText!=names:
            self.label.config(text=names, font='Consolas 20',anchor='c',image='')
            self.circleButton.config(relief='sunken')
            self.label.image=None
            self.canvas.itemconfig(self.point,state='hidden')
            self.currText=names
        else:
            if self.prevText=='Καιρός!':
                self.label.config(text='Καιρός!',image='',anchor='c')
                self.circleButton.config(relief='raised')
                self.label.image=None
                self.currText='Καιρός!'
            else:
                self.label.config(text=self.prevText,image=self.weatherIc,anchor='n')
                self.circleButton.config(relief='raised')
                self.label.image=self.weatherIc
                self.currText=self.prevText
                self.canvas.itemconfig(self.point,state='normal')
        
        
        
    def nextCity(self):
        currCity=self.label["text"].split('\n')[0][6:]
        sortedLi=sorted(li,key=self.getKey)
        try:
    
            for item in sortedLi:
                if item[2]==currCity:
                    pos=sortedLi.index(item)
                    break
            if pos!=(len(sortedLi)-1):
                nextCityID=sortedLi[pos+1][3]
                nextCityN=sortedLi[pos+1][2]
                nCX=sortedLi[pos+1][0]
                nCY=sortedLi[pos+1][1]
            else:
                nextCityID=sortedLi[0][3]
                nextCityN=sortedLi[0][2]
                nCX=sortedLi[0][0]
                nCY=sortedLi[0][1]

            self.prevText=self.printCity(nextCityID,nextCityN) 
            self.createPoint(nCX,nCY)
        except:
            self.label.config(text='Παρακαλώ διαλέξετε\n μια πόλη πρώτα.',anchor='c',image='')
            self.label.image=None
        
        self.nextButton.config(relief='raised')


    def prevCity(self):
        
        currCity=self.label["text"].split('\n')[0][6:]
        sortedLi=sorted(li,key=self.getKey)
        try:
            for item in sortedLi:
                if item[2]==currCity:
                    pos=sortedLi.index(item)
                    break
            if pos!=0:
                prevCityID=sortedLi[pos-1][3]
                prevCityN=sortedLi[pos-1][2]
                pCX=sortedLi[pos-1][0]
                pCY=sortedLi[pos-1][1]
            else:
                prevCityID=sortedLi[len(sortedLi)-1][3]
                prevCityN=sortedLi[len(sortedLi)-1][2]
                pCX=sortedLi[len(sortedLi)-1][0]
                pCY=sortedLi[len(sortedLi)-1][1]
            self.prevText=self.printCity(prevCityID,prevCityN)
            self.createPoint(pCX,pCY)
        except:
            self.label.config(text='Παρακαλώ διαλέξετε\n μια πόλη πρώτα.',anchor='c',image='')
            self.label.image=None
        time.sleep(0.05)
        self.prevButton.config(relief='raised')
    #------Sorting-Function------          
    def getKey(self,li):
        word=uni.unidecode(li[2])
        if word[0]=='B':
            word='V'+word[1:]
        elif li[2][0]=='Η':
            word='Η'+uni.unidecode(li[2])[1:]
        elif li[2][0]=='Χ':
            word='Ch'+uni.unidecode(li[2])[1:]
        elif li[2][0]=='Ξ':
            word='X'+uni.unidecode(li[2])[1:]
        elif li[2][0]=='Φ':
            word='F'+uni.unidecode(li[2])[1:]
        else:
            word=word
        return translit(word,'el')



    #------ComboBox-Function------
    def comboBox(self):
        self.box_value = tk.StringVar()
        self.box = tk.ttk.Combobox(self.frame,state='readonly', textvariable=self.box_value)
        self.box.bind('<<ComboboxSelected>>', self.newselection)
        newli=sorted(li,key=self.getKey)
        cityTupple=('--Επιλέξτε μια πόλη--',)
        for item in newli :
            cityTupple=cityTupple+(item[2],)
            
        self.box['values'] = cityTupple
        self.box.current(0)
        self.box.pack(fill='x',expand=0)
        
        
    def newselection(self, event):
        self.value_of_combo = self.box.get()
        for item in li:
            if item[2]==self.value_of_combo:
                cID=item[3]
                X=item[0]
                Y=item[1]
                self.prevText=self.printCity(cID,self.value_of_combo)
                self.createPoint(X,Y)
                
        

    #------Mouse-Functions------
    def mouseChanger(self,event):
            self.canvas.config(cursor='draft_large')
    
    def buttonChange(self,event):
        self.canvas.config(cursor='hand2')
        self.frame2.config(cursor='hand2')
    
    def callback(self,event):
        if event.x<746:
            self.canvas.config(cursor='draft_large red red')
            X,Y,cName,cID=self.findClosest(li,event.x,event.y)
            self.createPoint(X,Y)
            self.prevText=self.printCity(cID,cName)
            
           
            
    
    #------Selection/Weather-Functions------
    def findClosest(self,li,mouseX,mouseY):
        closestD=0
        cityName=''
        cityID=''
        cityX=0
        cityY=0
        for item in li :
            d=((item[0]-mouseX)**2+(item[1]-mouseY)**2)**0.5
            if mouseX==item[0] and mouseY==item[1]:
                cityName=item[2]
                cityX=item[0]
                cityY=item[1]
                cityID=item[3]
            else:
                if closestD==0:
                    closestD=d
                    cityID=item[3]
                    cityName=item[2]
                    cityY=item[1]
                    cityX=item[0]
                elif d<closestD:
                    closestD=d
                    cityName=item[2]
                    cityX=item[0]
                    cityY=item[1]
                    cityID=item[3]
        
        return cityX,cityY,cityName,cityID


    def weatherIcon(self,icon):
        fileName=icon+".png"
        filepath=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+'\\Images\\'+fileName
        return filepath 

    def sounds(self,icon):
        di={'01d':'sun.mp3','01n':'clear_night.wav','02d':'clouds_normal.wav','02n':'clouds_normal.wav',
            '03d':'clouds_normal.wav','03n':'clouds_normal.wav','04d':'clouds_heavy.wav','04n':'clouds_heavy.wav',
            '09d':'rain2.wav','09n':'rain.wav','10d':'rain2.wav','10n':'rain2.wav',
            '11d':'thunder.wav','11n':'thunder.wav','13d':'snow.wav','13n':'snow.wav','50d':'clouds_normal.wav',
            '50n':'clouds_normal.wav'}
        sound=di[icon]
        soundpath=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+'\\soundsWav\\'+sound
        return soundpath
        
    

                       
    def createPoint(self,x,y):
        radious=5
        if self.point ==None:
            self.point=self.canvas.create_oval(x-radious,y-radious,x+radious,y+radious,fill='red')
        else:
            self.canvas.coords(self.point,x-radious,y-radious,x+radious,y+radious)
        self.canvas.itemconfig(self.point,state='normal')



    def printCity(self,cityID,cityName):
        pygame.init()
        weather,icon=wL.getWeather(cityID)
        path=self.sounds(icon)
        soundPlayer = pygame.mixer.Sound(path)
        soundPlayer.set_volume(self.volume)
        self.soundPlayer=soundPlayer
        fileN=self.weatherIcon(icon)
        if icon[-1]=='n': bg_color='midnight blue'
        else: bg_color='sky blue'
        self.weatherIc=ImageTk.PhotoImage(file=fileN)
        weatherTxt='Πόλη: {}\n{} '.format(cityName,weather)
        self.label.config(text=weatherTxt,font='Consolas 18',bg=bg_color,anchor='n',image=self.weatherIc,compound='bottom',height=728)
        self.label.image=self.weatherIc
        self.sounds(icon)
        soundPlayer.play()
        root.after(2000,soundPlayer.stop)
        self.circleButton.config(relief='raised')
        return weatherTxt
    

    
            
#------List-of-Cities------
li=[[168,372,'Πάτρα','255683'],[141,432,'Πύργος','8133887'],[96,420,'Ζάκυνθος','251280'],[195,500,'Καλαμάτα','261604'],
    [219,450,'Τρίπολη','252601'],[256,445,'Ναύπλιο','256637'],[264,407,'Κόρυνθος','259289'],[142,359,'Μεσολόγγι','6693122'],
    [330,403,'Αθήνα','264371'],[432,458,'Ερμούπολη','262603'],[601,422,'Σάμος','256865'],[529,360,'Χίος','259973'],
    [712,558,'Ρόδος','400666'],[563,282,'Μυτιλήνη','256866',],[502,693,'Άγιος Νικόλαος','263824'],[452,680,'Ηράκλειο','261745'],
    [356,661,'Χανιά','260114'],[395,677,'Ρέθυμνο','254352'],[321,352,'Χαλκίδα','260133'],[260,356,'Λιβαδειά','258463'],[220,344,'Άμφισσα','265187'],
    [63,376,'Αργοστόλι','264668'],[226,305,'Λαμία','258620'],[173,303,'Καρπενήσι','260891'],[83,309,'Λευκάδα','258438'],[88,295,'Πρέβεζα','254698'],
    [107,276,'Άρτα','264559'],[185,254,'Καρδίτσα','260989'],[267,257,'Βόλος','8133894'],[227,229,'Λάρισα','258576'],[172,235,'Τρίκαλα','252664'],[50,236,'Ηγουμενίτσα','262420'],
    [97,221,'Ιωάννινα','261779'],[23,222,'Κέρκυρα','2463679'],[146,178,'Γρεβενά','736151'],[178,155,'Κοζάνη','735563'],[136,131,'Καστοριά','735927'],
    [234,160,'Κατερίνη','735914'],[147,106,'Φλώρινα','736229'],[210,133,'Βέροια','733905'],[199,105,'Έδεσσα','736357'],
    [271,128,'Θεσσαλονίκη','734077'],[309,151,'Πολύγυρος','734517'],[263,85,'Κιλκίς','735736'],[317,77,'Σέρρες','734330'],[365,70,'Δράμα','736364'],
    [385,92,'Καβάλα','735861'],[425,71,'Ξάνθη','733840'],[465,71,'Κομοτηνή','735640'],[505,98,'Αλεξανδρούπολη','736928'],[139,333,'Αγρίνιο','265560'],[468,456,'Μύκονος','257056'],
    [476,496,'Νάξος','256632'],[454,497,'Πάρος','255721'],[515,521,'Αμοργός','265142'],[467,534,'Ίος','261772'],[624,650,'Κάρπαθος','260895'],[476,569,'Σαντορίνη','252920'],[154,495,'Πύλος','255293'],[233,497,'Σπάρτη','253394'],
    [605,504,'Κάλυμνος','261507'],[85,355,'Ιθάκη','261708'],[199,377,'Αίγιο','265500'],[87,185,'Κόνιτσα','735636'],[211,182,'Όλυμπος','8133846'],[318,403,'Πειραιάς','255274'],[451,205,'Λήμνος','256930'],
    [414,510,'Σίφνος','264748'],[395,537,'Μήλος','256952'],[397,487,'Σέριφος','8133682'],[391,465,'Κύθνος','8133953'],[633,515,'Κως','259245'],[453,442,'Τήνος','252854'],[427,413,'Άνδρος','265040'],[533,441,'Ικαρία','8133747'],
    [531,691,'Σητεία','253759'],[497,711,'Ιεράπετρα','8133930'],[344,690,'Παλαιόχωρα','256131'],[424,717,'Μάταλα','255242'],[432,544,'Φολέγανδρος','262319'],[309,278,'Σκιάθος','8133939'],
    [328,281,'Σκόπελος','253581'],[310,472,'Ύδρα','8133769'],[401,305,'Σκύρος','8133975'],[385,441,'Κέα','260348'],[227,535,'Γύθειο','251297'],[268,588,'Κύθηρα','8133702'],[306,375,'Θήβα','252910'],
    [121,406,'Κυλλήνη','259813'],[312,428,'Αίγινα','265502'],[409,122,'Θάσος','8133898'],[482,142,'Σαμοθράκη','734359']]



#======Main-Programme======
root=tk.Tk()
root.geometry('1251x728+0+0')
root.resizable(width=False, height=False)
root.title('                                                                                                                                                         Ο καιρός στην Ελλάδα')
app=Map(root)
root.mainloop()
