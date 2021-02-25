import sqlite3

def Increment():
    dbname = 'counter.db'
    conn = sqlite3.connect('counter.db')
    cur = conn.cursor()
    counter = conn.execute("select times from counter")
    for data in counter:
        counter = int(data[0])
    counter= counter +1
    cur.execute("INSERT INTO counter VALUES (" + str(counter) +")")
    conn.commit()

    cur.close()
    conn.close()


def get():
    dbname = 'counter.db'
    conn = sqlite3.connect('counter.db')
    cur = conn.cursor()
    counter = conn.execute("select times from counter")
    for data in counter:
        counter = int(data[0])
    conn.commit()

    cur.close()
    conn.close()

    return counter

