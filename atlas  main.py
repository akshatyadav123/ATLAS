import speech_recognition as sr
import pyttsx3
import mysql.connector as m
import random
import queue
import sys
import tkinter as tk
import ttkbootstrap as tbk
from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from ttkbootstrap.scrolled import ScrolledFrame
import threading
import time
import math
from PIL import Image
Image.CUBIC = Image.BICUBIC

####################################################################################
root = tk.Tk()
root.title("ATLAS")
root.geometry("565x600") 
root.style=Style(theme='cyborg')
#############################################################################

my=m.connect(host="localhost",user="root",database="India",password="85246")
mc=my.cursor()


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
###############################################################################
#timer

'''def update_time():
    meter.step(1)
    #time.sleep(1)
    #update_time()'''

#list of all the used cities tablename,id
master=[]
pos=2
you="YOU"
dx="DEX"
dd="           DEX : "

#dict for chracter tables
dit={}
for i in range(97,123,1):
    c=chr(i)
    st=c+"_city"
    dit[c]=st
i=random.randrange(97,116,1)


sst="LETS START THE GAME WITH ALPHABET : "+chr(i).upper()
SpeakText(sst)
print(sst)
#dex label
dex=Label(root,text=dd+sst)
dex.grid(row=1,column=0,columnspan=5,sticky="n",ipadx=30,pady=30)
dex.configure(font=("",12))

#main frame for data

f1=ScrolledFrame(root,autohide=True,width=540,height=200,padding=0,bootstyle="dark")
f1.grid(row=3,column=0,rowspan=10,ipady=100,padx=10)

#headings
l2=Label(f1,text="Who",bootstyle="success")
l2.grid(row=0,column=0,sticky='w',columnspan=1,)

l3=Label(f1,text="CITY",bootstyle="success")
l3.grid(row=0,column=1,sticky='w',columnspan=1)

l4=Label(f1,text="STATE",bootstyle="success")
l4.grid(row=0,column=2,sticky='w',columnspan=1)

l5=Label(f1,text="ENDS WITH",bootstyle="success")
l5.grid(row=0,column=3,sticky='w',columnspan=1)

#meter
'''meter = tbk.Meter(
    root,
    metersize=95,
    amounttotal=120,
    wedgesize=0,
    amountused=120,
    meterthickness=12,
    stripethickness=10,
    subtext=None,
    subtextfont="",
    metertype="full",
    bootstyle='success'
    
)
meter.grid(row=10,column=0,columnspan=3,sticky="n",pady=20)'''



########################################################################
#adding data in table frame
def addc(t,i):
    e1=Entry(f1)
    e1.grid(row=i,column=0,ipadx=1,sticky="w",)

    e2=Entry(f1)
    e2.grid(row=i,column=1,ipadx=1,sticky="w",)

    e3=Entry(f1)
    e3.grid(row=i,column=2,ipadx=1,sticky="w",)

    e4=Entry(f1)
    e4.grid(row=i,column=3,ipadx=1,sticky="w",)

    
    
    e1.insert(0,t[0])
    e2.insert(0,t[1])
    e3.insert(0,t[2])
    e4.insert(0,t[3])
    root.update()



############################
def listen_v():
    try:
        r=sr.Recognizer()
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            c= MyText.lower()
            return (c,0)
    except sr.RequestError as e:
        return ("1",1)
    except sr.UnknownValueError:
        r = sr.Recognizer()
        return ("wa",1)
        
#t1=threading.Thread(target=listen_v)
'''class MyThread(threading.Thread):
    def __init__(self,result_queue):
        threading.Thread.__init__(self)
        self.result_queue=result_queue
        self.running=threading.Event()
        self.running.set()
    def run(self):
        while self.running.is_set():
            result=listen_v()
            self.result_queue.put(result)
            #time.sleep(5)
            
            
        
    def get_result(self):
        return self.result
    def stop(self):
        self.running.clear()
result_queue=queue.Queue()        
t1=MyThread(result_queue)'''
        
def sp(lastc):
    #t1.join()
    #result=result_queue.get()
    result=listen_v()
    c,er=result[0],result[1]
    if(er==0):
        a=c[0]
        if(a==lastc and c!="exit"):
            q="select id,city_state,frequency from "+dit[a]+" where city_name='{}'".format(c)
            mc.execute(q)
            idc=mc.fetchone()
        
            if(idc):
                cid,state,freq=idc
                print("You have said : "+c+" city of "+state)
                dex.configure(text=dd+"You have said : "+c.upper()+" city of "+state.upper())
                
                SpeakText("You have said : "+c+" city of "+state)
                
                temp=c[::-1]
                lc=temp[0]
                global pos
                addc((you,c.upper(),state,lc.upper()),pos)
                root.update()
                pos+=1
                root.update()
                dump=mc.fetchall()
                q2="update "+dit[a]+" set used=1,frequency=frequency+1 where id='{}'".format(cid)
                my.commit()
                master.append([dit[a],cid])
                dump=mc.fetchall()
                q3="select * from "+dit[lc]+" where used=0 and frequency in(select max(frequency)from "+dit[lc]+") limit 1"
                mc.execute(q3)
                cid,na,st,us,ff=mc.fetchall()[0]
                
                print("DEX : "+na+" city of "+st)
                dex.configure(text=dd+na.upper()+" city of "+st.upper())
                na=na.lower()
                SpeakText(na+" city of "+st)
                nc=na[::-1]
                nc=nc[0]
                print("Ends with :"+nc.upper())
                
                addc((dx,na.capitalize(),st,nc.upper()),pos)
                pos+=1
                #meter.configure(amountused=120)
                root.update()

                
                master.append([dit[na[0]],cid])
                q4="update "+dit[na[0]]+" set used=1 where id='{}'".format(cid)
                mc.execute(q4)
                my.commit()
                return nc
            else:
                print("Does Not found this city in Database")
                dex.configure(text=dd+"Does Not found this city in Database")
                SpeakText("Does Not found this city in Database")
                return lastc
        elif(c=="exit"):
            print("Quitting the game")
            dex.configure(text=dd+"Quitting the game")
            root.update()
            SpeakText("Quitting the game")
            
            return 0
        else:
            print("Please name a city which starts with letter :"+lastc)
            dex.configure(text=dd+"Please name a city which starts with letter :"+lastc)
            root.update()
            SpeakText("Please name a city which starts with letter :"+lastc)
            return lastc
    if(er==1 and c=="1"):
        print("Could not request results; {0}".format(e))

        return lastc
    
    if(er==1 and c=="wa"):
        print("Waiting....")
        dex.configure(text=dd+" Waiting....")
        root.update()
        return lastc
        
        
#update_time()
#t1.start()
kk=sp(chr(i))
 


root.update()


while(1):
    kk=sp(kk)
    if(kk==0):
        #t1.stop()
        #t1.join()
        for i in master:
            q="update "+i[0]+" set used=0 where id='{}'".format(i[1])
            mc.execute(q)
        if(len(master)!=0):
            my.commit()
            my.close()
        sys.exit()
        break
    
    

root.mainloop()


