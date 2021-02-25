import sqlite3

# データベースに接続する
conn = sqlite3.connect('Bus.db')
c = conn.cursor()


# テーブルの作成
c.execute('''CREATE TABLE UniqueBusDB(Busid INTEGER, area_SquareM REAL,owner TEXT)''')
# データの挿入
c.execute("INSERT INTO UniqueBusDB VALUES (1 ,30, 'owner1')")
c.execute("INSERT INTO UniqueBusDB VALUES (2 ,22.5, 'owner2')")
c.execute("INSERT INTO UniqueBusDB VALUES (3 ,16.8, 'owner3')")


# テーブルの作成
c.execute('''CREATE TABLE ImaginaryBusTimetable(BusID INTEGER, areaID INTEGER,time TEXT)''')
# データの挿入
areaNum=10
BusNum =5
startTime = "2021-2-28 12:"
for Bus in range(BusNum):
    for area in range(areaNum):
        time = 5* area #分のデータ
        Str = "INSERT INTO ImaginaryBusTimetable VALUES(" + str(Bus) + "," + str(area) + ",\"" + startTime +str(time) +":00"+"\")"
        c.execute(Str)




c.execute('''CREATE TABLE RealBusTimetable(BusID INTEGER, areaID INTEGER,time TEXT,PersonNum INTEGER)''')
# 挿入した結果を保存（コミット）する
conn.commit()

# データベースへのアクセスが終わったら close する
conn.close()