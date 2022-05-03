from xml.dom import minidom
import xml.etree.ElementTree as ET
import requests,json,os,boto3
from xml.dom.minidom import Node
import funzioni
import tkinter as tk
from tkinter import *
from tkinter import filedialog
f1 = funzioni.func()
url =  " https://hn36l3ei1m.execute-api.us-east-1.amazonaws.com/fase_tgv/lambda_tgv"
tempoX = 1100

def leggi_file():
    root = tk.Tk()
    root.title("Inserisci file XML")
    root.config(bg="white") 
    width = 460
    height = 260
    root.geometry("460x260")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)

    def inserisci():
            global frame_x
            frame_x = Frame(root, bg="white")
            frame_x.pack(side=TOP, pady=60)
            btn = Button(frame_x, text="INSERISCI FILE XML", font=('arial', 18), width=30, bg="red", command=openFile)
            btn.grid(row=4, columnspan=2, pady=20)
    def openFile():
            tk.Tk().withdraw()
            filepath = filedialog.askopenfilenames(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                            title="Open file okay?",
                                            filetypes= (("File di origine XML","*.xml"),
                                            ("all files",".")))
            filepath = str(filepath)
            filepath = filepath[2:len(filepath)-3]
            datasource = open(filepath)
            #dom = minidom.parse(datasource)
            
            #print(dom.getElementsByTagName('Name')[0].firstChild.data)
            root.destroy()
            tree = f1.writer(datasource)
            files = {'file': open('risultatoParziale.xml', 'rb')}
            headers ={'jwt_token':'TGVsecret'}
            r = requests.post(url, files=files, headers=headers)
            print(r)
            #f1.elabora_xml(dom)    
    inserisci()
    if __name__ == "__main__":
        root.mainloop()
leggi_file()    





