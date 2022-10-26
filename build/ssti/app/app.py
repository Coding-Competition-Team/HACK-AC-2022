from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/intelligent', methods=['POST'])
def intelligent():
    return render_template_string(request.form['scholar'])

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
