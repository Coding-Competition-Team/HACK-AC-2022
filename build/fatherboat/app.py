from flask import Flask, render_template, request, Response, make_response, redirect
from urllib.parse import urlparse

from bot import Bot

app = Flask(__name__)

@app.route('/')
def index():
    posts = request.cookies
    return render_template("index.html", posts=posts)

@app.route('/title')
def title():
    posts = request.cookies
    if title := request.args.get('title', ''):
        if any([post.startswith(title) for post in posts]):
            if any([title == post for post in posts]):
                return Response(render_template('post.html', title=title, content=posts[title]), status=200)
            else:
                return Response(render_template('found.html', title=title), status=201)
        else:
            return Response(render_template('not-found.html', title=title), status=404)
    else:
        return Response("Why liddat", status=400)

@app.route('/body')
def body():
    posts = request.cookies
    if search_body := request.args.get('body'):
        for title, body in posts.items():
            if body == search_body:
                return Response(render_template('post.html', title=title, content=posts[title]), status=200)
            elif body.endswith(search_body):
                return Response(render_template('found-body.html'), status=201)
        else:
            return Response(render_template('not-found-body.html'), status=404)
    else:
        return Response("Why liddat", status=400)

@app.route('/create', methods=["POST"])
def create():
    title = request.form.get('title')
    content = request.form.get('content')
    if not title or not content:
        return Response('Bad Request', 400)
    res = make_response(redirect(f'/title?title={title}'))
    res.set_cookie(title, content, httponly=True)
    return res

@app.route('/sharelobang', methods=["GET", "POST"])
def visit():
    if request.method == "GET":
        return render_template("share.html")
    else:
        if url := request.form.get('url'):
            if urlparse(url).netloc != "localhost:5000":
                return Response('eh this one not from our site... from mothership isit??', status=400)
            thread = Bot(url)
            thread.start()
            return Response('Thanks ah!', status=200)
        return Response('Why liddat', status=400)
