# Flaskr 开发说明

**官方文档**

<http://flask.pocoo.org/docs/0.12/tutorial/>

**涉及到的内容**:

* 连接sqlite，增删查
* 模板使用
* 应用上下文、请求上下文
* session
* 单元测试
* g,app.cli.command()

**知识点详解**

* 连接sqlite
```
    rv = sqlite3.connect("sqlite所在的位置")
    rv.row_factory = sqlite3.Row  # 将查询数据和查询语句组合为字典的形式，而非tuple
```
* 模板的使用
```python
render_template("index.html",name = "")
# 模板使用很简单
# 在模板中变量取值用 {{ name}}
# 判断 
{% if flag %} 
{% else %} 
{% endif %}
# 循环
{% for x in name%}
{% endfor%}
# 模板继承
{% extends 目标名%}
# url生成
{{url_for("index")}}
{{url_for("static",filename="")}} #静态资源
```
* g对象的使用
```python
# g 对象是和当前应用上下文有关的变量，能够保证线程安全，我们可以用来存储当前请求的一些信息
def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db
# 对于不同的请求，g对象的内容是不同的
```

* app.cli.command()
```python
#app.cli.command() 会给flask脚本注册一个新的命令，并且自动创建应用上下文
@app.cli.command('initdb') #注册initdb命令，
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
```

* 单元测试

根据flaskr.app.test_client()来发出get、post请求