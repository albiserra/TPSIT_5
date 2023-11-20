import socket
from threading import Thread, Lock

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8000))

tris = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
mutex = Lock()
pedina = 1

def fine():
    global tris
    if (tris[1] != 0) and (tris[2] != 0) and (tris[3] != 0) and (tris[4] != 0) and (tris[5] != 0) and (tris[6] != 0) and (tris[7] != 0) and (tris[8] != 0) and (tris[9] != 0):
        return True
    else:
        return False

class Server(Thread):
    def __init__(self, conn, id):
        Thread.__init__(self)
        self.conn = conn
        self.id = id

    def run(self):
        global tris
        global pedina
        while not fine():
            if pedina == self.id:
                self.conn.sendall("inserire posizione".encode())
                pos = self.conn.recv(4096).decode()
                while tris[int(pos)] != 0:
                    self.conn.sendall("inserire posizione".encode())
                    pos = self.conn.recv(4096).decode()
                tris[int(pos)] = self.id
                print(tris)
                if self.id == 1:
                    pedina = 2
                else:
                    pedina = 1



def main():
    lista_thread = []
    cont = 1
    try:
        while cont<=2:#ciclo per accettare le connessioni
            s.listen()
            conn, address = s.accept()
            server = Server(conn, cont)#dichiaro il nuovo oggeto thread
            lista_thread.append(server)#aggiungo l'oggetto alla lista che utilizzerò per chiudere tutti i thread
            server.start()#faccio partire il thread
            print("start thread")
            cont+=1
        
    except KeyboardInterrupt:#se utilizzo keyboard interrupt
        for i in lista_thread:#ciclo per chiudere tutti i thread
            i.join()
        s.close()#chiudo il socket
        print("Chiusura")

if __name__ == "__main__":
    main()