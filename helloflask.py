from flask import Flask,render_template,request,session
import pandas as pd
import smtplib
import ssl
import datetime
import requests
import time
import random
from email.mime.text import MIMEText


app = Flask(__name__)
app.secret_key = "user"


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

@app.route('/thanx.html', methods=["GET","POST"])
def thanx():
    if request.method == "POST":
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
    else:
        return render_template("index.html")

# @app.route("/sql")
# def hello_sql():
#     sql = "SELECT `id`, `name` ,`age` FROM users ORDER BY id"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     # moji = ""
#     # for row in result:
#     #    moji = moji+"id：" + str(row[0]) + "　　name：" + str(row[1]) + "さん"+"   age:" +str(row[2])+"歳<br>"
#     # return moji
#     # cursor.close()
#     # connector.close()
#     return render_template("kaiin.html",kaiin=result)
#     connector.commit()
#     cursor.close()
#     connector.close()

# @app.route("/whatday")
# def wd_sql():
#     dt_now =  datetime.date.today()
#     month = dt_now.month
#     day = dt_now.day
#     sql = f"SELECT `月`, `日` ,`内容` FROM what_day2 WHERE 月='{month}' AND 日='{day}'"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     # moji = ""
#     # for row in result:
#     #    moji = moji+"id：" + str(row[0]) + "　　name：" + str(row[1]) + "さん"+"   age:" +str(row[2])+"歳<br>"
#     # return moji
#     # cursor.close()
#     # connector.close()
#     return render_template("kaiin.html",kaiin=result)
#     connector.commit()
#     cursor.close()
#     connector.close()

@app.route("/chatbot")
def chatbot():
    session["list"] = []
    return render_template("chatbot.html")

@app.route("/talkroom.html", methods=["GET","POST"])
def talkroom():
    talk_list = session["list"]
    if request.method == "POST":
        talk = request.form['talk']
        talk_list.append(f"あなた＞{talk}")
        import mysql.connector as mydb
        # mysql接続
        connector = mydb.connect(
            host='localhost',
            user='root',
            password='itaruchan',
            database='itaru_test',
            charset="utf8")
        cursor = connector.cursor()
        sql = "SELECT title,text FROM profile;"
        cursor.execute(sql)
        result = cursor.fetchall()
        ans_list = []
        for ans in result:
            if ans[0] in talk:
                ans_list.append(ans[1])
        connector.commit()
        cursor.close()
        connector.close()
        if len(ans_list) > 0:
            answer = random.choice(ans_list)
            talk_list.append(f"itarubot＞{answer}")
        #profileに内容が無ければ以下へ
        elif "何の日" in talk:
            import mysql.connector as mydb
            # mysql接続
            connector = mydb.connect(
                host='localhost',
                user='root',
                password='itaruchan',
                database='itaru_test',
                charset="utf8")
            cursor = connector.cursor()
            #SQLから何の日情報取得
            dt_now = datetime.date.today()
            month = dt_now.month
            day = dt_now.day
            sql = f"SELECT `月`, `日` ,`内容` FROM what_day2 WHERE 月='{month}' AND 日='{day}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            whatday = result[0][2]
            after_text=random.choice(["らしいですよ！","だそうですよ。","ですって。","なんですよ。エッヘン！","なのです！"])
            talk_list.append(f"itarubot＞今日{month}月{day}日は{whatday}{after_text}")
            connector.commit()
            cursor.close()
            connector.close()
        else:
            #A3RTtalkAPI取得へ
            # apikey = 'DZZSAPf1t4pKmUBHwCWHI7P6juvbju0o'
            # URL = f"https://api.a3rt.recruit.co.jp/talk/v1/smalltalk"
            # payload = {'apikey': apikey, 'query': talk}
            # time.sleep(0.5)
            # try:
            #     r = requests.post(URL, data=payload)
            #     back = (r.json()["results"][0]["reply"])
            # except KeyError:
            #     back = "すいませんわかりません"
            # talk_list.append(f"itarubot＞{back}")
            talk_list.append(f"itarubot＞{fetch_reqests(talk)}")
        session["list"] = talk_list
        return render_template("talkroom.html" ,talk=session["list"])
    else:
        return render_template("chatbot.html")

def fetch_reqests(word):
    import requests
    #A3RTtalkAPI取得へ
    apikey = 'DZZSAPf1t4pKmUBHwCWHI7P6juvbju0o'
    URL = f"https://api.a3rt.recruit.co.jp/talk/v1/smalltalk"
    payload = {'apikey': apikey, 'query': word}
    time.sleep(0.1)
    try:
        r = requests.post(URL, data=payload)
        back = (r.json()["results"][0]["reply"])
    except KeyError:
        back = "すいませんわかりません"
    return back

if __name__ == '__main__':
    app.run(debug=True)