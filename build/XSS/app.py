import sqlite3
from uuid import uuid4

from flask import Flask, make_response, redirect, render_template, request

from bot import Bot

app = Flask(__name__)

@app.route('/')
def main():
    if (uuid := request.cookies.get('uuid')):
        with sqlite3.connect('./db') as cnx:
            cursor = cnx.cursor()
            cursor.execute('SELECT post FROM users WHERE uuid = ?', (uuid,))
            if (post := cursor.fetchone()) is None:
                # invalid uuid
                return render_template('login.html')
            else:
                return render_template('post.html', post=post)
        return render_template('post.html')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if (username := request.form.get('username')) and (password := request.form.get('password')):
        with sqlite3.connect('./db') as cnx:
            cursor = cnx.cursor()
            cursor.execute('SELECT uuid FROM users WHERE username = ? and password = ?', (username, password))
            if (uuid := cursor.fetchone()) is None:
                uuid = str(uuid4())
                cursor.execute('INSERT INTO users (username, password, uuid) VALUES (?, ?, ?)', (username, password, uuid))
            else:
                uuid = uuid[0]
        resp = make_response(redirect('/'))
        resp.set_cookie('uuid', uuid)
        return resp
    else:
        return 'Username/password missing.'

@app.route('/post', methods=['POST'])
def post():
    if (uuid := request.cookies.get('uuid')):
        if (post := request.form.get('body')):
            with sqlite3.connect('./db') as cnx:
                cursor = cnx.cursor()
                if uuid == cursor.execute('SELECT uuid FROM users WHERE username = "admin"').fetchone()[0]:
                    return 'oi u r not allowed to change my post go away >:('
                cursor.execute('UPDATE users SET post = ? WHERE uuid = ?', (post, uuid)) 
                if cursor.rowcount == 0:
                    return 'Invalid uuid'
                else:
                    return post
    return 'No UUID/body found'

@app.route('/visit/<uuid>')
def visit(uuid):
    thread = Bot(uuid)
    thread.start()
    return 'very interesting post, from that i\'ve gotten your ip and will now proceed to HACK you!!!!!!!!!!!!!!!!!!!!'

@app.route('/render/<uuid>')
def render(uuid):
    with sqlite3.connect('./db') as cnx:
        cursor = cnx.cursor()
        cursor.execute('SELECT post FROM users WHERE uuid = ?', (uuid,))
        if (post := cursor.fetchone()):
            return post[0]
        else:
            return redirect('/')

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
