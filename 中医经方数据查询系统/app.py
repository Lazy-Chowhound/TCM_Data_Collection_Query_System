import json
from datetime import timedelta
import mysql.connector
from flask import Flask, render_template, request, abort

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route('/')
def hello_world():
    return render_template('search.html')


@app.route('/index/')
def index():
    try:
        connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
        cursor = connection.cursor()
        opt = request.args.get('opt')
        if opt == '1':
            illness = request.args.get('illness')
            if illness is None:
                return render_template('record.html', catalogs=None)
            else:
                cursor.execute("SELECT * FROM medical_info.medical_record WHERE name LIKE '%%%s%%'" % illness)
                illnesses = cursor.fetchall()
                connection.close()
                cursor.close()
                catalogs = []
                for illness in illnesses:
                    catalog = [illness[0]]
                    text = illness[1]

                    beg = text.find('主诉：')
                    end = text.find(' ', beg)
                    catalog.append(text[beg + 3:end])

                    beg = text.find('出处：')
                    end = text.find(' ', beg)
                    catalog.append(text[beg + 3:end])

                    catalogs.append(catalog)
                return render_template('record.html', catalogs=catalogs)

        elif opt == '2':
            symptom = request.args.get('symptom')

        elif opt == '3':
            herb = request.args.get('herb')
            if herb is None:
                return render_template('herb.html', herbs=None)
            else:
                cursor.execute("SELECT * FROM medical_info.herb WHERE name LIKE '%%%s%%'" % herb)
                herbs = cursor.fetchall()
                connection.close()
                cursor.close()
                return render_template('herb.html', herbs=herbs)
        elif opt == '4':
            prescription = request.args.get('prescription')
            if prescription is None:
                return render_template('prescription.html', prescription=None)
            cursor.execute("SELECT * FROM medical_info.prescription WHERE name=%s", [prescription])
            res = cursor.fetchone()
        else:
            return render_template('index_base.html')
    except mysql.connector.Error as e:
        abort(500)


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/record')
def displayRecord():
    try:
        connection = mysql.connector.connect(user='root', password='061210', database='medical_info')
        cursor = connection.cursor()
        name = request.args.get('name')
        cursor.execute("SELECT * FROM medical_info.medical_record WHERE name=%s", [name])
        record = cursor.fetchone()

        return render_template('detail.html', name=name)
    except mysql.connector.Error as e:
        abort(500)


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
