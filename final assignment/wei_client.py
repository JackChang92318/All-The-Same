import socket
import threading
import time
from tkinter import *
from tkinter import font
from tkinter import ttk


IP = '172.26.43.148'
PORT = 6969
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((IP, PORT))
print("Connected to server.")

GM = False
ContinueGame = 1

ans_list = []
event_login = threading.Event()

class GUI:
    # chat window which is currently hidden
    def __init__():
        Window = Tk()
        Window.withdraw()

    # login window
        login = Toplevel()
        # set the title
        login.title("Login")
        login.resizable(width=False,height=False)
        login.configure(width=400,height=300)
        login.iconbitmap('icon.bmp')

    # create a Label
        pls = Label(login,text="Please login to continue",justify=CENTER,font="Helvetica 14 bold")
        pls.place(relheight=0.15,relx=0.2,rely=0.07)



def login(s):                           # step 0th
    print("enter your name to login")
    Name = input()
    userName = Name.encode()
    print("your name is:", Name)
    s.send(userName)



def send_StartMsg(s):                   # step 1st
    StartGame = input().encode()
    s.send(StartGame)
    print("!!!Game Start!!!")
    
    
def recv_player_data(s):                # step 2nd
    indata = s.recv(1024).decode()
    number_of_player = int(indata)
    print("There are",number_of_player,"player")

    for i in range(number_of_player):
        player = s.recv(1024).decode()
        print("({})player:{}".format(i+1,player))
        # time.sleep(0.3)


def recv_gm(s):                         # step 3rd
    # print("check")
    GM_or_not = s.recv(1024).decode()
    # print(GM_or_not)
    if GM_or_not == '0':
        print("you are <not> GM for this round ,please wait")

    elif GM_or_not == '1':
        print("you are GM for this round ,please enter your question")
        ques = input()
        sendQues = ques.encode()
        s.send(sendQues)
        print("send",ques)


def recv_ques(s):                   # step 4th
    question = s.recv(1024).decode()
    print("Question is:",question)
    
    
def send_ans(s):                    # step 5th
    print("send your ans")
    ans = input()
    s.send(ans.encode())
    print("(send_ans):",ans)
    
    
def recv_ans(s,):                   # step 6th
    indata = s.recv(1024).decode()
    number_of_player = int(indata)
    # print("There are",number_of_player,"ans")
    # print("wait for 2 sec")
    # time.sleep(2)
    
    for _ in range(number_of_player):
        ans = s.recv(1024).decode()
        ans_list.append(ans)
        # print("(ans({})):{}",format(i+1,ans))
        time.sleep(0.5)

    print("all players ans is ready wait 3 sec to show all ans")
    time.sleep(3)

    for i in range(len(ans_list)):
        print("(ans({})):{}".format(i+1,ans_list[i]))

    ans_list.clear()


def next_round_or_not(s):               # step 7th
    global ContinueGame
    print("if all ans is the same, press (0) to end the game,if not,press (1) to continue")
    NextRound = input()
    s.send(NextRound.encode())

    indata = s.recv(1024).decode()
    if indata == "0":
        ContinueGame = 0
        print("end the game in 5 sec")
        time.sleep(5)
        # s.close()
    else:
        ContinueGame = 1
        print("wait 5 sec for next round")
        time.sleep(5)

    




def main():
    try:
        login(s)
        print("if everyone ready to join the game press (1)")
        send_StartMsg(s)

        recv_player_data(s)
        rnd = 1
        while rnd <= 5:
            # print("check")
            recv_gm(s)
            recv_ques(s)
            send_ans(s)
            recv_ans(s)
            next_round_or_not(s)

            #print("wait 5 sec for next round")
            # time.sleep(5)

        t = input("game end")

    except:
        
        t = input("something error")

main()