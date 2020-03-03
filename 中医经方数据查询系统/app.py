from datetime import timedelta
from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route('/')
def hello_world():
    return render_template('navigate.html')


@app.route('/index/')
def index():
    sym = request.args.get('sym')
    return render_template('index.html', sym=sym)


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/display', methods=['GET', 'POST'])
def display():
    # 获取后端json
    data = request.get_data()
    symptom = json.loads(data)
    print(symptom)
    return json.dumps(symptom)


if __name__ == '__main__':
    app.run()
