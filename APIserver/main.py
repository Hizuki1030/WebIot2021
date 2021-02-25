from flask import Flask, render_template #追加
from flask import request
import sqlite3
import datetime
import json
import counter
app = Flask(__name__)


conn = sqlite3.connect('Bus.db',check_same_thread=False)
BusDB= conn.cursor()


@app.route('/')
def a():
    counter.Increment()
    times = counter.get()
    Digit1=""
    Digit2=""
    Digit3=""
    Digit4=str(times)
    return render_template('index.html', T1=Digit1, T2=Digit2,T3=Digit3,T4=Digit4) #変更


#DBへデータ送信~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/AddDB', methods=["GET"])#
def AddDB():#http://127.0.0.1:5000/AddDB?BusID=1&AreaID=2&time="2021-02-28 12:10:00"&personNum=10
    counter.Increment()
    id = request.args.get("BusID")
    area = request.args.get("AreaID")
    time = request.args.get("time")
    personNum = request.args.get("personNum")
    StringAddDB = "INSERT INTO RealBusTimetable VALUES (" + str(id) + ","+str(area) + ","+str(time) + ","+str(personNum)+")"
    BusDB.execute(StringAddDB)
    conn.commit()
    return "OK!!!"

#予想時刻の取得~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/estimateTimetable/<int:BusID>', methods=["GET"])#http://127.0.0.1:5000/estimateTimetable/1?lastAreaID=1
def EstimateTimetable(BusID):
    counter.Increment()
    lastAreaID = int(request.args.get("lastAreaID"))

    ImaginaryBusTimetable = BusDB.execute("select * from ImaginaryBusTimetable where BusID = "+ str(BusID))

    #どうにかしてバスの遅延度（プラスマイナス）を算出する~~~~~~~~~~~~~~~~~~~~~~~
    dtDict_minute =dict(((1,-2),(2,0),(3,2),(4,1),(5,1),(6,0),(7,2),(8,2),(9,1)))#((AreaID1,dt1),(AreaID2,dt2),,,,,,,,,,)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    estimateTimetable ={}
    for data in ImaginaryBusTimetable: #(BusID,AreaID,time)
        AreaID = int(data[1])
        ImaginaryTime = datetime.datetime.strptime(data[2],'%Y-%m-%d %H:%M:%S')

        if(AreaID <= lastAreaID):#通過したareaの予想時刻はいらない
            continue

        dt_minute = datetime.timedelta(minutes=dtDict_minute[AreaID])
        estimateTime = ImaginaryTime + dt_minute
        estimateTimetable[AreaID] = str(estimateTime)
    estimateTimetable_json = json.dumps(estimateTimetable)
    return estimateTimetable_json

#乗車人数、人口密度、実際の到着予想時刻の取得~~~~~~~~~~~~~~~~
@app.route('/status/<int:BusID>',methods=["GET"])#http://127.0.0.1:5000/status/1
def status(BusID):
    counter.Increment()
    UniqueBusInfo    = BusDB.execute("SELECT * FROM UniqueBusDB where BusID = "+ str(BusID))
    a=None
    for data in UniqueBusInfo:
        BusArea = data[1]
    RealBusTimetable = BusDB.execute("SELECT * FROM RealBusTimetable where BusID = "+ str(BusID))    
    StatusTable = {} #変数名何にすべき？？？？？？？？？

    for data in RealBusTimetable:
        Status ={}
        AreaID = int(data[1])
        print(data[2])
        Time  = datetime.datetime.strptime(data[2],'%Y-%m-%d %H:%M:%S')
        PersonNum = int(data[3])
        PopulationDensity = PersonNum/BusArea
        Status["Time"] = str(Time)
        Status["PersonNUM"] = PersonNum
        Status["PopulationDensity"] = PopulationDensity
        StatusTable[AreaID]= str(Status)
    StatusTable_json = json.dumps(StatusTable)

    return StatusTable_json

    

    
        
        
    
    



if __name__ == '__main__':
    app.debug = True
    app.run()