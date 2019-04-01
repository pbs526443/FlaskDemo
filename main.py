from flask import Flask,render_template,request,redirect,make_response
import datetime
from orm import model
from orm import ormmanage as magen
app = Flask(__name__)
#配置缓存更新时间
app.send_file_max_age_default = datetime.timedelta(seconds=1)
app.debug=True
# 将http://127.0.0.1:5000/ 和index视图函数绑定
@app.route('/')
def index():
    # return "<h1>hellopbs</h1>"

    b1 = model.Book()
    b1.id = 1
    b1.name="天龙八部"
    b1.price=10
    b2 = model.Book()
    b2.id = 2
    b2.name = "射雕英雄传"
    b2.price = 10
    b3 = model.Book()
    b3.id = 3
    b3.name = "笑傲江湖"
    b3.price = 10
    # bl = [{b1},{b2},{b3}]

    user = None
    user = request.cookies.get("id")
    if user:
        print("之前已经登录过")
    else:
        user ='未登录'
        print("之前没有登录过")
    return render_template("index.html",books=[b1,b2,b3],name=user)
    # return render_template("homepage.html", books=[b1, b2, b3], name="李白")

@app.route("/news/<int:num>")
def news(num):
    print(num,type(num))
    # limit(20,20)

    # pagenews根据num查询数据库的信息显示页面内容
    # 在视图函数可以获取URL变量
    return render_template("news.html",pagenews=['那个男人又来了','震惊，据小道消息说。。。。','夭寿啦，五等分的男主？'],pagenum=num)

@app.route("/regist",methods=["POST","GET"])
def regist():
    if request.method == "GET":
        args = request.args
        name = args.get("username")
        values = args.get("password")
        print(name,values)
        print('收到get请求','返回注册界面')
        return render_template("regist.html",userinput="请输入您的用户名",pwdinput="请输入您的密码")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username,password)
        print('收到post请求','可以提取表单参数')
        # return "注册成功"
        if username == "":
            return render_template("regist.html",userinput="用户名不为空",pwdinput="请输入您的密码",uservalue=username)
        elif password == "":
            return render_template("regist.html", userinput="请输入您的用户名", pwdinput="密码不为空",uservalue=username)
        else:
            result = magen.inserUser(username,password)
            return redirect("/logind")

@app.route("/logind",methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("logind.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
        result = magen.checkUser(username,password)
        # print("-------->",result.username,result.id)
        if result != -1:
            uid = str(result.id)
            res = make_response(redirect('/'))
            res.set_cookie('id',result.username,expires=datetime.datetime.now()+ datetime.timedelta(days=7))
            res.set_cookie('userid', uid, expires=datetime.datetime.now() + datetime.timedelta(days=7))
            return res
        else:
            return redirect("/logind")

        # 自动在URL发起请求 请求list
        # return redirect('/list')

@app.route("/quit")
def quit():
    res = make_response(redirect("/"))
    res.delete_cookie("id")
    return res


@app.route("/list")
def list():
    # result = magen.checkBooks()
    # print(result,type(result))
    # user = request.cookies.get("id")
    # return render_template("list.html",infoarry=result,name=user)
    userid = request.cookies.get("userid")
    uid = int(userid)
    result = magen.checkmemor(uid)
    print(result, type(result))
    user = request.cookies.get("id")
    return render_template("list.html", infoarry=result, name=user)

@app.route("/detall/<id>")
def detall(id):
    # print("当前商品为",id)
    # return render_template("detall.html",detall="haodx",id = id)
    print(id,type(id))
    result = magen.checkmemor1(id)
    print(result, type(result),"_______________")
    return render_template("detall.html", infoarry=result)

# @app.route("/insertbook",methods=["POST","GET"])
# def insertbook():
#     if request.method == "GET":
#         args = request.args
#         bookname = args.get("booknmae")
#         price = args.get("price")
#         print(bookname,price)
#         return render_template("insertbook.html")
#     elif request.method == "POST":
#         bookname = request.form["bookname"]
#         price = request.form["price"]
#         print(bookname,price,"------>")
#         result = magen.inserBooks(bookname,price)
#
#         return redirect("/list")

@app.route("/deletebook/<id>")
def deletebook(id):
    print(id)
    magen.deleteBooks(id)
    return redirect("/list")


@app.route("/insertmemor",methods=["POST","GET"])
def insertmemor():
    if request.method == "GET":
        args = request.args
        memorname = args.get("memorname")
        memorcontent = args.get("memorcontent")
        userid = request.cookies.get("id")
        print(memorname,memorcontent,userid)
        return render_template("insertmemor.html")
    elif request.method == "POST":
        memorname = request.form["memorname"]
        memorcontent = request.form["memorcontent"]
        userid = request.cookies.get("userid")
        uid = int(userid)
        print(memorname,memorcontent,userid,"------>")
        result = magen.insertmemor(memorname,memorcontent,uid)

        return redirect("/list")

@app.route("/deletememor/<id>")
def deletememor(id):
    print(id)
    magen.deletememor(id)
    return redirect("/list")

@app.route("/updatememor/<int:id>",methods=["POST","GET"])
def updatememor(id):
    print(id)
    if request.method == "GET":
        resu = magen.checkmemor1(id)
        return render_template("updatememor.html",resu = resu,id = id)
    elif request.method == "POST":
        memorname = request.form["memorname"]
        memorcontent = request.form["memorcontent"]
        print(memorname, memorcontent)

        result = magen.updatememor(id,memorname,memorcontent)
        print(result,"###############################")
        return redirect("/list")

if __name__ =="__main__":
    app.run(host="192.168.12.168",port=8888)