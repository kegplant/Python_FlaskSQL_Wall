from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key='poshit'
mysql = MySQLConnector(app,'emails')
@app.route('/')
def index():
    query = "SELECT * FROM emails"                           # define your query
    emails = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', emails=emails) # pass data to our template
@app.route('/insert',methods=['POST'])
def insert():
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid Email Address!')
        return redirect('/')
    else:
        query='insert into emails (email,date_created) values (:email,now())'
        data={'email':request.form['email']}
        mysql.query_db(query,data)
        # print query
        # print data
        return redirect('/success')
@app.route('/success')
def success():
    query=('select * from emails')
    emails=mysql.query_db(query)                           # run query with query_db()
    return render_template('success.html',emails=emails)
@app.route('/delete/<id>')
def deleteEmail(id):
    query=('delete from emails where id= :id')
    data={'id':id}
    # result=
    mysql.query_db(query,data)
    query=('select * from emails')
    emails=mysql.query_db(query)
    # if result:
    flash('email deleted')
    return redirect('/success')
app.run(debug=True)
#style, priority
