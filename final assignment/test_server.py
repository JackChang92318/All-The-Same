import socket
import time
import threading
import queue

HOST = ''
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(8)

connDict = {} # {key, value} => {socket, ((addr), (Recv), order)}
check = 0
GM = 0
chooseGM = False
event = threading.Event()

def sendA(client):
    global GM
    global chooseGM
    id = threading.get_ident()
    while True:
        try:
            # print('before recv1')
            event.wait()
            # print('before recv')
            data = client.recv(1024)
            print('Revc msg from ', id)
            outdata = 'Recv from ' + str(id) + ': ' + data.decode()
            connDict[client][1].put(outdata)
            global check
            check = check + 1
            if check == len(connDict):
                for key in connDict:
                    outdata = connDict[key][1].get()
                    for recver in connDict:
                        if recver != key:# 只送給別人，不要就拿掉
                            recver.sendto(outdata.encode(), connDict[recver][0])
                            print('Send', outdata,'to ', recver)
                GM = GM + 1
                GM = GM % len(connDict)
                print('GM = ', GM)
            chooseGM = False
            
            text = 'Number of player is ' + str(len(connDict))
            client.send(text.encode())
            print('send player number')
            
            time.sleep(1)
        except ConnectionResetError:
            print('Connection[addr: ', connDict[client], 
                  '] closed.(Current client: %d)'%(len(connDict)-1))
            connDict.pop(client)
            break
        
def sendQ(client):
    try:
        global chooseGM
        print('Select GM is OK')
        time.sleep(0.1)
        # print('before recv')
        data =  client.recv(1024)
        print('Get Question', data.decode())
        for clnt in connDict:
            outdata = 'Question: ' + data.decode()
            clnt.send(outdata.encode())
            print('Send Question to all')
            
            # text = 'Number of player is' + str(len(connDict))
            # clnt.send(text)
            # print('send player number')
        event.set()
    except:
        connDict.pop(client) # might be a problem, be careful
        print('Send Failed')

def choose():
    global GM
    global chooseGM
    new_dict = {v : k for k, v in connDict.items()}
    # new_dict = {(addr, msg, order) : socket}
    # => nd[key] = socket, connDict[nd[key]] = (addr, msg, order)
    for key in new_dict:
        # print(key)
        if connDict[new_dict[key]][2] == GM:# chooseGM == False: #  key[2] == GM and 
            # print()
            # print('****************%d****************'%key[2])
            # print()
            text = 'You are GM, now enter your question'
            # print('ok')
            # print(key)
            new_dict[key].send(text.encode())
            # GM += 1
            chooseGM = True
            sendQ(new_dict[key])

        else:
            # print('this is not gm')            
            text = 'Wait for question'
            new_dict[key].send(text.encode())
            print('text')

def main():
    while True:
        client, addr = s.accept()
        order = len(connDict)
        # print()
        # print(order)
        # print()
        connDict[client] = (addr, queue.Queue(), order)
        text = 'You are number ' + str(len(connDict))
        client.send(text.encode())
        print('New client with thread ID: %r and addr: '%(id,), connDict[client][0],
          'Current client: %d'%len(connDict))
        time.sleep(0.1)
        
        global chooseGM
        global GM
        print(connDict[client][2], ', ', GM)
        if chooseGM == False:
            t = threading.Thread(target=choose)
            t.start()
            chooseGM == True
            # t.join()
        
        t2 = threading.Thread(target = sendA, args=(client,))
        t2.start()
        global check
        check = 0

main()

# set gameNum...(O) -> *here* able to select gm...(X) -> get q...(O) ->
# send q...(O)-> recv ans...(O) -> *head+1

# Might use later:
# text = 'Number of player is' + str(len(connDict))
# new_dict[key].send(text.encode())
# print('send player number')