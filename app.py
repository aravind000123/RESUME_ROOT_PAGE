from flask import Flask,render_template,request,redirect
import sqlite3
import os
from datetime import datetime

app=Flask(__name__)

def create_table():
    conn=sqlite3.connect("comments.db")
    cursor=conn.cursor()
    
    cursor.execute("create table if not exists comment(id integer primary key autoincrement,comment_text text)")

    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/post_comment',methods=["GET","POST"])
def write_comments():
    if request.method=="GET":
        return render_template("write_comments.html")
    if request.method=="POST":
        posted_comment=request.form["written_comment"]
        conn=sqlite3.connect("comments.db")
        cursor=conn.cursor()

        cursor.execute("insert into comment(comment_text) values(?)",(posted_comment,))

        conn.commit()
        conn.close()

    return redirect("/projects")

@app.route("/read_comments")
def read_comments():
        conn=sqlite3.connect("comments.db")
        cursor=conn.cursor()

        cursor.execute("select * from comment order by id desc")
        result=cursor.fetchall()

        conn.commit()
        conn.close()

        return render_template("read_comments.html",table_comments=result)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
