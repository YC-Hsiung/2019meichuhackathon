import tkinter as tk
import os
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import copy
from tkinter import *
from PIL import ImageTk, Image
import pdfProcess
import cv2

file_path = ''
#dealing with open file
gap_x = 100
gap_y1 = 150
gap_y2 = 225

class Yee(tk.Toplevel):
    def __init__(self, parent,name):
        super().__init__()
        self.title('Soup Head Saver')
        self.parent = parent # 顯式地保留父視窗
        #self.iconbitmap("bear.ico")
        self.geometry("800x400")
        self.starbt = Button(self, text='unstared', width=8,bg = "grey",command = self.starpressed)
        self.starbt.place(x=700,y=20)

        self.quitbt = Button(self, text='quit', width=8,command = self.leave)
        self.quitbt.place(x=700,y=300)


        self.name = name
        if name[:-4] in self.parent.favorite:
            self.starbt.config(bg = 'yellow', text = 'stared')
        self.guten(name)
    def leave(self):
        self.destroy()
    def starpressed(self):          
        if self.starbt.cget('bg') == 'yellow':
            self.starbt.config(bg = 'grey',text = 'unstared')
            self.parent.favorite.remove(self.name[:-4])
        else:
            self.starbt.config(bg = 'yellow',text = 'stared')
            self.parent.favorite.append(self.name[:-4])
        fp = open('favorite.txt','w+')
        for t in self.parent.favorite: 
            fp.write(t+'\n')
        fp.close()


    def guten(self,name):
        n=Image.open(os.path.join("pdfProcess","tests",name[:-4],name))
        w,h=n.size
        factor=min([600/w,400/h])
        n=n.resize((int(factor*w),int(factor*h)), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(n)
        tk.Label(self,image = self.img).place(x=0,y=0)
        self.info = tk.Label(self,text="")
        self.info.place(x=n.size[0]+50,y=70)

        fp = open(os.path.join("pdfProcess","tests",name[:-4],"pinName.txt"),"r")
        tline = fp.readline()
        i=0
        self.inf = []
        while tline:
            i+=1
            x1=tline.split(" ")
            x=x1[0].split(",")
            x[0]=x[0][1:]
            x[1]=x[1][:-1]
            self.inf.append((x1[1],int(factor*int(x[0])),int(factor*int(x[1]))))
            tline = fp.readline()
        fp.close()
        for j in range(len(self.inf)):
            tk.Button(self,text=str(j+1),command=lambda j=j: self.cmd(j)).place(x=self.inf[j][1],y=self.inf[j][2])
    def cmd(self,n):
        self.info.configure(text="")
        self.info.configure(text=self.inf[n][0])


# 彈窗1: stored 
class Adding(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('Soup Head Saver')
        self.parent = parent # 顯式地保留父視窗
        #self.iconbitmap("bear.ico")
        self.geometry("800x400")
        self.file_path = ""
        self.r = ""

        #mf = Frame(self)
        #mf.pack()
        #f1 = Frame(mf, width=600, height=250)
        #f1.pack(fill=X)
        #f2 = Frame(mf, width=600, height=250)
        #f2.pack()
        Label(self,text="Select Element's Image",font = "Arial 12 bold").place(x = 40, y = 60)
        Button(self, text="Browse", command=self.open_file).place(x = 250, y = 60)
        Label(self,text="You Select: ",font = "Arial 12").place(x = 40, y = 120)
        self.l1 = Label(self,text = self.file_path,font = "12")
        self.l1.place(x = 250, y = 115)
        # 第三行
        #row3 = tk.Frame(self)
        #row3.pack(fill="x")
        
        tk.Button(self, text="取消", command=self.cancel).place(x = 400, y = 200 )
        tk.Button(self, text="確定", command=self.ok).place(x = 350, y = 200)
        self.l2 = Label(self,text = self.r)
        self.l2.place(x = 40, y = 150)
        self.l2.config(font = "Arial 13", fg = "Red")


    def result(self):
        # read component , convert to jpg
        component_name=self.parent.browse
        pin_img = pdfProcess.find_chart.Convert2Jpg(component_name)
        pdfProcess.table.box_extraction(cv2.imread(os.path.join("pdfProcess","tests",component_name,component_name+".jpg")),component_name)
        pinNameList=pdfProcess.pdfplum.readPinNameFile(os.path.join("pdfProcess","tests",component_name,"pinName.txt"))
        textList=[]
        pages=pdfProcess.pdfplum.textExtract(os.path.join("pdfProcess","tests",component_name,component_name+".pdf"),textList)
        usefulPg=pdfProcess.pdfplum.findUsefulPg(textList,pages,pinNameList,component_name)
        return True
    def ok(self):
        if(self.result() == False):
            self.l2.config(text = "Oops! There are no information in the given PDF file :(")
        else:
            fp = open('all.txt','r+')
            print('a')
            a = fp.readline()
            print(a)
            flag = True
            while a:
                if self.parent.browse == a[:-1]:
                    self.l2.config(text = "Oh No! The element already exists:(",fg = "Red")
                    flag = False
                    break
                a = fp.readline()
            if flag:
                fp.write(self.parent.browse)
                fp.write('\n')
                fp.close()
                self.parent.lall.append(self.parent.browse)
                self.destroy()
            fp.close()
        
    def cancel(self):
        self.destroy() 

    def open_file(self):
        self.attributes('-topmost',0)
        filename = askopenfilename()
        self.attributes('-topmost',1)
        infile = open(filename, 'r')
        self.parent.browse = filename
        self.parent.browse = filename.split('/')[-1][:-4]
        self.l1.config(text = filename)
        return  


# 主窗
class MyApp(tk.Tk):
        def __init__(self):
            super().__init__()
            #self.iconbitmap("bear.ico")
            self.geometry("800x400")
            # self.pack() # 若繼承 tk.Frame，此句必須有！！！
            self.title('Soup Head Saver')
            # 程式介面
            self.resizable(False,False) 
            self.searching = ""
            self.imgg = [0,1,2,3,4,5,6]   #history's image
            self.imgB = [0,0,0,0,0,0,0]   #history's button
            self.Lk = [self.Lk0,self.Lk1,self.Lk2,self.Lk3,self.Lk4,self.Lk5,self.Lk6]

            self.history = ["x.png","x.png","x.png","x.png","x.png","x.png","x.png"]  #history
            self.satisfied = ["x.png","x.png","x.png","x.png","x.png","x.png","x.png"]
            self.file = copy.deepcopy(self.history)
            self.lb = [0,0,0,0,0,0,0]
            self.setupUI()
           


        def setupUI(self):
        # title
            tk.Label( text='Soup Head Saver', width=100, fg = "blue",font = "Arial 20").pack()
            self.l1 = tk.Label( text="Save Your Time and Soup!", width=160)
            self.l1.config(font = "Arial 13",fg = "brown")
            self.l1.pack(fill = 'x')
            self.l2 = tk.Label(text="Enter the element you want to search: ",width=80)
            self.l2.place(x = -75, y = 70)
        # search bar
            self.en = Entry(cursor = "arrow")
            self.en.place(x = 100, y = 90, width = 600, height = 20)

            self.bt = Button(text = "Go", command = self.gogo)
            self.bt.config(bg = 'skyblue')
            self.bt.place(x = 710, y = 90, height = 20)

            self.rs = tk.Label(text = "Recently Used: ")
            self.rs.configure(font = "Arial 12 bold",fg = "red",)
            self.rs.place(x = 100, y = 125) 


            self.plusimg = ImageTk.PhotoImage(Image.open("plus.jpg"))  # PIL solution
            self.addingbt = Button(image = self.plusimg, command = self.adding)
            self.addingbt.place(x = 10, y = 100)
            #self.addlb = Label(text = "ADD")
            #self.addlb.place(x = 10, y = 210)

            self.homesimg = ImageTk.PhotoImage(Image.open("home.jpg"))  # PIL solution
            self.home = Button(image = self.homesimg, command = self.u_h_f)
            self.home.place(x = 10, y = 160)

            self.favosimg = ImageTk.PhotoImage(Image.open("star.jpg"))  # PIL solution
            self.favo = Button(image = self.favosimg,command = self.favoriting)
            self.favo.place(x = 10, y = 220)

            self.stored = ImageTk.PhotoImage(Image.open("store.jpg"))  # PIL solution
            self.storedbt = Button(image = self.stored, command = self.all)
            self.storedbt.place(x = 10, y = 280)

            self.dimg = ImageTk.PhotoImage(Image.open("x.png"))  # PIL solution
            self.imgB[0] = Button(image = self.dimg, command = self.Lk[0])
            self.imgB[0].place(x = 200, y = 150)
            self.lb[0] = Label(text = "x")
            self.lb[0].place(x = 200, y = 206)
            self.imgB[1] = Button(image = self.dimg, command = self.Lk[1])
            self.imgB[1].place(x = 300, y = 150)
            self.lb[1] = Label(text = "x")
            self.lb[1].place(x = 300, y = 206)
            self.imgB[2] = Button(image = self.dimg, command = self.Lk[2])
            self.imgB[2].place(x = 400, y = 150)
            self.lb[2] = Label(text = "x")
            self.lb[2].place(x = 400, y = 206)
            self.imgB[3] = Button(image = self.dimg, command = self.Lk[3])
            self.imgB[3].place(x = 500, y = 150)
            self.lb[3] = Label(text = "x")
            self.lb[3].place(x = 500, y = 206)
            self.imgB[4] = Button(image = self.dimg, command = self.Lk[4])
            self.imgB[4].place(x = 200, y = 230)
            self.lb[4] = Label(text = "x")
            self.lb[4].place(x = 200, y = 286)
            self.imgB[5] = Button(image = self.dimg, command = self.Lk[5])
            self.imgB[5].place(x = 300, y = 230)
            self.lb[5] = Label(text = "x")
            self.lb[5].place(x = 300, y = 286)
            self.imgB[6] = Button(image = self.dimg, command = self.Lk[6])
            self.imgB[6].place(x = 400, y = 230)
            self.lb[6] = Label(text = "x")
            self.lb[6].place(x = 400, y = 286)
            
            self.lea = tk.Button(text="Quit",height = 1, width=10,command = self.leave)
            #self.lea.config(bg = "")
            self.lea.place(x = 600, y = 350)
            self.browse = ""
            self.lall=[]
            self.favorite = []
            fp=open("all.txt")
            tline=fp.readline()
            i=0
            while tline:
                self.lall.append(tline[:-1])
                tline=fp.readline()
            fp.close()

            fp=open("favorite.txt")
            tline=fp.readline()
            i=0
            while tline:
                self.favorite.append(tline[:-1])
                tline=fp.readline()
            fp.close()
           #methods
        def favoriting(self):
            for i in range(len(self.favorite)):
                n = Image.open(self.favorite[i]+"_s.jpg")
                self.imgg[i]=ImageTk.PhotoImage(n)
                self.imgB[i].configure(image=self.imgg[i])
                self.lb[i].configure(text = self.favorite[i])
                self.file[i] = self.favorite[i]+".jpg"
            for j in range(len(self.favorite),len(self.file)):
                n = Image.open("x.png")
                self.imgg[j]=ImageTk.PhotoImage(n)
                self.imgB[j].configure(image=self.imgg[j])
                self.lb[j].configure(text = "x")
                self.file[j] = "x.png"
            self.rs.configure(text = "Favorite Element",fg = "ForestGreen",font = "Arial 12 bold")

        def all(self):
            for i in range(len(self.lall)):
                n = Image.open(self.lall[i]+"_s.jpg")
                self.imgg[i]=ImageTk.PhotoImage(n)
                self.imgB[i].configure(image=self.imgg[i])
                self.lb[i].configure(text = self.lall[i])
                self.file[i] = self.lall[i]+".jpg"
            for j in range(len(self.lall),len(self.file)):
                n = Image.open("x.png")
                self.imgg[j]=ImageTk.PhotoImage(n)
                self.imgB[j].configure(image=self.imgg[j])
                self.lb[j].configure(text = "x")
                self.file[j] = "x.png"

            self.rs.configure(text = "Stored Element",fg = "brown",font = "Arial 12 bold")


        def u_h_f(self):    #update history figure
            for i in range(len(self.history)):
                n = Image.open(self.history[i][:-4]+"_s.jpg")
                self.imgg[i] = (ImageTk.PhotoImage(n))  # PIL solution
                #p = "LK"+str(i)
                self.imgB[i].configure(image = self.imgg[i])
                n.close()
                self.lb[i].configure(text = self.history[i][:-4])

            self.rs.configure(text = "Recently Used: ",fg = "red", font = "Arial 12 bold") 
            self.file = copy.deepcopy(self.history)

        def u_s_f(self):  #update search figure
            for i in range(len(self.history)):
                n=self.satisfied[i][:-4]+"_s.jpg"
                self.imgg[i] = (ImageTk.PhotoImage(Image.open(n)))   # PIL solution
                self.imgB[i].configure(image = self.imgg[i])
                self.lb[i].configure(text = self.satisfied[i][:-4])
            for i in range(len(self.lall), len(self.file)):
                n="x_s.jpg"
                self.imgg[i] = (ImageTk.PhotoImage(Image.open(n)))   # PIL solution
                self.imgB[i].configure(image = self.imgg[i])
                self.lb[i].configure(text = "x")
            self.file = copy.deepcopy(self.satisfied)
        
        def leave(self):
            self.destroy()    

        def adding(self):
            pw2 = Adding(self)  #Adding is the new class
            self.wait_window(pw2)
            img = Image.open(os.path.join("pdfProcess","tests",self.browse,self.browse+".jpg"))
            img = img.resize((50,50),Image.ANTIALIAS)
            img.save(self.browse+'_s.jpg')
            return
        def gogo(self):
            self.searching = self.en.get()   #get the value input,  COMPARE
            self.rs.configure(text = "File satisfied requirement: ",fg = "blue")
            self.en.delete(0,END)
            i=0
            for t in self.lall:
                flag = True
                if len(self.searching) > len(t):
                    flag = False
                else:
                    for m in range(len(self.searching)):
                        if self.searching[m] != t[m]:
                            flag = False
                            break
                if flag :
                    self.satisfied[i]=t+".jpg"
                    i+=1
            for j in range(i,7):
                self.satisfied[j]="x.png"
            self.u_s_f()

        def Lk0(self): 
            if self.file[0] == "x.png" :
                return
            pw2 = Yee(self,self.file[0])  #Yee is the new class
            self.history = [self.file[0]] + self.history[:-1]
            self.wait_window(pw2)
            return
        def Lk1(self):
            if self.file[1] == "x.png":
                return
            pw2 = Yee(self,self.file[1])  #Yee is the new class
            self.history = [self.file[1]] + self.history[:-1]
            self.wait_window(pw2)
            return
        def Lk2(self):
            if self.file[2] == "x.png":
                return
            pw2 = Yee(self,self.file[2])  #Yee is the new class
            self.history = [self.file[2]] + self.history[:-1]
            self.wait_window(pw2)
            return
        def Lk3(self):
            if self.file[3] == "x.png":
                return
            pw2 = Yee(self,self.file[3])  #Yee is the new class
            self.history = [self.file[3]] + self.history[:-1]
            self.wait_window(pw2)
            return
        def Lk4(self):
            if self.file[4] == "x.png":
                return
            pw2 = Yee(self,self.file[4])  #Yee is the new class
            self.history = [self.file[4]] + self.history[:-1]
            self.wait_window(pw2)
            return
        def Lk5(self):
            if self.file[5] == "x.png":
                return
            pw2 = Yee(self,self.file[5])  #Yee is the new class
            self.history = [self.file[5]] + self.history[:-1]
            self.wait_window(pw2)
            return
        def Lk6(self):
            if self.file[6] == "x.png":
                return
            pw2 = Yee(self,self.file[6])  #Yee is the new class
            self.history = [self.file[6]] + self.history[:-1]
            self.wait_window(pw2)
            return

if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
