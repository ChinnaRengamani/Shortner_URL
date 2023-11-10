

from flask import Flask
from markupsafe import escape
from main import *
from flask import render_template
from flask import request
from flask import abort, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():     
    if request.method == "POST":
        first_name = request.form.get("furl")
        login = request.form.get("login")
        signup = request.form.get("signup")
        if login:
            return redirect("login")
        if signup:
            return redirect("signup")
        url=insert(first_name)
        qrimg=qrcode1(url)
        return render_template('short-url.html', url=url, qrimg=qrimg,oglink=first_name)
    return render_template("root.html")

@app.route('/<code>', methods=["GET"])
def code(code):
    H =retrive(code)
    if H:
        if code[-1] == '+':
            return H
        else:return redirect(str(retrive(code)), code=301)
    else:
        return f'{code} is not Correct'
    

@app.route('/user/<user>', methods=["GET"])
def user(user):
    return user


@app.route('/signup', methods=["GET","POST"])
def signup():

    if request.method == "POST":
        user = request.form.get("suser")
        password = request.form.get("spassword")
        if add_user(user,password):
            return "Sign up successful"
        else: 
            return f'<h1>Already Signup. Please Login</h1><p align="center"><a href=login ><button class=grey style="height:75px;width:150px">Login</button></a></p>'
    return render_template("signup.html")

@app.route('/login', methods=["GET",'POST'])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")
        h=check_user(user,password)
        if h == "signup":
            return f'<h1>User not Exsits. Please Signup </h1><p align="left"><a href=signup ><button class=grey style="height:75px;width:75px">Login</button></a></p>'
        elif h is True:
            return redirect(url_for('dashboard', user=user))
        elif h is True:
            return redirect(url_for('dashboard', user=user))
        else:
            return "Check Username and password." + render_template("login.html")
    return render_template("login.html")

@app.route('/dashboard/<user>', methods=["GET", "POST"])
def dashboard(user):
    name = user
    li=user_data(user)
    li.pop('_id')
    li.pop('username')
    li.pop('Password')
    if request.method == "GET":
        return render_template('dashboard.html',name=name,urls=li,Domain=Domain)
    if request.method == "POST":
        url = request.form.get("durl")
        code = insert(url).split('/')[-1]
        user_insert(user,url,code)
        url1=f'{Domain}/{code}'
        qrimg=qrcode1(url)
        return render_template('short-url.html', url=url1, qrimg=qrimg,oglink=url)
    return 'WELCOMe'+user

@app.route('/s/<short_url>', methods=["GET"])
def redirect_to_original(short_url):
    return redirect(f'{Domain}/{short_url}', code=301)
    


app.run(host="0.0.0.0", port=8080)