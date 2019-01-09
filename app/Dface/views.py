from app import app
from app import db
from app.Dface import dface
from app.models import Alert_Jack
from flask import render_template, redirect, url_for, flash, request, session, Response, jsonify
import json
import pymysql


def executesql(sql1):
    db = pymysql.connect(host='172.16.1.6', user='root',
                         password='Tunicorn@hf#2017', db='dface_community', port=3306, charset='utf8mb4')
    cur = db.cursor()
    sql_select = sql1
    qret = cur.execute(sql_select)
    rows = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    return rows


@dface.route("/")
def index():
    if request.method == 'GET':
        return render_template("dface/admin_list.html")


# @dface.route("/verity_list/<string:deployid>/<string:sourceid>", methods=["GET", "POST"])
@dface.route("/verity_list/", methods=["GET", "POST"])
def verity_list():
    if request.method == "GET":
        return render_template("dface/verity_list.html")
    if request.method == "POST":
        # data = json.loads(request.form.get("data"))
        data = request.form
        # deployid = request.form["deployid"]
        # data = json.loads(str(request.data))
        deployid = data["deployid"]
        sourceid = data["sourceid"]
        # alerts = executesql("")
        sql = "select id, capture_id, capture_file_path,asset_path,face_id, score  from alert where deploy_id="+deployid+" and source_id="+sourceid
        alert_datas = executesql(sql)
        # alert_datas = list(alert_datas)
        # print(alert_datas)
        str = "/mnt/storage4/dface/6w_zhuzhou/430202193108083647.jpg"

        sql_2 = "select count(1)  from alert where deploy_id=" + deployid + " and source_id=" + sourceid
        sql_count = executesql(sql_2)
        return render_template("dface/verity_list.html", datas=alert_datas, sql_count=sql_count)




@dface.route("/verity_look/<string:alertid>", methods=["GET"])
def verity_look(alertid=None):
    if request.method == "GET":
        alertjacksql = "select alert_id, yesornot from alert_jack"
        alertjacks = executesql(alertjacksql)
        alertjacksql_self = "select alert_id, yesornot from alert_jack where alert_id='"+alertid+"'"
        alertjack = executesql(alertjacksql_self)
        sql = "select id, capture_file_path,asset_path,score, deploy_id, source_id from alert where id='"+alertid+"'"
        alertmes = executesql(sql)
        suc_count_sql = "select count(1)  from alert_jack where yesornot=1"
        err_count_sql = "select count(1)  from alert_jack where yesornot=0"
        suc_count = executesql(suc_count_sql)
        err_count = executesql(err_count_sql)
        return render_template(
            "dface/verity_look.html",
            alertjack=alertjack,
            alertjacks=alertjacks,
            alert=alertmes,
            alertid=alertid,
            suc_count=suc_count,
            err_count=err_count
        )


@dface.route("/verity_ajax/", methods=["POST"])
def verity_ajax():
    if request.method == "POST":
        # data = json.loads(request.data)
        data = request.form
        sourceid = data["sourceid"]
        deployid = data["deployid"]
        alertidold = data["alertid"]
        yesornot = data["yesornot"]
        # 保存数据
        alerts_count = Alert_Jack.query.filter_by(alert_id=alertidold).count()
        if alerts_count == 0:
            alert_jack = Alert_Jack(
                deploy_id=deployid,
                alert_id=alertidold,
                source_id=sourceid,
                yesornot=yesornot
            )
            db.session.add(alert_jack)
            db.session.commit()
        # 进入下一页
        sql = "select id, capture_file_path,asset_path,score, deploy_id, source_id  from alert where id='" + alertidold + "'"
        sqls="select id, capture_id, capture_file_path,asset_path,face_id, score  from alert where deploy_id="+deployid+" and source_id="+sourceid
        suc_count_sql = "select count(1)  from alert_jack where yesornot=1"
        err_count_sql = "select count(1)  from alert_jack where yesornot=0"
        datas = executesql(sqls)
        for i in range(0, len(datas)):
            if datas[i][0] == alertidold and i < len(datas)-1:
                # print(datas[i][0])
                alertidnew = datas[i+1][0]
                break

            if i == len(datas)-1:
                suc_count = executesql(suc_count_sql)
                err_count = executesql(err_count_sql)
                returndata = {
                    "status": 'success',
                    "alertnext": datas[i][0],
                    "msg": "匹配结束，当前为最后一条记录",
                    "suc_count":suc_count,
                    "err_count":err_count
                    }
                return Response(json.dumps(returndata), content_type='application/json')

        returndata = { "status": 'success', "alertnext": alertidnew, "msg": "下一个" }

        return Response(json.dumps(returndata), content_type='application/json')











