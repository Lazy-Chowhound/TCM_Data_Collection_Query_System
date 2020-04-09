import json
from datetime import timedelta
import mysql.connector
from flask import Flask, render_template, request, abort
from pypinyin import lazy_pinyin

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
            page = request.args.get('page')
            if illness is None:
                return render_template('record.html')
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
                count = getPage(catalogs, 4)
                pageCount = []
                for i in range(count):
                    pageCount.append(i + 1)
                beg = (int(page) - 1) * 4
                catalogs = catalogs[beg:beg + 4]
                return render_template('record.html', catalogs=catalogs, pageCount=pageCount)

        elif opt == '2':
            symptom = request.args.get('symptom')
            page = request.args.get('page')
            if symptom is None:
                return render_template('record.html')
            else:
                cursor.execute("SELECT * FROM medical_info.medical_record WHERE diagnose LIKE '%%%s%%'" % symptom)
                res = cursor.fetchall()
                connection.close()
                cursor.close()
                catalogs = []
                for each in res:
                    catalog = [each[0]]
                    text = each[1]

                    beg = text.find('主诉：')
                    end = text.find(' ', beg)
                    catalog.append(text[beg + 3:end])

                    beg = text.find('出处：')
                    end = text.find(' ', beg)
                    catalog.append(text[beg + 3:end])

                    catalogs.append(catalog)
                count = getPage(catalogs, 4)
                pageCount = []
                for i in range(count):
                    pageCount.append(i + 1)
                beg = (int(page) - 1) * 4
                catalogs = catalogs[beg:beg + 4]
                return render_template('record.html', catalogs=catalogs, pageCount=pageCount)
        elif opt == '3':
            herb = request.args.get('herb')
            page = request.args.get('page')
            if herb is None:
                return render_template('herb.html')
            else:
                cursor.execute("SELECT * FROM medical_info.herb WHERE name LIKE '%%%s%%'" % herb)
                herbs = cursor.fetchall()
                count = getPage(herbs, 5)
                pageCount = []
                for i in range(count):
                    pageCount.append(i + 1)
                beg = (int(page) - 1) * 5
                herbs = herbs[beg:beg + 5]
                connection.close()
                cursor.close()
                return render_template('herb.html', herbs=herbs, pageCount=pageCount)
        elif opt == '4':
            alpha = request.args.get("alpha")
            name = request.args.get("prescriptionName")
            prescription = request.args.get("prescription")
            # 按首字母查询
            if alpha is not None and name is None and prescription is None:
                page = request.args.get('page')
                prescriptionAlpha = []
                cursor.execute("SELECT * FROM medical_info.prescription")
                res = cursor.fetchall()
                beg = (int(page) - 1) * 52
                for each in res:
                    if getPinyinInitial(each[0]).upper() == alpha:
                        prescriptionAlpha.append(each)
                count = getPage(prescriptionAlpha, 52)
                pageCount = []
                for i in range(count):
                    pageCount.append(int(i + 1))
                prescriptionAlpha = prescriptionAlpha[beg:beg + 52]
                return render_template('prescription.html', prescriptionAlpha=prescriptionAlpha, pageCount=pageCount)
            # 按关键字查询
            elif name is not None and alpha is None and prescription is None:
                page = request.args.get('page')
                prescriptionCata = []
                cursor.execute("SELECT * FROM medical_info.prescription WHERE name LIKE '%%%s%%'" % name)
                res = cursor.fetchall()
                for each in res:
                    presCata = [each[0], each[3], each[5]]
                    prescriptionCata.append(presCata)
                count = getPage(prescriptionCata, 5)
                pageCount = []
                for i in range(count):
                    pageCount.append(int(i + 1))
                beg = (int(page) - 1) * 5
                prescriptionCata = prescriptionCata[beg:beg + 5]
                return render_template('prescription.html', prescriptionCata=prescriptionCata, pageCount=pageCount)
            # 某个经方
            elif prescription is not None and alpha is None and name is None:
                cursor.execute("SELECT * FROM medical_info.prescription WHERE name=%s", [prescription])
                pres = cursor.fetchone()
                return render_template('prescription.html', prescription=pres)
            elif name is None and alpha is None and prescription is None:
                return render_template('prescription.html')
        else:
            return render_template('404.html')
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


@app.errorhandler(500)
def error(e):
    return render_template("500.html"), 500


@app.errorhandler(404)
def notFound(e):
    return render_template("404.html"), 404


def getPinyinInitial(string):
    """
    获取中文词语的拼音首字母
    :param string:
    :return:
    """
    pinyinList = lazy_pinyin(string, errors='ignore')
    return pinyinList[0][0:1]


def getPage(myList, eachPageCount):
    """
    获取页数
    :param myList:
    :param eachPageCount: 每页个数
    :return:
    """
    length = len(myList)
    count = length // eachPageCount
    if length % eachPageCount != 0:
        count += 1
    return count


if __name__ == '__main__':
    app.run()
