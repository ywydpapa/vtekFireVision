import json
from flask import Flask, jsonify, request, render_template, redirect, session
import dbconn
from dbconn import selectUsers
import pymysql
import datetime
import os
import psutil
from dotenv import load_dotenv

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


@app.route('/subm/mnujson', methods=['GET'])
def mnujson():
    curr = datetime.datetime.now()
    datfr = ''
    datto = ''
    filePath = "./menu.json"
    with open(filePath, 'r') as file:
        jsonDump = json.load(file)
    splitStr = jsonDump["menuItems"][request.args.get("menuIndex")].split(",")
    sqlStr = ''

    for i in range(len(splitStr)):
        if sqlStr == '':
            sqlStr += " AND (d004 in(" + "'" + splitStr[i].replace(" ", "") + "'))";
        else:
            sqlStr += " OR (d004 in(" + "'" + splitStr[i].replace(" ", "") + "'))";

    if (request.args.get("whereplus") != None):
        wherecon = request.args.get("whereplus")
    else:
        wherecon = sqlStr

    if request.args.get("datefrom") == '':
        datfr = curr - datetime.timedelta(minutes=5)
        datfr = datfr.strftime('%Y-%m-%d %H:%M')
    else:
        datfr = request.args.get("datefrom") + " " + request.args.get("timefrom")

    if request.args.get("dateto") == '':
        datto = curr.strftime('%Y-%m-%d %H:%M')
    else:
        datto = request.args.get("dateto") + " " + request.args.get("datetimetofrom")

    resultlength = dbconn.fromtoTraffic(datfr, datto, wherecon)
    result = dbconn.fromtoTrafficLimit(datfr, datto, str(wherecon), request.args)
    resultData = {
        "data": result,
        "recordsTotal": len(resultlength),
        "recordsFiltered": len(resultlength),
    }
    return jsonify(resultData)


@app.route('/subm/mnu001', methods=['GET', 'POST'])
def mnu001f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        result = dbconn.fromtoTraffic(datfr, datto, str(wherecon))
        cond = dbconn.menuSet("TRAF")
        return render_template('./subm/mnu001.html', result=result, cond=cond)
    else:
        datfr = ''
        datto = ''
        wherecon = ''
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item02 + ")"
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        result = dbconn.fromtoTraffic(datfr, datto, str(wherecon))
        cond = dbconn.menuSet("TRAF")
        return render_template("./subm/mnu001.html", result=result, cond=cond)


@app.route('/subm/mnu002', methods=['GET', 'POST'])
def mnu002f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("THRE")
        return render_template('./subm/mnu002.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item02 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("THRE")
        return render_template("./subm/mnu002.html", result=result, cond=cond)


@app.route('/subm/mnu003', methods=['GET', 'POST'])
def mnu003f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("URLF")
        return render_template('./subm/mnu003.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item03 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("URLF")
        return render_template("./subm/mnu003.html", result=result, cond=cond)


@app.route('/subm/mnu004', methods=['GET', 'POST'])
def mnu004f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("WILD")
        return render_template('./subm/mnu004.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item04 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("WILD")
        return render_template("./subm/mnu004.html", result=result, cond=cond)


@app.route('/subm/mnu005', methods=['GET', 'POST'])
def mnu005f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("DATA")
        return render_template('./subm/mnu005.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item05 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("DATA")
        return render_template("./subm/mnu005.html", result=result, cond=cond)


@app.route('/subm/mnu006', methods=['GET', 'POST'])
def mnu006f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("HIPM")
        return render_template('./subm/mnu006.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item06 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("HIPM")
        return render_template("./subm/mnu006.html", result=result, cond=cond)


@app.route('/subm/mnu007', methods=['GET', 'POST'])
def mnu007f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("GLOB")
        return render_template('./subm/mnu007.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item07 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("GLOB")
        return render_template("./subm/mnu007.html", result=result, cond=cond)


@app.route('/subm/mnu008', methods=['GET', 'POST'])
def mnu008f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("IPTA")
        return render_template('./subm/mnu008.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item08 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("IPTA")
        return render_template("./subm/mnu008.html", result=result, cond=cond)


@app.route('/subm/mnu009', methods=['GET', 'POST'])
def mnu009f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("USER")
        return render_template('./subm/mnu009.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item09 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("USER")
        return render_template("./subm/mnu009.html", result=result, cond=cond)


@app.route('/subm/mnu010', methods=['GET', 'POST'])
def mnu010f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("DESC")
        return render_template('./subm/mnu010.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item10 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("DESC")
        return render_template("./subm/mnu010.html", result=result, cond=cond)


@app.route('/subm/mnu011', methods=['GET', 'POST'])
def mnu011f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("TUNN")
        return render_template('./subm/mnu011.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item11 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("TUNN")
        return render_template("./subm/mnu011.html", result=result, cond=cond)


@app.route('/subm/mnu012', methods=['GET', 'POST'])
def mnu012f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("CONF")
        return render_template('./subm/mnu012.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item12 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("CONF")
        return render_template("./subm/mnu012.html", result=result, cond=cond)


@app.route('/subm/mnu013', methods=['GET', 'POST'])
def mnu013f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("SYST")
        return render_template('./subm/mnu013.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item13 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("SYST")
        return render_template("./subm/mnu013.html", result=result, cond=cond)


@app.route('/subm/mnu014', methods=['GET', 'POST'])
def mnu014f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("ALAR")
        return render_template('./subm/mnu014.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item14 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("ALAR")
        return render_template("./subm/mnu014.html", result=result, cond=cond)


@app.route('/subm/mnu015', methods=['GET', 'POST'])
def mnu015f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("AUTH")
        return render_template('./subm/mnu015.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item15 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("AUTH")
        return render_template("./subm/mnu015.html", result=result, cond=cond)


@app.route('/subm/mnu016', methods=['GET', 'POST'])
def mnu016f():
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("UNIF")
        return render_template('./subm/mnu016.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus') + " and o004 in (" + item16 + ")"
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=5)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("UNIF")
        return render_template("./subm/mnu016.html", result=result, cond=cond)


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
    curr = datetime.datetime.now()
    if request.method == 'GET':
        datfr = ''
        datto = ''
        wherecon = ''
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=2)
            datfr = datfr.strftime('%Y-%m-%d %H:%M')
        if datto == '':
            datto = curr.strftime('%Y-%m-%d %H:%M')
        print(datfr)
        print(datto)
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("TRAF")
        return render_template('./stat/indexStart.html', result=result, cond=cond)
    else:
        datfr = request.form.get('datefrom') + " " + request.form.get('timefrom')
        datto = request.form.get('dateto') + " " + request.form.get('timeto')
        wherecon = request.form.get('whereplus')
        if wherecon != '':
            wherecon = wherecon
        if datfr == '':
            datfr = curr - datetime.timedelta(minutes=2)
        if datto == '':
            datto = curr
        print(wherecon)
        result = dbconn.fromtoTraffic(datfr, datto, wherecon)
        cond = dbconn.menuSet("TRAF")
        return render_template("./stat/indexStart.html", result=result, cond=cond)


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
    sql = "select * from dayservice limit 10"
    cur.execute(sql)
    result_service = cur.fetchall()
    sql = "select * from areafrom limit 10"
    cur.execute(sql)
    result_area = cur.fetchall()
    result_disk = psutil.disk_usage(os.getcwd())
    sql = "select * from monthcount order by d002 asc"
    cur.execute(sql)
    result_month = cur.fetchall()
    sql = "select * from hourcount order by d002 asc"
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
        sql1 = "insert into userAccount (userId, userName, userPasswd, userEmail, userKey, userRole, attrib) values (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql1, (
        str(request.form.get("userId")), str(request.form.get("userName")), str(request.form.get("userPasswd")),
        str(request.form.get("userEmail")), str("1111111111"), str("ADMIN"), str("10000")))
        db.commit()
        cond = cur.fetchall()
        db.close()
        return render_template("menu/userAdd.html")


if __name__ == '__main__':
    app.degub = True
    # app.run(host='0.0.0.0', port="443", ssl_context="adhoc")
    app.run(debug=True, port=80, host='0.0.0.0')
