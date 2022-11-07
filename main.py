import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import time
from datetime import datetime
import datetime

time.strftime('%d-%m-%Y')

@app.route('/Account', methods=['POST'])
def CreateAcc():
    try:        
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _DOB = _json['DOB']
        _username = _json['username']
        _pass = _json['pass']
        _ques = _json['ques']
        _ans = _json['ans']
        _sex = _json['sex']
        if _name and _email and _DOB and _username and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            _date = datetime.strptime(_DOB, '%d-%m-%Y')
            sqlQuery = "INSERT INTO User_(Name, DOB, Email,sex) Values (%s, %s, %s, %s)"
            bindData = (_name, _date, _email, _sex)
            cursor.execute(sqlQuery, bindData)
            _id = cursor.lastrowid
            cursor.execute("SELECT COUNT(*) FROM account WHERE username = %s", _username)
            rowcount = cursor.fetchall()
            if rowcount[0]['COUNT(*)'] != 0:
                respone = jsonify("Username is exist")
                respone.status_code = 200
                cursor.close()
                conn.close()
                return respone		
            sqlQuery = "INSERT INTO account(Username, Pass, Ques, Ans, UserID) values (%s, %s, %s, %s, %d)"
            bindData = (_username, _pass, _ques, _ans, _id)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('successfully!')
            respone.status_code = 200
            cursor.close() 
            conn.close()  
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)        
     
@app.route('/Account')
def CheckAcc():
    try:
        conn = mysql.connect()
        curson = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        username_ = json_['username']
        pass_ = json_['pass']
        curson.execute("SELECT Username, pass, role from account WHERE Username = %s", username_)
        rc = curson.rowcount
        if rc == 0:
            d = {"Status" : "username is not exist"}
            response = jsonify(d)
            response.status_code = 200
            return response
        d = curson._result.rows[0]
        if pass_ != d[1]:
            d = {"Status": "Wrong password"}
            response = jsonify(d)
            response.status_code = 200
            return response
        d = {"Status":"OK", "role": d[2]}
        response = jsonify(d)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            curson.close()
            conn.close()

@app.route('/CalcTDEE', methods = ['PUT'])
def update_calcTDEE():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        username = json_['username']
        height = json_['height']
        weight = json_['weight']
        activity = json_['activity']
        object_ = json_['object']
        if username and height and weight and activity and object_ and request.method == "PUT":
            cursor.execute("SELECT UserID from account WHERE Username = %s", username)
            rc = cursor.rowcount
            if rc == 0:
                reponse = jsonify()
                reponse.status_code = 404
                return reponse
            d = cursor._result.rows[0]
            userID = int(d[0])
            rc = cursor.execute("SELECT sex,DOB from user_ WHERE ID = %s", userID)
            d = cursor._result.rows[0]
            sex = d[0]
            DOB = d[1]
            age = datetime.date.today().year - DOB.year
            BMR = 0
            if sex == "male":
                BMR = 655 + 9.6*float(weight) + 1.8*float(height) - 4.7*age
            else:
                BMR = 66 + 13.7*float(weight) + 5 * float(height) - 6.8*age
            TDEE = 0
            if activity == "very little":
                TDEE = 1.2 * BMR
            elif activity == "little":
                TDEE = 1.375 * BMR
            elif activity == "normal":
                TDEE = 1.55 * BMR
            elif "heavy":
                TDEE = 1.725 * BMR
            else:
                TDEE = 1.9 * BMR
            if object_ == "increase":
                TDEE += 300
            elif object_ == "decrease":
                TDEE -= 300
            query = "UPDATE user_ set Height = %s, Weight = %s, acin = %s, TDEE = %s, object = %s WHERE ID = %s"
            bindData = (height, weight, activity, TDEE, object_, userID)
            cursor.execute(query,bindData)
            conn.commit()
            d = {"Status" :"OK", "TDEE": TDEE}
            reponse = jsonify(d)
            reponse.status_code = 200
            return reponse
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/food', methods = ['POST'])
def addFood():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        name = json_['name']
        calo = json_['calo']
        protein = json_['protein']
        fat = json_['fat']
        description = json_['description']
        if name and calo and protein and fat and description:
            cursor.execute("SELECT * from food WHERE Name = %s", name)
            if cursor.rowcount != 0:
                d = {"status" :"Food name have already existed"}
                reponse = jsonify(d)
                reponse.status_code = 200
                return reponse
            query = "INSERT into food(Name, Calo, Protein, Fat, Des) VALUES (%s, %s, %s,%s,%s)"
            bindData = (name, calo, protein, fat, description)
            cursor.execute(query, bindData)
            conn.commit()
            d = {"status" : "OK"}
            reponse = jsonify(d)
            reponse.status_code = 200
            return reponse
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/food' , methods = ['PUT'])
def editFood():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        calo = json_['calo']
        fat = json_['fat']
        protein = json_['protein']
        des = json_['description']
        IDfood = json_['ID']
        if calo and fat and protein and des and IDfood:
            sqlquery = "UPDATE food set Calo = %s protein = %s fat = %s des = %s WHERE ID = %s"
            bindData = (calo, protein, fat, des, IDfood)
            cursor.execute(sqlquery, bindData)
            conn.commit()
            d = {"status" : "OK"}
            reponse = jsonify(d)
            reponse.status_code = 200
            return reponse
        else:
            reponse = jsonify("wrong json")
            reponse.status_code = 200
            return reponse
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/favList', methods = ['POST'])
def addFav():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        UserID = json_['UserID']
        FoodID = json_['FoodID']
        if UserID and FoodID:
            rc = cursor.execute("SELECT * FROM pick WHERE userID = %s and foodID = %s", (UserID,FoodID))
            if rc != 0:
                reponse = jsonify("existence")
                return reponse
            query = "INSERT into pick (FoodID,UserID, type) values (%s,%s,%s)"
            bindData = (FoodID, UserID, "favorite")
            cursor.execute(query, bindData)
            conn.commit()
            d = {"status" : "OK"}
            reponse = jsonify(d)
            reponse.status_code = 200
            return reponse
        else:
            reponse = jsonify("wrong json")
            reponse.status_code = 200
            return reponse 
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/favList')
def getFavList():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        UserID = json_['UserID']
        if UserID:
            sqlquery = "SELECT Name,Calo,Protein,Fat,Des from food WHERE ID IN (SELECT FoodID from pick WHERE UserID = %s)"
            bindData = (UserID)
            cursor.execute(sqlquery, bindData)
            res = cursor.fetchall()
            reponse = jsonify(res)
            reponse.status_code = 200
            return reponse
        else:
            reponse = jsonify("wrong json")
            reponse.status_code = 200
            return reponse 
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.debug = True
    app.run()