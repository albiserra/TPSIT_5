from pickle import TRUE
import socket as sck
from threading import Thread

address = ('192.168.1.129',8000)
isRunning = True

s_client = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

class Client(Thread):
        def __init__(self, s = s_client):
            Thread.__init__(self)
            self.s_client = s
        def run(self):
            global isRunning
            s_client.connect(address)

            while isRunning:
                print(s_client.recv(4096).decode())


def main():
    global isRunning
    client = Client()
    client.start()
    while isRunning:
        mex = input("1 AVANTI 2 DESTRA 3 SINISTRA 4 INDIETRO")
        if (mex == "exit"):
            isRunning = False
            break
            
        s_client.sendall(mex.encode())
    s_client.close()

if __name__=="__main__":
    main()