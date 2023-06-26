import time

import pyodbc
import redis
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    value = ""
    key = ""
    d = {}
    if request.method == "POST":
        s = request.form['abc']
        s=s.split(",")
        for i in s:
            d[i[0]]=i[2:]
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
