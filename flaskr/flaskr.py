import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField,StringField,SelectField
from flask_bootstrap import  Bootstrap


class SubmitForm(FlaskForm):
    xq = SelectField("校区",choices=[("2", "崂山校区"), ("1", "鱼山校区")])
    lx = SelectField("类型",choices=[("1", "四级"), ("2", "六级")])
    js = StringField("教室号")
    kch = StringField("考场号")
    submit = SubmitField("提交")


class QueryForm(FlaskForm):
    xq = SelectField("校区",choices=[("2", "崂山校区"), ("1", "鱼山校区")])
    lx = SelectField("类型",choices=[("1", "四级"), ("2", "六级")])
    js = StringField("教室号")
    submit = SubmitField("提交")


app = Flask(__name__)
app.config.update(
    dict(
        DATABASE=os.path.join(app.root_path,"flaskr.db"),
        SECRET_KEY=b'\n\xc5gH\x1a\xcd\xfd<;\xbb\xb0\xbd\xb6\xef\x98Y|/\xb7\x9d',
        USERNAME="admin",
        PASSWORD="password"
    )
)
bootstrap = Bootstrap(app)
app.config.from_envvar("FLASKR_SETTINGS", silent=True)
# 设置一个名为 FLASKR_SETTINGS 环境变量来设定一个配置文件载入后是否覆盖默认值。
# 静默开关告诉 Flask 不去关心这个环境变量键值是否存


def connect_db():
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row  # 将查询数据和查询语句组合为字典的形式，而非tuple
    return rv


def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource("install.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command("initdb")  # app.cli.command() decorator registers a new command with the flask script.
def initdb_command():
    init_db()
    print("Initialized the database")


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


@app.route("/")
def show_entries():
    db = get_db()
    cur = db.execute("select id,title,content FROM entries")
    entries = cur.fetchall()
    return render_template("show.html", entries=entries)


@app.route("/add/", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        db = get_db()
        db.execute("INSERT  INTO entries (title,content) VALUES (?,?)", [title, content])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for("show_entries"))
    else:
        return render_template("add.html")


@app.route("/login", methods=["POST","GET"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == app.config['USERNAME'] and password == app.config["PASSWORD"]:
            session["uid"] = username
            flash("登陆成功",)
            return redirect(url_for("show_entries"))
        else:
            error = "账号或密码错误"
    return render_template("login.html", title="登陆", error=error)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("uid")
    flash("注销成功!")
    return redirect(url_for("login"))


@app.route("/cet_submit",methods=["POST","GET"])
def cet_submit():
    form = SubmitForm()
    if form.validate_on_submit():
        data = form.data
        db = get_db()
        db.execute("INSERT  INTO cet (xq,lx,js,kch) VALUES (?,?,?,?)",
                   [form.xq.data,form.lx.data,form.js.data,form.kch.data])
        db.commit()
        flash('感谢你的提交!')
        return redirect(url_for("cet_query"))
    return render_template("submit.html", form=form, title="四六级")


@app.route("/cet_query/",methods=['POST','GET'])
def cet_query():
    form = QueryForm()
    db = get_db()
    if form.validate_on_submit():
        xq = form.xq.data
        lx = form.lx.data
        js = form.js.data
        js = "%" + js + "%"
        cur = db.execute("select xq,lx,js,kch FROM cet where xq = ? and lx = ? and js like ?",
                         [xq, lx, js])
    else:
        cur = db.execute("select xq,lx,js,kch FROM cet  group by xq,kch")
    entries = cur.fetchall()
    return render_template("cet_query.html", form = form, entries=entries)


if __name__ == "__main__":
    app.run(debug=True)



