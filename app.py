import time

import pyodbc
import redis
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
server = 'assignmentservershruthaja.database.windows.net'
database = 'assignemnt3'
username = 'shruthaja'
password = 'mattu4-12'
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()

red = redis.StrictRedis(host='testredisshruthaja.redis.cache.windows.net', port=6379, db=0,
                        password='4KZj2Wt0qlRAoLaQrQt9urjqOLSfIWMnXAzCaByCwkw=', ssl=False)
red.flushall()


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    value = ""
    key = ""
    d = {}
    if request.method == "POST":
        s = request.form['abc']
        s=s.split()
        print(s[0][1])
        for i in s:
            d[i[0]]=int(i[1])
    return render_template("index.html", result=list(d.values()), r=list(d.keys()))


@app.route('/page2.html', methods=['GET', 'POST'])
def page2():
    value = ""
    key = ""
    d = {}
    if request.method == "POST":
        s = request.form['abc']
        s=s.split(',')
        for i in s:
            i=i.split()
            d[i[0]] = i[1]
    return render_template("page2.html", result=list(d.values()), r=list(d.keys()))


@app.route('/page22.html', methods=['GET', 'POST'])
def page22():
    query_time = []
    time_query = []
    result = []
    redis_time = []
    if request.method == "POST":
        smag = request.form['smag']
        emag = request.form['emag']
        query = "select top(1000) * from dbo.earthquake where mag between ? and ? ;"
        cursor.execute(query, smag, emag)
        temp = cursor.fetchall()
        temp_result = ""
        for j in temp:
            temp_result = temp_result + str(j)
        red.set(3, temp_result)
        for i in range(30):
            time_query.append(i + 1)
        query_time = []
        for i in time_query:
            start = time.time()
            cursor.execute(query, smag, emag)
            end = time.time()
            diff = end - start
            query_time.append(diff)
            s = time.time()
            red.get(3)
            e = time.time()
            redis_time.append(e - s)
    return render_template("page2.html", result=query_time, r=time_query, redis_time=redis_time)


@app.route('/page23.html', methods=['GET', 'POST'])
def page23():
    query_time = []
    time_query = []
    result = []
    redis_time = []
    if request.method == "POST":
        lat = request.form['lat1']
        long = request.form['lon1']
        ran = request.form['range']
        query = "select top(1000) * from dbo.earthquake  WHERE ( 6371 * ACOS(COS(RADIANS(latitude)) * COS(RADIANS(?)) * COS(RADIANS(longitude) - RADIANS(?)) + SIN(RADIANS(latitude)) * SIN(RADIANS(?)) ))< ?;"
        cursor.execute(query, lat, long, lat, ran)
        temp = cursor.fetchall()
        temp_result = ""
        for j in temp:
            temp_result = temp_result + str(j)
        red.set(4, temp_result)
        time_query = []
        for i in range(30):
            time_query.append(i + 1)
        query_time = []
        for i in time_query:
            start = time.time()
            cursor.execute(query, lat, long, lat, ran)
            end = time.time()
            diff = end - start
            query_time.append(diff)
            s = time.time()
            red.get(4)
            e = time.time()
            redis_time.append(e - s)
    return render_template("page2.html", result=query_time, r=time_query, redis_time=redis_time)


@app.route('/page3.html', methods=['GET', 'POST'])
def page3():
    xvalues=[]
    yvalues=[]
    color=[]
    if request.method == "POST":
        x = request.form['xvalues']
        y=request.form['yvalues']
        z=request.form['zvalues']
        for i in x.split():
            xvalues.append(i)
        for i in y.split():
            yvalues.append(i)
        for i in z.split():
            if(i=="1"):
                color.append('rgb(0,255,0)')
            elif(i=="2"):
                color.append('rgb(0,0,0)')
            elif(i=="3"):
                color.append('rgb(255,0,0)')
    return render_template("page3.html", xvalues=xvalues, yvalues=yvalues,color=color)


if __name__ == '__main__':
    app.run(debug=True)
