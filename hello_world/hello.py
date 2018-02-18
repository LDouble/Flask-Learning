from flask import Flask,flash
from flask import render_template,url_for,redirect, request, session, send_from_directory
from werkzeug.utils import secure_filename
from redis import Redis
import json
app = Flask(__name__)
app.secret_key = "\xeew\xe4\xc0\xee\xb1]\x9b\xa0\x9e)\x15Qhem\xe5\xf17\xd6\xceB\xb7\xb4"
UPLOAD_FOLDER = './uploads/'

@app.route("/start/")
def start():
    """Let's start to use Flask"""
    return render_template("start.html", title="一个小开始", code="""
    from flask import Flask #从flask中导入Flask类
    app = Flask(__name__) #实例化Flask类，参数__name__用于确定程序目录
    
    app.debug = True #开启debug模式
    @app.route("/start/") #设置路由规则并绑定到函数start
    def start():
        return render_template("start.html", title="一个小开始",code = "the code you see" #调用模板并渲染，
        #其中title和code为参数，在模板中使用{{title}}即可获得
    
    
    if __name__ == "__main__": #如果当前模块被运行，而非导入，
        app.run() #启动服务器,可通过host、port、debug等设置参数
    """)


@app.route("/")
def index():
    return redirect(url_for("api"))


@app.route("/api/")
def api():
    return render_template("api.html", title="Flask学习实例")


@app.route("/success/")
def success():
    url = request.args.get("url")
    return render_template("success.html", url=url)


def do_register():
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        r = Redis()
        flag = r.get(username)
        if flag:
            flash("该用户名已存在", "register_err")
            return redirect(url_for("register"))
        else:
            r.append(username,password)
            message = "恭喜你，注册成功"
            flash(message)
            return render_template("success.html", url=url_for("login"))
    else:
        flash("账号或密码不能为空", "register_err")
        return redirect(url_for("register"))


@app.route("/user/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        return do_register()
    else:
        return render_template("register.html", title="用户注册", code="""
def do_register():
    username = request.form.get("username") # 获取form表单
    password = request.form.get("password")
    if username and password: 
        r = Redis() # 调用redis
        flag = r.get(username)
        if flag:
            return render_template('register.html', error="该用户名已存在")
        else:
            r.append(username,password)
            message = "恭喜你，注册成功" 
            flash(message) # 闪现消息，用于提示
            return redirect(url_for("success", redirect=url_for("login")))
    else:
        return render_template('register.html', error="账号或密码不能为空")


@app.route("/user/register", methods=["POST", "GET"])
def register():
    if request.method == "POST": # 判断请求的类型
        return do_register() # 处理POST请求
    else:
        return render_template("register.html", title="用户注册", code="the code you see" # 渲染模板，
        """)


def do_login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        r = Redis()
        pwd = r.get(username)
        print(pwd)
        if pwd.decode() == password:
            session["uid"] = username
            flash("登录成功")
            return redirect(url_for("success", url=url_for("my")))
        else:
            flash("登录失败,账号或密码错误", "login_error")
            return redirect(url_for("login"))
    else:
        flash("账号密码不能为空", "login_error")
        return redirect(url_for("login"))


@app.route("/user/login/",methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return do_login()
    else:
        return render_template("login.html", title="用户登录", code="""
def do_login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        r = Redis()
        pwd = r.get(username)
        if pwd == password:
            session["uid"] = username
            flash("登录成功")
            return redirect(url_for("success", url=url_for("index")))
        else:
            flash("登录失败,账号或密码错误","login_error")
    else:
        flash("账号密码不能为空", "login_error")
        return redirect(url_for("login"))


@app.route("/user/login")
def login():
    if request.method == "POSt":
        do_login()
    else:
        return render_template("login.html", title="用户登录", code="the code you see"
        """)


@app.route("/user/my/")
def my():
    uid = session.get("uid")
    if uid:
        data = dict();
        pic = session.get(uid+"pic")
        if pic:
            data["pic"] = url_for("uploads", filename=pic)
        data["uid"] = uid
        return render_template("my.html", title="我的首页", data=data, code="""
@app.route("/user/my")
def my():
    uid = session.get("uid") #从session中查找是否有该用户
    if uid:
        data = dict();
        pic = session.get(uid+"pic")
        if pic:
            data["pic"] = url_for("uploads", filename=pic)
        data["uid"] = uid
        return render_template("my.html", title="我的首页", data=data, code="the code you see")
    else:
        return redirect("login")  # 未登陆跳转到登录
        
        
@app.route("/user/upload_pic/", methods=["POST", "GET"])
def upload_pic():
    if request.method == "POST":
        f = request.files.get("pic")
        uid = session["uid"]
        if f and uid:
            f.save(UPLOAD_FOLDER+secure_filename(f.filename))
            session[uid+"pic"] = secure_filename(f.filename)
            return redirect(url_for("my"))
    else:
        flash("请求错误", "my_error")
        return redirect(url_for("my"))


@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
        """)
    else:
        return redirect("login")  # 未登陆跳转到登录


@app.route("/user/upload_pic/", methods=["POST", "GET"])
def upload_pic():
    if request.method == "POST":
        f = request.files.get("pic")
        uid = session["uid"]
        if f and uid:
            f.save(UPLOAD_FOLDER+secure_filename(f.filename))
            session[uid+"pic"] = secure_filename(f.filename)
            return redirect(url_for("my"))
    else:
        flash("请求错误", "my_error")
        return redirect(url_for("my"))


@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/headers/",methods=['POST', 'GET'])
def header():
    data = request.headers
    headers = dict()
    for key, value in data:
        headers[key] = value
    str_header = json.dumps(headers)
    return render_template("header.html", title="header信息展示", str=str_header, code="""
def header():
    data = request.headers
    headers = dict()
    for key, value in data:
        headers[key] = value
    str_header = json.dumps(headers)
    return render_template("header.html", str=str_header, code="the code you see")
    """)


@app.route("/cookie/", methods=["POST", "GET"])
def cookie():
    name, value = None, None
    if request.method == "POST":
        name = request.form.get("name")
        value = request.form.get("value")
        flash("设置cookie成功")
        res = redirect(url_for("success", url=url_for("cookie")))
        res.set_cookie(name,value)
        return res
    str_cookie = json.dumps(request.cookies)
    res = render_template("cookie.html", str=str_cookie, title="cookie的添加与查询", code="""
@app.route("/cookie/", methods=["POST", "GET"])
def cookie():
    name, value = None, None
    if request.method == "POST":
        name = request.form.get("name")
        value = request.form.get("value")
        flash("设置cookie成功")
        res = redirect(url_for("success", url=url_for("cookie")))
        res.set_cookie(name,value)
        return res
    str_cookie = json.dumps(request.cookies)
    res = render_template("cookie.html", str=str_cookie, code="the code you see")
    return res
    """)
    return res


@app.route("/log/")
def log():
    app.logger.error("test")
    return ""


if __name__ == "__main__":
    app.run()

