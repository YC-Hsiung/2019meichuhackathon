import tkinter as tk
import os
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import *
from PIL import ImageTk, Image

file_path = ''
#dealing with open file

# 彈窗1: stored 
class Adding(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('Soup Head Saver')
        self.parent = parent # 顯式地保留父視窗
        self.iconbitmap("bear.ico")
        self.geometry("800x400")
        self.file_path = ""
        self.r = ""
        mf = Frame(self)
        mf.pack()
        f1 = Frame(mf, width=600, height=250)
        f1.pack(fill=X)
        f2 = Frame(mf, width=600, height=250)
        f2.pack()
        Label(f1,text="Select Element's Image").grid(row=0, column=0, sticky='e')
        Button(f1, text="Browse", command=self.open_file).grid(row=0, column=1, sticky='ew', padx=8, pady=4)
        Label(f2,text="You Selected: ").grid(row=1, column=0, sticky='e')
        self.l1 = Label(f2,text = self.file_path)
        self.l1.grid(row = 1,column = 1,sticky = 'e')
        # 第三行
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="取消", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row3, text="確定", command=self.ok).pack(side=tk.RIGHT)
        row4 = tk.Frame(self)
        row4.pack(fill="x")

        self.l2 = Label(row4,text = self.r)
        self.l2.pack(side = tk.LEFT)
        self.l2.config(font = "Arial 13", fg = "Red")
    def result(self,INPUTFILE):  
        return False
    def ok(self):
        if(self.result(self.file_path) == False):
            self.l2.config(text = "Oops! There are no information in the given PDF file :(")
        else:
            pass
    def cancel(self):
        self.destroy() 

    def open_file(self):
        filename = askopenfilename()
        infile = open(filename, 'r')
        self.file_path = os.path.dirname(filename)
        self.file_path += filename
        print('cool:',self.file_path)
        self.l1.config(text = self.file_path)
        return  
class Store(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('Soup Head Saver')
        self.parent = parent # 顯式地保留父視窗
        self.iconbitmap("bear.ico")
        self.geometry("800x400") 


 
    def ok(self):
        pass
    def cancel(self):
        self.destroy()  


# 主窗
class MyApp(tk.Tk):
        def __init__(self):
            super().__init__()
            self.iconbitmap("bear.ico")
            self.geometry("800x400")
            # self.pack() # 若繼承 tk.Frame，此句必須有！！！
            self.title('Soup Head Saver')
            # 程式引數
            
            self.name = '張三'
            self.age = 30
            # 程式介面
            self.setupUI()
        def setupUI(self):
        # 第一行（兩列）
            row1 = tk.Frame(self)
            row1.pack(fill="x")
            tk.Label(row1, text='Soup Head Saver', width=100, fg = "blue",font = "Arial 20").pack()

            self.l1 = tk.Label(row1, text="Save Your Time and Soup!", width=160)
            self.l1.config(font = "Arial 13",fg = "brown")
            self.l1.pack(side=tk.LEFT)
            # 第二行
            row2 = tk.Frame(self)
            row2.pack(fill="x")
            self.br = tk.Label(row2,text = "")
            self.br.pack()           
            #第三行
            row3 = tk.Frame(self)
            row3.pack(fill="x")
            self.bt = tk.Button(row3, text="Stored Element",height = 5, width=50,command = self.store)
            self.bt.pack(side = tk.LEFT)
            self.bt.config(bg = "skyblue")
            self.bt2 = tk.Button(row3, text="ADD Element", height = 5,width=50,command = self.adding)
            self.bt2.pack(side = tk.RIGHT)
            self.bt2.config(bg = "pink")
            # 第二行
            row2 = tk.Frame(self)
            row2.pack(fill="x")
            self.br = tk.Label(row2,text = "")
            self.br.pack()           
            # 第二行
            row2 = tk.Frame(self)
            row2.pack(fill="x")
            self.br = tk.Label(row2,text = "")
            self.br.pack()           
            # 第二行
            row2 = tk.Frame(self)
            row2.pack(fill="x")
            self.br = tk.Label(row2,text = "")
            self.br.pack()           
            #功能說明
            self.fu = tk.Label(row2,text = "Press Stored Element to check the stored element's information"+'\n'+"Press ADD Element to add and browse new element's information"+'\n'+'\n'+'\n')
            self.fu.config(font = "Arial 13")
            self.fu.pack()           

            self.bt10 = tk.Button(row2,text="Quit",height = 1, width=10,command = self.leave)
            self.bt10.config(bg = "grey")
            self.bt10.pack(side = tk.RIGHT)
            
        def leave(self):
            self.destroy()    
            
        def store(self):
            pw = Store(self)
            self.wait_window(pw) # 這一句很重要！！！
            return
        def adding(self):
            pw2 = Adding(self)
            self.wait_window(pw2) # 這一句很重要！！！            
            return

if __name__ == '__main__':
    app = MyApp()
    app.mainloop()