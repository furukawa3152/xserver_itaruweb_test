from flask import Flask,render_template,request
import pandas as pd
import smtplib
import ssl
import datetime
from email.mime.text import MIMEText
app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/code.html')
def code():
    return render_template("code.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")

@app.route('/library.html')
def phtotos():
    return render_template("library.html")

@app.route('/line_bot.html')
def line_bot():
    return render_template("line_bot.html")

@app.route('/potate_boy.html')
def potate_boy():
    return render_template("potate_boy.html")

@app.route('/profile.html')
def profile():
    return render_template("profile.html")

@app.route('/index.html')
def hello():
    return render_template("index.html")

@app.route('/python_tips.html')
def tips():
    return render_template("python_tips.html")

@app.route('/thanx.html', methods=["POST"])
def thanx():
    name = request.form["お名前"]
    add = request.form["メールアドレス"]
    naiyou = request.form["お問い合わせ"]

    #送信
    df = pd.read_csv("static/itaruchan.csv", header=0)
    line_1 = df.iloc[0]
    id, password = (line_1[0], line_1[1])
    g_mail_address = f"{id}@gmail.com"
    g_mail_password = password
    msg = MIMEText(f"{name}--{add}--{naiyou}", "html")
    msg["Subject"] = f"{name}様よりお問い合わせです。"
    msg["To"] = "itaruchann511@gmail.com"
    msg["From"] = g_mail_address
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
                              context=ssl.create_default_context())
    server.login(g_mail_address, g_mail_password)
    server.send_message(msg)  # メールの送信



    return render_template("thanx.html", name=id)

if __name__ == '__main__':
    app.run()