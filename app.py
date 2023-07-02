import json
from flask import Flask, jsonify, request, render_template, redirect, session, Response
import dbconn
from dbconn import selectUsers
import pymysql
import datetime,time
import os
import psutil
from dotenv import load_dotenv
import cv2
import imutils
import threading
import argparse

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

source = "rtsp://coredjk:core2020@swc200e.iptimecam.com:21064/stream_ch00_0"
cap = cv2.VideoCapture(source)
time.sleep(2.0)


@app.route('/')
def home():
    return render_template('./login/login.html')

@app.route("/video")
def video():
    # return the rendered template
    return render_template("/subm/videofeed.html")

@app.route('/subm/mnu001', methods=['GET', 'POST'])
def mnu001f():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select camName,camLat,camLong from camlist where attrib not like 'XXX%'"
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
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql = "select camName, camAddr from camlist where attrib not like 'XXX%'"
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    db.close()
    if request.method == 'GET':
        return render_template('./subm/mnu002.html', result=result)
    else:
        return render_template("./subm/mnu002.html", result=result)


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
    sql1 = "select camNo,camName, custNo, serviceNo from camlist where attrib not like 'XXX%'"
    cur.execute(sql1)
    cond = cur.fetchall()
    if request.method == 'GET':
        return render_template('./subm/camlist.html', cond=cond)
    else:
        return render_template("./subm/camlist.html", cond=cond)


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
    db.close()
    return render_template("stat/dashinit.html", result=result_service, area=result_area,
                           cpu_remain=psutil.cpu_times_percent().idle, cpu_percent=psutil.cpu_percent(),
                           result_mem=psutil.virtual_memory(), result_disk=result_disk, result_month=result_month,
                           result_hour=result_hour)


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
    sql1 = "select * from camdevice where attrib not like 'XXX%'"
    cur.execute(sql1)
    cond = cur.fetchall()
    db.close()
    return render_template("subm/deviceman.html", cond=cond)

@app.route('/siteAdd')
def siteAdd():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "select * from camlist where attrib not like 'XXX%'"
    cur.execute(sql1)
    cond = cur.fetchall()
    sql2 = "select deviceNo, deviceSerial, deviceMacaddr from camdevice where attrib not like 'XXX%'"
    cur.execute(sql2)
    comba = cur.fetchall()
    sql3 = "select custNo, custName from custmng where attrib not like 'XXX%'"
    cur.execute(sql3)
    combb = cur.fetchall()
    db.close()
    return render_template("subm/siteman.html", cond=cond, comba=comba, combb=combb)

@app.route('/custAdd')
def custAdd():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    sql1 = "select * from custmng where attrib not like 'XXX%'"
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
        sql1 = "select * from camdevice where attrib not like 'XXX%'"
        cur.execute(sql1)
        cond = cur.fetchall()
        db.close()
        return render_template("subm/deviceman.html", cond=cond)
    else:
        sql1 = "insert into camdevice (deviceType, deviceSerial, deviceMacaddr, regDate) values (%s, %s, %s, now())"
        cur.execute(sql1, (str(request.form.get("devType")), str(request.form.get("devSerial")), str(request.form.get("devMac"))))
        db.commit()
        cond = cur.fetchall()
        db.close()
        return render_template("subm/deviceman.html")

@app.route('/siteInsert', methods=['GET', 'POST'])
def siteinsert():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    if request.method == 'GET':
        sql1 = "select * from camlist where attrib not like 'XXX%'"
        cur.execute(sql1)
        cond = cur.fetchall()
        db.close()
        return render_template("subm/siteman.html", cond=cond)
    else:
        sql1 = "insert into camlist (camName, deviceNo, custNo, serviceNo,camPostno, camAddr,regDate) values (%s,%s,%s,%s,%s,%s,now())"
        cur.execute(sql1, (str(request.form.get("siteNo")), str(request.form.get("deviceNo")),int(request.form.get("custNo")),str(request.form.get("serviceType")),str(request.form.get("camPostno")),str(request.form.get("camAddr"))))
        db.commit()
        cond = cur.fetchall()
        db.close()
        return render_template("subm/siteman.html")

@app.route('/custInsert', methods=['GET', 'POST'])
def custinsert():
    db = pymysql.connect(host=envhost, user=envuser, password=envpassword, db=envdb, charset=envcharset)
    cur = db.cursor()
    if request.method == 'GET':
        sql1 = "select * from custmng where attrib not like 'XXX%'"
        cur.execute(sql1)
        cond = cur.fetchall()
        db.close()
        return render_template("subm/custman.html", cond=cond)
    else:
        sql1 = "insert into custmng (custName, custAddr, custTel, custMail, serviceNo, regDate) values (%s, %s, %s, %s, %s, now())"
        cur.execute(sql1, (str(request.form.get("custName")), str(request.form.get("custAddr")),str(request.form.get("custTel")), str(request.form.get("custMail")), str(request.form.get("serviceNo"))))
        db.commit()
        cond = cur.fetchall()
        db.close()
        return render_template("subm/custman.html")

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

def stream(frameCount):
    global outputFrame, lock
    if cap.isOpened():
        # cv2.namedWindow(('CCTV camera'), cv2.WINDOW_AUTOSIZE)
        while True:
            ret_val, frame = cap.read()
            if frame.shape:
                frame = cv2.resize(frame, (640, 360))
                with lock:
                    outputFrame = frame.copy()
            else:
                continue
    else:
        print('camera open failed')

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')




if __name__ == '__main__':
    app.degub = True
    # app.run(host='0.0.0.0', port="443", ssl_context="adhoc")
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=False, default='127.0.0.1',
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=False, default=8000,
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
cap.release()
cv2.destroyAllWindows()