import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 8000))

def main():
    while True:
        ricevuto = s.recv(4096).decode()
        mess = input("Inserire messaggio")
        mess = mess.encode()#codifica messaggio
        s.sendall(mess)#invio messaggio
    s.close()

if __name__ == "__main__":
    main()