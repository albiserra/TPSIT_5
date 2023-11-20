import socket
import sqlite3
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8000))

class Server(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            mess =  self.conn.recv(4096).decode()#leggo il messaggio in entrata e lo decodifico
            if mess[0] == '1':
                conSQL = sqlite3.connect("file.db")#connessione al db
                cur = conSQL.cursor()
                list = mess.split(';') #split per ottenere le info da cercare
                list[1] = "'" + list[1] + "'"#aggiungole ' al nome file
                print(list[1])
                
                try:
                    research = cur.execute(f"SELECT * FROM files WHERE nome = {list[1]}")
                    #ricerca presenza di un file
                    db_info = research.fetchall()[0][0]
                except:#se il file nonviene trovato entra in except
                    db_info = "Non trovato"
                
                conSQL.close()
                db_info = str(db_info)
                if db_info != "Non trovato":#se è diverso da non trovato vuol dire ch è stato trovato il file
                    db_info = "Trovato"

                self.conn.sendall(db_info.encode())# invio stringa trovato o non trovato
                print(db_info)
            elif mess[0] == '2':
                conSQL = sqlite3.connect("file.db")#connessione al db
                cur = conSQL.cursor()
                list = mess.split(';') #split sul messaggio
                list[1] = "'" + list[1] + "'"#aggiungo le virgolette
                print(list[1])
                try:
                    research = cur.execute(f"SELECT tot_frammenti FROM files WHERE nome = {list[1]}")
                    #ricerca numero frammenti dato nome file
                    db_info = research.fetchall()[0][0]
                except:#se non trova nulla entra in except
                    db_info = "Non trovato"
                conSQL.close()
                db_info = "Numero frammenti: " + str(db_info)
                self.conn.sendall(db_info.encode())#invio le info richieste
                print(db_info)
            elif mess[0] == '3':
                conSQL = sqlite3.connect("file.db")
                cur = conSQL.cursor()
                list = mess.split(';') 
                list[1] = "'" + list[1] + "'"
                print(list[1])
                try:
                    research = cur.execute(f"SELECT host FROM frammenti fr, files fi WHERE fr.id_file = fi.id_file AND fi.nome = {list[1]} AND fr.n_frammento = {list[2]}")
                    #ricerca host con nome file e numero segmento
                    db_info = research.fetchall()[0][0]
                except:
                    db_info = "Non trovato"
                conSQL.close()
                db_info = "ip host su cui è presente il frammento: " + str(db_info)
                self.conn.sendall(db_info.encode())
                print(db_info)
            elif mess[0] == '4':
                conSQL = sqlite3.connect("file.db")
                cur = conSQL.cursor()
                list = mess.split(';') 
                list[1] = "'" + list[1] + "'"
                print(list[1])
                try:
                    research = cur.execute(f"SELECT host FROM frammenti fr, files fi WHERE fr.id_file = fi.id_file AND fi.nome = {list[1]}")
                    #ricerca lista di host in sono presenti i frammenti di un file
                    db_info = research.fetchall()
                except:
                    db_info = "Non trovato"
                conSQL.close()
                db_info = "ip host su cui è presente il frammento: " + str(db_info)
                self.conn.sendall(db_info.encode())
                print(db_info)



def main():
    lista_thread = []
    try:
        while True:#ciclo per accettare le connessioni
            s.listen()
            conn, address = s.accept()
            server = Server(conn)#dichiaro il nuovo oggeto thread
            lista_thread.append(server)#aggiungo l'oggetto alla lista che utilizzerò per chiudere tutti i thread
            server.start()#faccio partire il thread
            print("start thread")
    except KeyboardInterrupt:#se utilizzo keyboard interrupt
        for i in lista_thread:#ciclo per chiudere tutti i thread
            i.join()
        s.close()#chiudo il socket
        print("Chiusura")

if __name__ == "__main__":
    main()