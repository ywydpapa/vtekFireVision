import json
from flask import Flask, flash, request, render_template, redirect, session, Response
import dbconn
from dbconn import selectUsers
import deviceSetup
import pymysql
import datetime,time
import os
import psutil
from dotenv import load_dotenv
import cv2
import imutils
import threading
import argparse
from geopy.geocoders import Nominatim
from decimal import Decimal
geo_local = Nominatim(user_agent='South Korea')

outputFrame = None
lock = threading.Lock()

load_dotenv()
db = None
cur = None
envhost = os.getenv('envhost')
envuser = os.getenv('envuser')
envpassword = os.getenv('envpassword')
envdb = os.getenv('envdb')
envcharset = os.getenv('envcharset')
app = Flask(__name__)
app.secret_key = 'fsdfsfgsfdg3234'

@app.route('/')
def home():
    return render_template('./login/login.html')

@app.route("/video")
def video():
    # return the rendered template
    video_feed()
    return render_template("/subm/videofeed.html")

@app.route('/subm/mnu001', methods=['GET', 'POST'])
def mnu001f():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select camName,camLat,camLong from camList where attrib not like 'XXX%'"
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    db.close()
    if request.method == 'GET':
        return render_template('./subm/mnu001.html', result=result)
    else:
        return render_template("./subm/mnu001.html", result=result)


@app.route('/subm/mnu002', methods=['GET', 'POST'])
def mnu002f():
    resultArr = []
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select camNo, camName, camLat, camLong, camAddr1, camAddr2, camLink from camList where attrib not like 'XXX%'"
    cur.execute(sql)
    result = json.dumps(cur.fetchall(), default=str)
    db.close()
    
    if request.method == 'GET':
        return render_template('./subm/mnu002.html', result=result)
    else:
        return render_template("./subm/mnu002.html", result=result)

@app.route('/camListSelect/<alarmkey>', methods=['GET', 'POST'])
def camListSelect(alarmkey):
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select * from camList where alarmKey = '" + str(alarmkey) + "' and attrib not like 'XXX%'"
    cur.execute(sql)
    result = json.dumps(cur.fetchall(), default=str)
    db.close()
    return result

@app.route('/sitedetail/<camno>', methods=['GET', 'POST'])
def sitedetail(camno):
    resultArr = []
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select camList.camName, camList.camLat, camList.camLong, camList.camAddr1, camList.camAddr2, camList.camLink, camList.attrib, camList.camNo, camList.alarmKey, alarmon.alarmNo as alarmNo, alarmon.attrib as alramAttrib from camList"
    sql += " left join alarmon on camList.alarmKey = alarmon.alarmKey and alarmon.attrib not like 'XXX%'"
    sql += " where camList.camNo = " + camno
    cur.execute(sql)
    result = cur.fetchall()
    cur.execute(sql)
    resultJson = json.dumps(cur.fetchall(), default=str)
    sql = "select sensordata.sensorKey, avg(sensordata.sensorValue) from sensordata"
    sql += " left join camDevice on sensordata.sensorKey = camDevice.sensor01"
    sql += " left join camList on camDevice.deviceType = camList.alarmKey"
    sql += " where camList.camNo = " + camno + " group by date_format(`sensordata`.`regDate`, '%Y-%m-%d %h:%i') order by sensordata.regDate desc limit 60"
    cur.execute(sql)
    sensor1 = json.dumps(cur.fetchall(), default=str)
    sql = "select sensordata.sensorKey, avg(sensordata.sensorValue) from sensordata"
    sql += " left join camDevice on sensordata.sensorKey = camDevice.sensor02"
    sql += " left join camList on camDevice.deviceType = camList.alarmKey"
    sql += " where camList.camNo = " + camno + " group by date_format(`sensordata`.`regDate`, '%Y-%m-%d %h:%i') order by sensordata.regDate desc limit 60"
    cur.execute(sql)
    sensor2 = json.dumps(cur.fetchall(), default=str)
    sql = "select sensordata.sensorKey, avg(sensordata.sensorValue) from sensordata"
    sql += " left join camDevice on sensordata.sensorKey = camDevice.sensor03"
    sql += " left join camList on camDevice.deviceType = camList.alarmKey"
    sql += " where camList.camNo = " + camno + " group by date_format(`sensordata`.`regDate`, '%Y-%m-%d %h:%i') order by sensordata.regDate desc limit 60"
    cur.execute(sql)
    sensor3 = json.dumps(cur.fetchall(), default=str)
    sql = "select sensordata.sensorKey, avg(sensordata.sensorValue) from sensordata"
    sql += " left join camDevice on sensordata.sensorKey = camDevice.sensor04"
    sql += " left join camList on camDevice.deviceType = camList.alarmKey"
    sql += " where camList.camNo = " + camno + " group by date_format(`sensordata`.`regDate`, '%Y-%m-%d %h:%i') order by sensordata.regDate desc limit 60"
    cur.execute(sql)
    sensor4 = json.dumps(cur.fetchall(), default=str)
    db.close()
    for i in range(len(result)):
        resultDatas = {
            "camName": result[i][0],
            "camLat": str(result[i][1]),
            "camLong": str(result[i][2]),
            "camAddr1": result[i][3],
            "camAddr2": result[i][4],
            "camLink": result[i][5],
            "attrib": result[i][6],
            "camNo": result[i][7],
            "alarmKey": result[i][8],
            "alarmNo": result[i][9],
            "alramAttrib": result[i][10]
        }
        resultArr.append(resultDatas)

    if request.method == 'GET':
        return render_template('./subm/sitedetail.html', result=resultArr,resultJson=resultJson,sensor01=sensor1,sensor02=sensor2,sensor03=sensor3,sensor04=sensor4)
    else:
        return render_template("./subm/sitedetail.html", result=resultArr,resultJson=resultJson,sensor01=sensor1,sensor02=sensor2,sensor03=sensor3,sensor04=sensor4)
    
@app.route('/alarmUpdate/<alarmNo>', methods=['GET'])
def alarmUpdate(alarmNo):
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "update alarmon set modDate = now(), attrib = 'XXXXX0000000000' where alarmNo = " + alarmNo
    cur.execute(sql1)
    db.commit()
    cur.fetchall()
    db.close()
    return "";


@app.route('/mainAlarmDatas', methods=['GET'])
def mainAlarmDatas():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select * from alarmon where attrib not like 'XXX%'"
    cur.execute(sql)
    result = json.dumps(cur.fetchall(), default=str)
    print(result);
    db.close()
    flash("OK")
    return result

@app.route('/alarmon/<alarmkey>', methods=['GET'])
def alarmon(alarmkey):
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "update alarmon set modDate = now() , attrib = 'XXXXX0000000000' where alarmKey = %s"
    cur.execute(sql1, str(alarmkey))
    sql = "insert into alarmon (alarmKey, regDate) values (%s, now())"
    cur.execute(sql, str(alarmkey))
    db.commit()
    cur.fetchall()
    db.close()
    flash("OK")
    return render_template("./stat/emptyPage.html")

@app.route('/sensins/<sensorkey>', methods=['GET'])
def sensorins(sensorkey):
    svalue = request.args.get('sensorval', default='0.0', type = str)
    print(svalue)
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "insert into sensordata (sensorKey, sensorValue, regDate) values (%s,%s, now())"
    cur.execute(sql,(str(sensorkey), str(svalue)))
    db.commit()
    cur.fetchall()
    db.close()
    flash("OK")
    return render_template("./stat/emptyPage.html")


@app.route('/alarmoff/<alarmkey>', methods=['GET'])
def alarmoff(alarmkey):
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "update alarmon set attrib = 'XXXXX0000000000', modDate = now() where alarmkey = %s"
    cur.execute(sql, str(alarmkey))
    db.commit()
    cur.fetchall()
    db.close()
    flash("OK")
    return render_template("./stat/emptyPage.html")
    
@app.route('/subm/deviceSelect', methods=['GET'])
def deviceSelect():
    deviceNo = request.args.get("deviceNo");
    resultArr = []
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select * from camDevice where deviceNo = " + deviceNo + " and attrib not like 'XXX%'"
    cur.execute(sql)
    result = json.dumps(cur.fetchall(), default=str)
    db.close()
    return result


@app.route('/subm/cpu')  # 요청
def cpustat():
    pid = os.getpid()
    py = psutil.Process(pid)
    # cpu_usage = os.popen("ps aux | grep " + str(pid) + " | grep -v grep | awk '{print $3}'").read()
    # cpu_usage = cpu_usage.replace("\n", "")
    # memory_usage = round(py.memory_info()[0] / 2. ** 30, 2)
    result_disk = psutil.disk_usage(os.getcwd())
    return render_template("stat/dashcpu.html", cpu_remain=psutil.cpu_times_percent().idle,
                           cpu_percent=psutil.cpu_percent(), result_mem=psutil.virtual_memory(),
                           result_disk=result_disk)


@app.route('/subm/disk')  # 요청
def diskstat():
    result_disk = psutil.disk_usage(os.getcwd())
    return render_template("stat/dashdisk.html", result=result_disk)


@app.route('/subm/network')  # 요청
def networkstat():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select * from hBefore order by d002 desc limit 200"
    cur.execute(sql)
    result = cur.fetchall()
    db.close()
    return render_template("stat/dashnetwork.html", result=result)


@app.route('/monmain', methods=['GET', 'POST'])  # 요청
def okhome():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "select * from camList where attrib not like 'XXX%' order by regDate desc limit 10"
    cur.execute(sql1)
    cond = cur.fetchall()
    if request.method == 'GET':
        return render_template('/subm/camList.html', cond=cond)
    else:
        return render_template("/subm/camList.html", cond=cond)


@app.route('/menuset')
def menuset():
    if request.args.get("selectValue") == None:
        selectValue = " and menuNo = 'TRAF'";
    else:
        selectValue = " and menuNo = '" + request.args.get("selectValue") + "'"

    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "select activeMenu,menuTitle,useYN,sortCust from menuCustom where attrib not like '%XXX%'" + selectValue
    cur.execute(sql1)
    cond = cur.fetchall()
    db.close()
    return render_template("menu/menuAdmin.html", cond=cond)


@app.route('/updatemenu', methods=['GET', 'POST'])
def updatemenu():
    formtotal = request.form
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    mtitles = formtotal.getlist('mtitle')
    mkeys = formtotal.getlist('mkey')
    muses = formtotal.getlist('muse')
    msorts = formtotal.getlist('msort')
    menuSelect = formtotal.get("menuSelect")
    for i in range(len(mkeys)):
        val01 = mtitles[i]
        val02 = muses[i]
        val03 = msorts[i]
        val04 = mkeys[i]
        sql1 = "update menuCustom set menuTitle = %s , useYN = %s , sortCust = %s where menuNo = '" + menuSelect + "'" + " and activeMenu = %s"
        cur.execute(sql1, (val01, val02, val03, val04))
    db.commit()
    sql2 = "select activeMenu,menuTitle,useYN,sortCust from menuCustom where menuNo = 'TRAF' and attrib not like '%XXX%'"
    cur.execute(sql2)
    cond = cur.fetchall()
    db.close()
    return render_template("menu/menuAdmin.html", cond=cond)


@app.route('/dashmain')  # 요청
def searchSel():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select * from inoutT limit 10"
    cur.execute(sql)
    result_service = cur.fetchall()
    sql = "select * from inoutT limit 10"
    cur.execute(sql)
    result_area = cur.fetchall()
    result_disk = psutil.disk_usage(os.getcwd())
    sql = "select * from inoutT order by d002 asc"
    cur.execute(sql)
    result_month = cur.fetchall()
    sql = "select * from inoutT order by d002 asc"
    cur.execute(sql)
    result_hour = cur.fetchall()
    sql = "select camList.camNo, camList.camName, camList.camPostNo, camList.camAddr1, camList.camAddr2, camDevice.sensor01, camDevice.sensor02, camDevice.sensor03, camDevice.sensor04 from camList"
    sql += " left join camDevice on camDevice.deviceType = camList.alarmKey"
    sql += " where camList.attrib not like 'XXX%' order by camList.regDate desc limit 10"
    cur.execute(sql)
    camList = cur.fetchall()
    db.close()
    return render_template("stat/dashinit.html", result=result_service, area=result_area,
                           cpu_remain=psutil.cpu_times_percent().idle, cpu_percent=psutil.cpu_percent(),
                           result_mem=psutil.virtual_memory(), result_disk=result_disk, result_month=result_month,
                           result_hour=result_hour,result_camList=camList)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('./login/login.html')
    else:
        uid = request.form.get('uid')
        upw = request.form.get('upw')
        row = selectUsers(uid, upw)
        if row:
            session['userNo'] = row['userNo']
            session['userName'] = row['userName']
            session['userRole'] = row['userRole']
            return redirect('/dashmain')
        else:
            return '''
                <script>
                    // 경고창 
                    alert("로그인 실패, 다시 시도하세요")
                    // 이전페이지로 이동
                    history.back()
                </script>
            '''


@app.route('/logout')
def logout():
    session.clear()
    return render_template('./login/login.html')

@app.route('/deviceAdd')
def deviceAdd():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "select * from camDevice where attrib not like 'XXX%'"
    cur.execute(sql1)
    cond = cur.fetchall()
    db.close()
    return render_template("subm/deviceman.html", cond=cond)

@app.route('/siteAdd')
def siteAdd():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "select * from camList where attrib not like 'XXX%'"
    cur.execute(sql1)
    cond = cur.fetchall()
    sql2 = "select deviceNo, deviceSerial, deviceMacaddr from camDevice where attrib not like 'XXX%'"
    cur.execute(sql2)
    comba = cur.fetchall()
    sql3 = "select custNo, custName from custMng where attrib not like 'XXX%'"
    cur.execute(sql3)
    combb = cur.fetchall()
    db.close()
    return render_template("subm/siteman.html", cond=cond, comba=comba, combb=combb)

@app.route('/custAdd')
def custAdd():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "select * from custMng where attrib not like 'XXX%'"
    cur.execute(sql1)
    cond = cur.fetchall()
    db.close()
    return render_template("subm/custman.html", cond=cond)

@app.route('/userAdd', methods=['GET', 'POST'])
def userAdd():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()

    if request.method == 'GET':
        sql1 = "select * from userAccount"
        cur.execute(sql1)
        cond = cur.fetchall()
        db.close()
        return render_template("menu/userAdd.html", cond=cond)
    else:
        sql1 = "insert into userAccount (userId, userName, userPasswd, userEmail, userKey, userRole, attrib) values (%s, %s, password(%s), %s, %s, %s, %s)"
        cur.execute(sql1, (
        str(request.form.get("userId")), str(request.form.get("userName")), str(request.form.get("userPasswd")),
        str(request.form.get("userEmail")), str("1111111111"), str("ADMIN"), str("10000")))
        db.commit()
        cond = cur.fetchall()
        db.close()
        return render_template("menu/userAdd.html")

@app.route('/devInsert', methods=['GET', 'POST'])
def devinsert():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    if request.method == 'GET':
        sql1 = "select * from camDevice where attrib not like 'XXX%'"
        cur.execute(sql1)
        cond = cur.fetchall()
        db.close()
        return render_template("subm/deviceman.html", cond=cond)
    else:
        sql1 = "insert into camDevice (deviceType, deviceSerial, deviceMacaddr,deviceIp4, deviceIp6, deviceSetno, sensor01,sensor02,sensor03,sensor04, regDate) " \
               "values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s, now())"
        cur.execute(sql1, (str(request.form.get("devType")), str(request.form.get("devSerial")), str(request.form.get("devMac")),
                           str(request.form.get("deviceIp4")), str(request.form.get("deviceIp6")),
                           str(request.form.get("deviceSetno")), str(request.form.get("sensor01")), str(request.form.get("sensor02")),
                           str(request.form.get("sensor03")), str(request.form.get("sensor04"))))
        db.commit()
        cond = cur.fetchall()
        db.close()
        return render_template("subm/deviceman.html")

@app.route('/devUpdate', methods=['POST'])
def devupdate():
    deviceNo = request.form.get("deviceNo")
    print(request.form)
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "update camDevice set deviceType = %s, deviceSerial = %s,  deviceMacaddr = %s, deviceIp4 = %s , deviceIp6 = %s, deviceSetno = %s, sensor01 = %s, sensor02 = %s, sensor03 = %s, sensor04 = %s, modDate = now() where deviceNo = " + deviceNo
    cur.execute(sql1, (str(request.form.get("devType")), str(request.form.get("devSerial")), str(request.form.get("devMac")),str(request.form.get("deviceIp4")),str(request.form.get("deviceIp6")),str(request.form.get("deviceSetno")),str(request.form.get("sensor01")),str(request.form.get("sensor02")),str(request.form.get("sensor03")),str(request.form.get("sensor04"))))
    db.commit()
    cur.fetchall()
    db.close()
    return render_template("subm/deviceman.html")


@app.route('/siteInsert', methods=['GET', 'POST'])
def siteinsert():
    addrStr = str(request.form.get("camAddr1"))
    latLong = geocoding(addrStr)
    print(latLong)
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    if request.method == 'GET':
        sql1 = "select * from camList where attrib not like 'XXX%'"
        cur.execute(sql1)
        cond = cur.fetchall()
        db.close()
        return render_template("subm/siteman.html", cond=cond)
    else:
        sql1 = "insert into camList (camName, deviceNo, camLat, camLong, custNo, serviceNo, camPostno, camAddr1, camAddr2, regDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"
        cur.execute(sql1, (str(request.form.get("siteNo")), str(request.form.get("deviceNo")),latLong[0],latLong[1],int(request.form.get("custNo")),str(request.form.get("serviceType")),str(request.form.get("camPostno")),str(request.form.get("camAddr1")),str(request.form.get("camAddr2"))))
        db.commit()
        cond = cur.fetchall()
        db.close()
        return render_template("subm/siteman.html")

@app.route('/custInsert', methods=['GET', 'POST'])
def custinsert():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    if request.method == 'GET':
        sql1 = "select * from custMng where attrib not like 'XXX%'"
        cur.execute(sql1)
        cond = cur.fetchall()
        db.close()
        return render_template("subm/custman.html", cond=cond)
    else:
        sql1 = "insert into custMng (custName, custAddr, custTel, custMail, serviceNo, regDate) values (%s, %s, %s, %s, %s, now())"
        cur.execute(sql1, (str(request.form.get("custName")), str(request.form.get("custAddr")),str(request.form.get("custTel")), str(request.form.get("custMail")), str(request.form.get("serviceNo"))))
        db.commit()
        cond = cur.fetchall()
        db.close()
        return render_template("subm/custman.html")


@app.route("/videoFeed/<camNo>")
def video_feed(camNo):
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select camLink from camList where camNo = " + camNo + " and attrib not like 'XXX%'"
    cur.execute(sql)
    result = cur.fetchone()
    print(result)
    try_num = 1
    program_quit = False
    while True:
        print(f'try {try_num}')
        cap = cv2.VideoCapture(result[0])
        ret, img_color = cap.read()
        if ret == False:
            try_num += 1
            time.sleep(1)
            continue
        try_num = 1
        fps = cap.get(cv2.CAP_PROP_FPS)
        print('fps', fps)
        if fps == 0.0:
            fps = 30.0
        while True:
            ret, img_color = cap.read()
            if ret == False:
                print('영상을 가져올 수 없습니다.')
                break

            cv2.imshow("vtekVision CCTV LIVE", img_color)

            if cv2.waitKey(1) == 27:
                program_quit = True
                break
        cap.release()
        cv2.destroyAllWindows()
        if program_quit:
            break

def geocoding(address):
    try:
        geo = geo_local.geocode(address)
        x_y = [geo.latitude, geo.longitude]
        print(x_y)
        return x_y
    except:
        return [0,0]
    
if __name__ == '__main__':
    app.degub = True
    # app.run(host='0.0.0.0', port="443", ssl_context="adhoc")
    app.run(debug=True, port=80, host='0.0.0.0')
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=False, default='127.0.0.1',
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=False, default=5000,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    t = threading.Thread(target=stream, args=(args["frame_count"],))
    t.daemon = True
    t.start()

    # app.run(debug=True, port=80, host='0.0.0.0')
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

# release the video stream pointer
#cap.release()
#cv2.destroyAllWindows()
