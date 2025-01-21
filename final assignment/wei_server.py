import socket
import time
import threading

HOST = ''
PORT = 6969

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

clnt_dict = {}
clnt_ans = {}
clnt_name = {}
clnt_GM = {}
clnt_end = {}

clntNum = 1
ReadyPlayer = int(0)
GM_Now = 1
ContinueGame = 1

event_ready = threading.Event()
event_GM = threading.Event()
event_sendAllAns = threading.Event()
event_recv_send_ans = threading.Event()
event_recv_ans = threading.Event()
event_ans_same_or_not = threading.Event()
event_next_round_or_not  = threading.Event()

def clnt_conn(s,):                      # step 1st
    global clntNum
    while True:
        if ReadyPlayer == len(clnt_dict) and len(clnt_dict) != 0:
            print("break loop")
            break
        else:
            try:
                clnt ,addr = s.accept()

                print("Client",addr,"is connected.")
                if clnt not in clnt_dict:
                    clnt_dict[(addr,clntNum)] = clnt

                    clnt_GM[addr] = clntNum
                    clntNum += 1
                    login = threading.Thread(target=login_msg,args=(clnt,addr))
                    login.start()
                    ready = threading.Thread(target=ready_msg,args=(clnt,addr))
                    ready.start()
            except ConnectionResetError:
                print("clnt conn error")
                
def login_msg(clnt,addr):               #step 2nd
    
    try:
        userName = clnt.recv(1024).decode()
        clnt_name[addr] = userName
        
        print(addr,"name is",userName)
        event_ready.set()
    except ConnectionResetError:
        print("clnt ",addr,"conn error")
        clnt_dict.pop(addr)
        
def ready_msg(clnt,addr):               # step 3nd
    
    try:
        event_ready.wait()
        event_ready.clear()
        global ReadyPlayer
        IAmReady = clnt.recv(1024).decode()
        if IAmReady == "1":
            ReadyPlayer += 1
            print(ReadyPlayer,"player is ready")

        time.sleep(1)
    except ConnectionResetError:
        print("clnt ",addr,"conn error")
        clnt_dict.pop(addr)
        


def send_player_data():                 # step 4th

    number_of_player = 'Number of player is ' + str(len(clnt_dict))
    print("number_of_player:",number_of_player)
    
    for addr in clnt_dict:
        clnt_dict[addr].send(number_of_player.encode())
    
    for addr_i in clnt_dict:
        for addr_j in clnt_name:
            clnt_dict[addr_i].send(clnt_name[addr_j].encode())
            time.sleep(0.15)

    print("wait for 2 sec")
    time.sleep(2)
    event_GM.set()
    
    
def select_gm():                        #step 5th
    global GM_Now
    event_GM.wait()
    event_GM.clear()

    for addr in clnt_dict:
        if GM_Now == clnt_GM[addr[0]]:
            print("GM:",GM_Now,"clnt",clnt_GM[addr[0]])
            clnt_dict[addr].send("GM".encode())
            print("send (GM) to", addr)
        else:
            clnt_dict[addr].send("NOT GM".encode())
            print("GM:",GM_Now,"clnt",clnt_GM[addr[0]])
            print("send (NOT GM) to", addr)

    event_recv_send_ans.set()


def recv_send_question():               # step 6th
    event_recv_send_ans.wait()
    event_recv_send_ans.clear()
    global GM_Now
    for addr in clnt_dict:
        if GM_Now == addr[1]:
            ques = clnt_dict[addr].recv(1024).decode()
            print("Question:",ques)
    
    if GM_Now < len(clnt_dict):
        GM_Now += 1
    else:
        GM_Now = 1

    for addr in clnt_dict:
        text = 'Question: ' + ques
        clnt_dict[addr].send(text.encode())
        print("send Q to",addr)

    event_recv_ans.set()
    
def recv_ans_init():                    # step 7th
    event_recv_ans.wait()
    event_recv_ans.clear()
    for addr in clnt_dict:
        threading.Thread(target=recv_ans,
                         args=(clnt_dict[addr],addr)).start()
        threading.Thread(target=ans_same_or_not,
                         args=(clnt_dict[addr],addr)).start()
        

def recv_ans(clnt,addr):            # step 7-1th
    
    print(clnt,addr)
    clnt.setblocking(False)
    while True:
        try:
            ans = clnt.recv(1024).decode()
            clnt_ans[addr] = ans
            print(addr,"ans is",ans)
            

            if (len(clnt_dict) == len(clnt_ans.keys())): # and (len(clnt_ans.keys()) != 0)
                clnt.setblocking(True)
                event_sendAllAns.set()
                print("break1")
                break

            if clnt_ans[addr]:
                clnt.setblocking(True)
                text = "wait for others"
                clnt.send(text.encode())
                print(text)
                print("break2")
                break
        except:
            pass
            # print("pass")
        time.sleep(0.5)
        

def ans_same_or_not(clnt,addr):             # step 7-2th

    # global EndGame
    event_ans_same_or_not.wait()
    event_ans_same_or_not.clear()

    print("same active")
    clnt.setblocking(False)

    while True:
        # print("loop")
        try:
            ans_is_same_or_not = clnt.recv(1024).decode()
            print("recv:",ans_is_same_or_not)
            clnt_end[addr] = ans_is_same_or_not

            if (len(clnt_dict) == len(clnt_end)):
                clnt.setblocking(True)
                event_next_round_or_not.set()
                print("break1")
                break

            if clnt_end[addr]:
                clnt.setblocking(True)
                print("break2")
                break

        except:
            # print("pass")
            pass

        time.sleep(0.5)

    time.sleep(3)



def send_all_ans():                     # step 8th
    

    event_sendAllAns.wait()
    event_sendAllAns.clear()
    

    # number_of_player = str(len(clnt_dict))
    # print("number_of_player:",number_of_player)
    # text = 'Num of player ' + number_of_player
    # for addr in clnt_dict:
    #     clnt_dict[addr].send(text.encode())

    print("send all ans")

    for addr_i in clnt_dict:
        for addr_j in clnt_ans:
            # Ans =  clnt_name[addr_j]+ ": " +clnt_ans[addr_j]
            Ans = clnt_ans[addr_j]
            clnt_dict[addr_i].send(Ans.encode())
            time.sleep(0.15)
            print("send",Ans,"to",addr_i)
            # time.sleep(0.5)

    for addr in clnt_dict:
        clnt_ans.pop(addr)
    
    time.sleep(1)
    event_ans_same_or_not.set()
    print("check")
    #event_GM.set()
    

def next_round_or_not():            # step 9th

    event_next_round_or_not.wait()
    event_next_round_or_not.clear()

    global ContinueGame
    c = 0

    for addr in clnt_end:
        if clnt_end[addr] == "end":
            c += 1
    
    if c == len(clnt_dict):
        ContinueGame = 0
        for addr in clnt_dict:
            clnt_dict[addr].send("Thanks for playing".encode())
    else:
        ContinueGame = 1
        for addr in clnt_dict:
            clnt_dict[addr].send("Next round".encode())
        event_GM.set()

    for addr in clnt_dict:
        clnt_end.pop(addr)

    time.sleep(5)


def main():
    global ContinueGame

    WaitConn = threading.Thread(target=clnt_conn,args=(s,))
    WaitConn.start()
    
    while True:
        if (ReadyPlayer == len(clnt_dict)) and (len(clnt_dict) != 0):
            print("everyone is ready")
            break
        time.sleep(0.5)

    send_player_data()
    # threading.Thread(target=send_player_data)
    # rnd = 1

    # event_GM.set()

    while ContinueGame:

        threading.Thread(target=select_gm).start()

        threading.Thread(target=recv_send_question).start()

        recv_ans_init()

        threading.Thread(target=send_all_ans).start()

        threading.Thread(target=next_round_or_not).start()

    t = input("end")
        
main()