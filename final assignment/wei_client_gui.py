import socket
import threading
import time
from tkinter import *

# IP = '192.168.0.109'
IP = '172.26.43.148'
PORT = 6969
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((IP, PORT))
print("Connected to server.")

FORMAT = "utf-8"

ans_list = ["", "", "", "", "", ""]


class GUI:
    def __init__(self):
        self.Window = Tk()
        self.login_layout()
        
        # self.context = Label(self.Window,bg="#7D7D7D", state=HIDDEN)
        
        self.Window.mainloop()
    
    def login_layout(self):
        self.Window.title("這介面超漂亮")
        self.Window.configure(width=450,
                              height=600,
                              bg="deeppink")
        self.Window.resizable(False,False)
        
        self.labelhead = Label(self.Window,
                               bg="lime",
                               fg="blueviolet",
                               text="登入畫面",
                               font="Helvetica 13 bold",
                               pady=5)
        self.labelhead.place(relwidth=1,
                             rely=0)
        
        self.login_img = PhotoImage(file="login.png")
        self.login_text = Label(image=self.login_img).place(x = 95,y = 80)
        
        self.labeltitle = Label(self.Window,
                                bg="lime",
                                fg="blueviolet",
                                text="輸入你的名字",
                                font="Helvetica 13 bold",
                                pady=5)
        self.labeltitle.place(relwidth=0.5,
                              relx=0.25,
                              rely=0.4)
        
        self.EnterUserName = Entry(self.Window,
                                   width=20,
                                   bg="white",
                                   fg="blueviolet",
                                   font="Helvetica 25 bold")
        self.EnterUserName.place(relx=0.1,
                                 rely=0.5)
        self.EnterUserName.focus()
        
        
        self.SendLogin = Button(self.Window,
                                 text="我準備好了!!",
                                 font="Helvetica 10 bold",
                                 fg="blueviolet",
                                 width=20,
                                 bg="lime",
                                 command=lambda: self.sendReadyButton(self.EnterUserName.get()))
        self.SendLogin.place(relheight=0.1,
                              relwidth=0.25,
                              relx=0.38,
                              rely=0.7)
        
        self.ten_img = PhotoImage(file="10.png")
        self.ten_text = Label(image=self.ten_img).place(x = 75,y = 350)
    def sendReadyButton(self, msg):
        self.msg = msg
        self.EnterUserName.delete(0, END)
        message = self.msg
        
        s.send(msg.encode())                        # login(s)
        
        StartGame = "1"                             # send_StartMsg(s)
        s.send(StartGame.encode())
        
        self.Window.destroy()
        self.client()
    
    def client(self):
        self.Window = Tk()
        self.Window.title('全員一致')
        self.Window.geometry('1200x750')
        self.Window.resizable(width=False, height=False)
        self.Window.configure(bg='sandybrown')
        recv = threading.Thread(target=self.Recving)
        recv.start()

        
        self.ans_img = PhotoImage(file="ans.png") 
        self.ans_text = Label(image=self.ans_img).place(x = 300,y = 250)
        
        # player list
        self.name_img = PhotoImage(file="name.png") 
        self.PlayerList = Canvas(self.Window,
                                 width=240,
                                 height=750,
                                 bg="pink")
        self.PlayerList.place(relx=0,
                              rely=0)
        self.name_text = Label(image=self.name_img).place(x = 15,
                                                          y = 10)
        self.line = Label(self.Window,
                          height=750,
                          font="Helvetica 1",
                          bg='black')
        self.line.place(relx=0.2,
                        rely=0)
        
        # title:全員一致
        self.title = Canvas(self.Window,
                            width=960,
                            height=75)
        self.title.place(relx=0.205,
                         rely=0)
        self.title.create_text(480, 40, text='全員一致', font=('Arial', 30, 'bold'))
        self.titlelabel = Label(self.Window,
                                width=960,
                                # height=1,
                                font="Helvetica 1 bold",
                                bg='black')
        self.titlelabel.place(relx=0.2,
                              rely=0.1)
        
        self.AllTheSame_img = PhotoImage(file="AllTheSame.png") 
        self.AllTheSame_text = Label(image=self.AllTheSame_img).place(x = 300,y = -8)
        
        # 輸入區
        self.enterAnsBg = Label(self.Window,
                                bg='antiquewhite3')
        self.enterAnsBg.place(relwidth=0.8,
                              relheight=0.1,
                              relx=0.205,
                              rely=0.9)
        self.enterAns = Entry(self.enterAnsBg,
                              bg="cyan2",
                              fg="black",
                              font="Helvetica 30")
        self.enterAns.place(relwidth=0.875,
                            relheight=0.8,
                            relx=0.005,
                            rely=0.1)
        self.enterAns.focus()
        self.SendButton = Button(self.enterAnsBg,
                                 text="Send",
                                 bg="#00C957",
                                 font="Helvetica 25 bold",
                                 command=lambda: self.Sending(self.enterAns.get()))
        self.SendButton.place(relwidth=0.1,
                              relheight=0.8,
                              relx = 0.89,
                              rely=0.1)
        
        # 顯示題目區
        self.question = Label(self.Window,
                              bg="lightcyan")
        self.question.place(relwidth=0.4,
                            relheight=0.22,
                            relx=0.402,
                            rely=0.11)
        self.questionText = Text(self.question,
                                 bg="lightcyan",
                                 fg="black",
                                 width=31,
                                 font="Helvetica 20 bold")
        self.questionText.place(relx=0,
                                rely=0)
        self.questionText.config(state=DISABLED)
        
        
        # 兩個互動按鈕
        self.rightButton = Button(self.Window,
                                  font="Helvetica 25 bold",
                                  state=DISABLED,
                                  command=lambda: self.RightButton())
        self.rightButton.place(relwidth=0.17,
                               relheight=0.13,
                               relx=0.22,
                               rely=0.15)
        self.end_img = PhotoImage(file="END.png") 
        self.rightButton.config(image=self.end_img)
        
        self.leftButton = Button(self.Window,
                                  font="Helvetica 25 bold",
                                  state=DISABLED,
                                  command=lambda: self.LeftButton())
        self.leftButton.place(relwidth=0.17,
                               relheight=0.13,
                               relx=0.81,
                               rely=0.15)
        self.next_img = PhotoImage(file="NEXT.png") 
        self.leftButton.config(image=self.next_img)
        
        
        
        # 顯示回答區
        self.context = Label(self.Window,
                             bg="#7D7D7D",
                             font="Helvetica 25 bold")
        self.context.place(relwidth=0.798,
                           relheight=0.445,
                           relx=0.205,
                           rely=0.455)
        self.ans1 = Label(self.context,
                          bg="#008080")
        self.ans1.place(relwidth=0.3,
                        relheight=0.4625,
                        relx=0.01995,
                        rely=0.025)
        self.ans1Text = Text(self.ans1,
                             bg="#008080",
                             fg="black",
                             font="Helvetica 25 bold",
                             width=15)
        self.ans1Text.place(relx=0,
                            rely=0)
        self.ans1Text.config(state=DISABLED)
        
        
        self.ans2 = Label(self.context,
                          bg="#008080")
        self.ans2.place(relwidth=0.3,
                        relheight=0.4625,
                        relx=0.3433,
                        rely=0.025)
        self.ans2Text = Text(self.ans2,
                             bg="#008080",
                             fg="black",
                             font="Helvetica 25 bold",
                             width=15)
        self.ans2Text.place(relx=0,
                            rely=0)
        self.ans2Text.config(state=DISABLED)
        
        self.ans3 = Label(self.context,
                          bg="#008080")
        self.ans3.place(relwidth=0.3,
                        relheight=0.4625,
                        relx=0.6798,
                        rely=0.025)
        self.ans3Text = Text(self.ans3,
                             bg="#008080",
                             fg="black",
                             font="Helvetica 25 bold",
                             width=15)
        self.ans3Text.place(relx=0,
                            rely=0)
        self.ans3Text.config(state=DISABLED)

        
        self.ans4 = Label(self.context,
                          bg="#008080")
        self.ans4.place(relwidth=0.3,
                        relheight=0.4625,
                        relx=0.01995,
                        rely=0.52)
        self.ans4Text = Text(self.ans4,
                             bg="#008080",
                             fg="black",
                             font="Helvetica 25 bold",
                             width=15)
        self.ans4Text.place(relx=0,
                            rely=0)
        self.ans4Text.config(state=DISABLED)

        
        self.ans5 = Label(self.context,
                          bg="#008080")
        self.ans5.place(relwidth=0.3,
                        relheight=0.4625,
                        relx=0.3433,
                        rely=0.52)
        self.ans5Text = Text(self.ans5,
                             bg="#008080",
                             fg="black",
                             font="Helvetica 25 bold",
                             width=15)
        self.ans5Text.place(relx=0,
                            rely=0)
        self.ans5Text.config(state=DISABLED)

        
        self.ans6 = Label(self.context,
                          bg="#008080")
        self.ans6.place(relwidth=0.3,
                        relheight=0.4625,
                        relx=0.6798,
                        rely=0.52)
        self.ans6Text = Text(self.ans6,
                             bg="#008080",
                             fg="black",
                             font="Helvetica 25 bold",
                             width=15)
        self.ans6Text.place(relx=0,
                            rely=0)
        self.ans6Text.config(state=DISABLED)
                
        
        self.Window.mainloop()
    
    def Sending(self, msg):
        self.msg = msg
        self.enterAns.delete(0, END)
        message = self.msg
        s.send(message.encode())
    
    def Recving(self):
        playnum = 0
        while True:
            message = s.recv(1024).decode()
            print('print: ', message)
            if message[0:19] == 'Number of player is':
                num = int(message[20:])
                playnum = num
                y = 100
                for i in range(num):
                    msg = s.recv(1024).decode()
                    self.PlayerList.create_text(25, y, 
                                                text=msg[0:5],
                                                anchor='nw',
                                                font=('Arial', 30, 'bold'))
                    self.PlayerList.create_text(25, y+40, 
                                                text=msg[5:],
                                                anchor='nw',
                                                font=('Arial', 30, 'bold'))
                    self.PlayerList.create_line(15, y+90, 
                                                230, y+90, 
                                                width=5, fill='black', dash=(10,3))
                    y += 130

            elif message == 'GM':
                self.questionText.config(state=NORMAL)
                self.questionText.delete("1.0","end")
                text = "你是這回合的主持人(提問者)， \n請輸入問題"
                self.questionText.insert(END,text+"\n\n")
                self.questionText.config(state=DISABLED)
                self.questionText.see(END)
                
                # send question
            elif message == 'NOT GM':
                self.questionText.config(state=NORMAL)
                self.questionText.delete("1.0","end")
                text = "請等待主持人發問"
                self.questionText.delete("1.0","end")
                self.questionText.insert(END,text+"\n\n")
                self.questionText.config(state=DISABLED)
                self.questionText.see(END)
                
            elif message[0:10] == 'Question: ':
                self.questionText.config(state=NORMAL)
                self.questionText.delete("1.0","end")
                self.questionText.insert(END,"問題: "+ message[10:] +"\n\n")
                self.questionText.insert(END,"請輸入回答"+"\n")
                self.questionText.config(state=DISABLED)
                self.questionText.see(END)
                
            elif message == "Thanks for playing":
                self.questionText.config(state=NORMAL)
                self.questionText.delete("1.0","end")
                self.questionText.insert(END,"!!!全員一致!!!"+"\n\n")
                time.sleep(1)
                self.questionText.delete("1.0","end")
                self.questionText.insert(END,"數秒後自動關閉")
                self.questionText.config(state=DISABLED)
                self.questionText.see(END)
                time.sleep(3)
                
                self.final_img = PhotoImage(file="endpage.png") 
                self.final_text = Label(image=self.final_img).place(x = 0,y = 0)

                time.sleep(3)
                
                self.Window.destroy()
            # 1200*750
            elif message == "Next round":
                self.questionText.config(state=NORMAL)
                self.questionText.delete("1.0","end")
                self.questionText.insert(END,message+"\n\n")
                self.questionText.config(state=DISABLED)
                self.questionText.see(END)
            
            elif message == "wait for others":
                self.questionText.config(state=NORMAL)
                self.questionText.insert(END,"等待其他玩家回答"+"\n\n")
                self.questionText.config(state=DISABLED)
                self.questionText.see(END)
                
            else:
                # self.questionText.insert(END,message+"\n\n")
                
                ans_list[0] = message
                for i in range(1,playnum):
                    msg = s.recv(1024).decode()
                    ans_list[i] = msg
                
                self.questionText.config(state=NORMAL)
                self.questionText.delete("2.0","end")
                self.questionText.see(END)
                self.questionText.config(state=DISABLED)
                
                
                self.questionText.config(state=NORMAL)
                self.questionText.insert(END,"\n\n" + "所有人均回答完畢，三秒後顯示所有人答案"+"\n\n")
                time.sleep(1)
                self.questionText.delete("2.0","end")
                self.questionText.see(END)
                self.questionText.config(state=DISABLED)
                
                
                self.questionText.config(state=NORMAL)
                self.questionText.insert(END,"\n\n" + "所有人均回答完畢，二秒後顯示所有人答案"+"\n\n")
                time.sleep(1)
                self.questionText.delete("2.0","end")
                self.questionText.see(END)
                self.questionText.config(state=DISABLED)
                
                self.questionText.config(state=NORMAL)
                self.questionText.insert(END,"\n\n" + "所有人均回答完畢，一秒後顯示所有人答案"+"\n\n")
                time.sleep(1)
                self.questionText.delete("2.0","end")
                self.questionText.see(END)
                self.questionText.config(state=DISABLED)
                
                self.questionText.config(state=NORMAL)
                self.questionText.insert(END,"\n\n" + "公布大家的答案"+"\n\n")
                time.sleep(1)
                self.questionText.delete("2.0","end")
                self.questionText.see(END)
                self.questionText.config(state=DISABLED)
                
                
                self.ans1Text.config(state=NORMAL)  
                self.ans1Text.delete("1.0","end")
                self.ans1Text.insert(END,ans_list[0])
                self.ans1Text.config(state=DISABLED)
                
                self.ans2Text.config(state=NORMAL)
                self.ans2Text.delete("1.0","end")
                self.ans2Text.insert(END,ans_list[1])
                self.ans2Text.config(state=DISABLED)
                
                self.ans3Text.config(state=NORMAL)
                self.ans3Text.delete("1.0","end")
                self.ans3Text.insert(END,ans_list[2])
                self.ans3Text.config(state=DISABLED)
                
                self.ans4Text.config(state=NORMAL)
                self.ans4Text.delete("1.0","end")
                self.ans4Text.insert(END,ans_list[3])
                self.ans4Text.config(state=DISABLED)
                
                self.ans5Text.config(state=NORMAL)
                self.ans5Text.delete("1.0","end")
                self.ans5Text.insert(END,ans_list[4])
                self.ans5Text.config(state=DISABLED)
                
                self.ans6Text.config(state=NORMAL)
                self.ans6Text.delete("1.0","end")
                self.ans6Text.insert(END,ans_list[5])
                self.ans6Text.config(state=DISABLED)
                
                # playnum = 0
                
                time.sleep(10)
                self.questionText.config(state=NORMAL)
                
                text = "\n\n" + "下一輪請按NEXT，\n結束遊戲請按END"
                self.questionText.insert(END,text+"\n\n")
                
                
                self.rightButton.config(state=NORMAL)
                self.leftButton.config(state=NORMAL)

                self.questionText.config(state=DISABLED)
                self.questionText.see(END)
    def RightButton(self):
        s.send("end".encode())
        self.rightButton.config(state=DISABLED)
        self.leftButton.config(state=DISABLED)
        
        
        self.ans1Text.config(state=NORMAL)  
        self.ans1Text.delete("1.0","end")
        self.ans1Text.config(state=DISABLED)
        
        self.ans2Text.config(state=NORMAL)  
        self.ans2Text.delete("1.0","end")
        self.ans2Text.config(state=DISABLED)
        
        self.ans3Text.config(state=NORMAL)  
        self.ans3Text.delete("1.0","end")
        self.ans3Text.config(state=DISABLED)
        
        self.ans4Text.config(state=NORMAL)  
        self.ans4Text.delete("1.0","end")
        self.ans4Text.config(state=DISABLED)
        
        self.ans5Text.config(state=NORMAL)  
        self.ans5Text.delete("1.0","end")
        self.ans5Text.config(state=DISABLED)
        
        self.ans6Text.config(state=NORMAL)  
        self.ans6Text.delete("1.0","end")
        self.ans6Text.config(state=DISABLED)
        
                
    def LeftButton(self):
        s.send("1".encode())
        self.leftButton.config(state=DISABLED)
        self.rightButton.config(state=DISABLED)
        
        
        self.ans1Text.config(state=NORMAL)
        self.ans1Text.delete("1.0","end")
        self.ans1Text.config(state=DISABLED)
        
        self.ans2Text.config(state=NORMAL)  
        self.ans2Text.delete("1.0","end")
        self.ans2Text.config(state=DISABLED)
        
        self.ans3Text.config(state=NORMAL)  
        self.ans3Text.delete("1.0","end")
        self.ans3Text.config(state=DISABLED)
        
        self.ans4Text.config(state=NORMAL)  
        self.ans4Text.delete("1.0","end")
        self.ans4Text.config(state=DISABLED)
        
        self.ans5Text.config(state=NORMAL)  
        self.ans5Text.delete("1.0","end")
        self.ans5Text.config(state=DISABLED)
        
        self.ans6Text.config(state=NORMAL)  
        self.ans6Text.delete("1.0","end")
        self.ans6Text.config(state=DISABLED)
                
g = GUI()   