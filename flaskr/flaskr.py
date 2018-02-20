import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask(__name__)
app.config.update(
    dict(
        DATABASE=os.path.join(app.root_path,"flaskr.db"),
        SECRET_KEY=b'\n\xc5gH\x1a\xcd\xfd<;\xbb\xb0\xbd\xb6\xef\x98Y|/\xb7\x9d',
        USERNAME="admin",
        PASSWORD="password"
    )
)
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


if __name__ == "__main__":
    app.run(debug=True)



