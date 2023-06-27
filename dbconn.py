import pymysql as my
import os
from dotenv import load_dotenv

load_dotenv()

envhost = os.getenv('envhost')
envuser = os.getenv('envuser')
envpassword = os.getenv('envpassword')
envdb = os.getenv('envdb')
envcharset = os.getenv('envcharset')

def selectUsers(uid, upw):
    row = None
    connection = None
    try:
        connection = my.connect(host=envhost,
                                user=envuser,
                                password=envpassword,
                                database=envdb,
                                cursorclass=my.cursors.DictCursor
                                )
        cursor = connection.cursor()
        sql = '''SELECT * FROM userAccount WHERE userId=%s AND userPasswd=password(%s)'''
        cursor.execute(sql, (uid, upw))
        row = cursor.fetchone()
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
    return row

def fromtoTraffic(datfr, datto, wherecon):
    rows = None
    connection = None
    try:
        connection = my.connect(host=envhost,
                                user=envuser,
                                password=envpassword,
                                database=envdb,
                                cursorclass=my.cursors.DictCursor
                                )
        cursor = connection.cursor()
        sql = "SELECT * FROM inoutT WHERE d002 between " + "'" + str(datfr) + "'" + " AND " + "'" + str(datto) + "'" + wherecon
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
    return rows

def fromtoTrafficLimit(datfr, datto, wherecon, requests):
    rows = None
    connection = None
    draw = requests.get("start")
    pageLength = requests.get("length")
    rowIndex = requests.get("order[0][column]");
    sort = requests.get("order[0][dir]");
    rowIndexColumn = requests.get("columns[" + rowIndex + "][data]")
    try:
        connection = my.connect(host=envhost,
                                user=envuser,
                                password=envpassword,
                                database=envdb,
                                cursorclass=my.cursors.DictCursor
                                )
        cursor = connection.cursor()
        firstLimit = int(draw)
        lastLimit = int(pageLength)
        sql = "SELECT * FROM inoutT WHERE d002 between " + "'" + str(datfr) + "'" + " AND " + "'" + str(datto)+ "'" + wherecon + " order by " + str(rowIndexColumn) + " " + str(sort) + " limit " + str(firstLimit) + ", " + str(lastLimit)
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
    return rows

def menuSet(typ):
    rows = None
    connection = None
    try:
        connection = my.connect(host=envhost,
                                user=envuser,
                                password=envpassword,
                                database=envdb,
                                cursorclass=my.cursors.DictCursor
                                )
        cursor = connection.cursor()
        sql = '''SELECT activeMenu, menuTitle FROM menuCustom WHERE useYn = %s AND menuNo = %s order by sortCust'''
        cursor.execute(sql, ("Y", typ))
        rows = cursor.fetchall()
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
    return rows

if __name__ == '__main__':
    row = selectUsers('guest', '1')
    print('쿼리회원조회결과 : ', row)
    row = selectUsers('guest', '2')
    print('회원조회결과 : ', row)