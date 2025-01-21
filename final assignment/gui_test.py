import socket
import threading
import random
from tkinter import *

#與server建立連線
SERVER = "25.33.100.39"
PORT = 5055
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)

class GUI:
    def __init__(self):      

        self.Window = Tk()
        name = 'user-'+str(random.randint(1,100)) #name數字隨機決定
        self.layout(name)
        
        #建立新thread處理接收資料，才不會卡住
        rcv = threading.Thread(target=self.receive)
        rcv.start()

        self.Window.mainloop()        


    def layout(self, name):
        self.name = name

        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name, 
                               font="Helvetica 13 bold",
                               pady=5)  #元件上下的空間
        self.labelHead.place(relwidth=1)
        
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9") 
        self.line.place(relwidth=1, #相對主視窗的寬度
                        rely=0.07, #相對主視窗的y座標
                        relheight=0.012) #相對主視窗的寬度
 
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5, #元件左右的空間
                             pady=5) 
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
 
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80) 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)  #相對主視窗的x座標
        self.entryMsg.focus()
 

        self.buttonMsg = Button(self.labelBottom,
                            text="Send",
                            font="Helvetica 10 bold",
                            width=20,
                            bg="#ABB2B9",
                            #將輸入區的文字，交由sendButton()處理
                            command=lambda: self.sendButton(self.entryMsg.get())) 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")
 
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1,
                        relx=0.974) 
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)#對話區不許變更
 
    #建立新thread處理接收訊息
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
 
                #初次連線，server會送來'NAME'，client會回傳自己的name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else: 
                    #之後，server送來的訊息，都會印至對話區
                    self.textCons.config(state=NORMAL) #對話區許可加入
                    self.textCons.insert(END,message+"\n\n") #END為對話區的輸入點
                    self.textCons.config(state=DISABLED)#對話區不許變更
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                client.close()
                break
    #按下send按紐
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)#對話區不許變更
        self.msg = msg
        self.entryMsg.delete(0, END)#將輸入區清空
        message = (f"{self.name}: {self.msg}")
        client.send(message.encode(FORMAT))      

g = GUI()
