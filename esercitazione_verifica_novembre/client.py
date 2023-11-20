import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 8000))

def main():
    mess = input("Inserire la query")#input messaggio
    while mess != "exit":#ciclo finchè il messaggio è diverso da exit
        mess = mess.encode()#codifica messaggio
        s.sendall(mess)#invio messaggio
        ricevuto = s.recv(4096).decode()#ricezione risposta
        print(ricevuto)
        mess = input("Inserire messaggio")
    s.close()

if __name__ == "__main__":
    main()