from datetime import timedelta
from flask import Flask, render_template, request, abort
import json
import mysql.connector

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route('/')
def hello_world():
    return render_template('ttt.html')


@app.route('/index/')
def index():
    try:
        connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
        cursor = connection.cursor()
        opt = request.args.get('opt')
        if opt == '1':
            illness = request.args.get('illness')
            cursor.execute("SELECT * FROM medical_info.medical_record WHERE name=%s", [illness])
            res = cursor.fetchone()

        elif opt == '2':
            symptom = request.args.get('symptom')

        elif opt == '3':
            herb = request.args.get('herb')
            cursor.execute("SELECT * FROM medical_info.herb WHERE name LIKE '%%%s%%'" % herb)
            herbs = cursor.fetchall()
            connection.close()
            cursor.close()
            if len(herbs) == 0:
                herbs = None
            return render_template('herb.html', herbs=herbs)
        elif opt == '4':
            record = request.args.get('record')
            cursor.execute("SELECT * FROM medical_info.prescription WHERE name=%s", [record])
            res = cursor.fetchone()
        else:
            return render_template('herb.html')
    except mysql.connector.Error as e:
        abort(500)


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/display', methods=['GET', 'POST'])
def display():
    """
    获取ajax
    :return:
    """
    data = request.get_data()
    data = json.loads(data)


@app.errorhandler(500)
def error(e):
    return render_template("500.html"), 500


@app.errorhandler(404)
def notFound(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run()
