import socket
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def init_setting(s):
    HOST = '127.0.0.1'
    PORT = 6968
    s.connect((HOST, PORT))
    s.setblocking(False)
    print("Connected to server.")
    
def recv_msg(s,):
    while True:
        try:
            indata = s.recv(1024).decode()
            print("(recv):",indata)
        except:
            pass
        time.sleep(0.5)

def send_msg(s):
    outdata = input()
    s.send(outdata.encode())
    print("(send):",outdata)

def send_ans(s):
    ans = input()
    s.send(ans.encode())
    print("(send_ans):",ans)
    
init_setting(s)
threading.Thread(target=recv_msg,args=(s,)).start()

while True:
    try:
        # send_msg(s)
        send_ans(s)
    except:
        print("something is wrong")
        continue