import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('form.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route("/lookup", methods=['POST', 'GET'])
def echo():
    if request.method == 'POST':
        connection = sqlite3.connect("flag.db")
        cursor = connection.cursor()
        statement = f"SELECT flag FROM users WHERE username='{request.form['username']}' AND password='{request.form['password']}'"
        try:
            cursor.execute(f"SELECT flag FROM users WHERE username='{request.form['username']}' AND password='{request.form['password']}'")
        except sqlite3.OperationalError:
            return render_template("results.html", result="OPERATION ERROR", statement=statement)
        else:
            if str(cursor.fetchall()) == "[]":
                return render_template("results.html", result="wrong username or password", statement=statement)
        try:
            cursor.execute(f"SELECT flag FROM users WHERE username='{request.form['username']}' AND password='{request.form['password']}'")
        except sqlite3.OperationalError:
            return render_template("results.html", result="OPERATION ERROR", statement=statement)
        else:
            return render_template("results.html", result=str(cursor.fetchall()[0][0]), statement=statement)
    elif request.method == "GET":
        return redirect('/'), 302
app.run(threaded=True, host="0.0.0.0")
