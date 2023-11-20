import sqlite3

comando = "'RR'"
conSQL = sqlite3.connect("movements.db")
cur = conSQL.cursor()
research = cur.execute(f"SELECT Mov_sequence FROM movements WHERE Shortcut = {comando}")
print(research.fetchall()[0][0])
s = "1" + "'"
print(f"{s}")