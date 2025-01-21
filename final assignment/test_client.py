import socket
import threading
import time
import select

host = '127.0.0.1'
port = 7000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((host, port))
# s.setblocking(False)
print('Connected...')

# 傳送給server並且接收就好

def SendQues():
    data = input('My question: ')
    s.send(data.encode())
    Recv()
    # print('Send question: ', data)

def Recv():
    # print('1')
    data = s.recv(1024).decode()
    # print('2')
    print(data)
    if data == 'You are GM, now enter your question': # if you are GM
        SendQues()
        # print('Send question: ', data)
    elif data == 'Wait for question': # if you are not
        print(data)
    elif data[0:11] == 'Question: ': # everyone get this
        print(data)
    elif data[0:19] == 'Number of player is':
        print(data)
        global playerNum
        num = data[19:]
        playerNum = int(num)
        # Recv()

def sendAns():
    data = input('Enter your answer: ')
    outdata = data.encode()
    s.send(outdata)

indata = [s]

while True:
    Recv()
    
    Recv()
    print('Step one: Send question and recv if you are GM, recv question if you are not')
    
    sendAns()
    
    indata = s.recv(1024).decode()
    data = int(indata[20:])
    print(data)
    
    for i in range(data):
        print('Enter loop')
        msg = s.recv(1024).decode()
        print(msg)
    
    # Recv()
    # print('Step two: Send answer')
    # indata = s.recv(1024).decode()
    # data = indata[20:]
    # print('Number of player is ', data)
    # sendAns()
    # for i in range(playerNum-1):
    #     indata = s.recv(1024)
    #     data = indata.decode()
    #     print(data)
    #     print('Step three: Get all answer')


# Might use later
# sd = threading.Thread(target = sending), sd.start()

# problem(1) can't change gm
# know who is GM -> (send question) -> send Ans -> *head