import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request, render_template
import time
from datetime import datetime
import datetime

time.strftime('%d-%m-%Y')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods= ['POST'])
def addFoodWeb():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        name = request.form['name']
        calo = request.form['calo']
        protein = request.form['protein']
        fat = request.form['fat']
        description = request.form['desc']
        link = request.form['link']
        recipt = request.form['recipt']
        if name and calo and protein and fat and description:
            cursor.execute("SELECT * from food WHERE Name = %s", name)
            if cursor.rowcount != 0:
                d = {"status" :"Food name have already existed"}
                reponse = jsonify(d)
                reponse.status_code = 200
                return reponse
            query = "INSERT into food(Name, Calo, Protein, Fat, Des, image, recipt) VALUES (%s, %s, %s,%s,%s,%s, %s)"
            bindData = (name, calo, protein, fat, description,link, recipt)
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
            _date = datetime.datetime.strptime(_DOB, '%d-%m-%Y')
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
            sqlQuery = "INSERT INTO account(Username, Pass, Ques, Ans, UserID) values (%s, %s, %s, %s, %s)"
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
        link = json_['link']
        recipt = json_['recipt']
        if name and calo and protein and fat and description:
            cursor.execute("SELECT * from food WHERE Name = %s", name)
            if cursor.rowcount != 0:
                d = {"status" :"Food name have already existed"}
                reponse = jsonify(d)
                reponse.status_code = 200
                return reponse
            query = "INSERT into food(Name, Calo, Protein, Fat, Des, image, recipt) VALUES (%s, %s, %s,%s,%s,%s, %s)"
            bindData = (name, calo, protein, fat, description, link, recipt)
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
        recipt = json_['recipt']
        if calo and fat and protein and des and IDfood:
            sqlquery = "UPDATE food set Calo = %s protein = %s fat = %s des = %s recipt = %s WHERE ID = %s"
            bindData = (calo, protein, fat, des,recipt ,IDfood)
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

@app.route('/food')
def getFood():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        foodID = json_["foodID"]
        rc = cursor.execute("select * from food where ID = %s", foodID)
        if rc == 0:
            reponse = jsonify("no food")
            reponse.status_code = 200
            return reponse
        res = cursor.fetchall()
        reponse = jsonify(res[0])
        reponse.status_code = 200
        return reponse
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/food', methods = ['DELETE'])
def delFood():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        foodID = json_["foodID"]
        rc = cursor.execute("delete from food where ID = %s", foodID)
        if rc == 0:
            reponse = jsonify("no food")
            reponse.status_code = 200
            return reponse
        conn.commit()
        reponse = jsonify("OK")
        reponse.status_code = 200
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
        if UserID and request.method == "GET":
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
    
@app.route('/favList', methods = ['DELETE'])
def delFoodFromList():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        UserID = json_['UserID']
        FoodID = json_['FoodID']
        if UserID and FoodID and request.method == "DELETE":
            rc = cursor.execute("DELETE FROM pick WHERE FoodID = %s and UserID = %s and type = %s", (FoodID, UserID, "favorite"))
            conn.commit()
            if rc != 0:
                d = {"Status" : "OK"}
                reponse = jsonify(d)
                reponse.status_code = 200
                return reponse
            else:
                d = {"Status": "Not exist"}
                reponse = jsonify(d)
                reponse.status_code = 200
                return reponse
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/plan', methods = ['POST'])
def createPlan():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        userID = json_['userID']
        rc = cursor.execute("SELECT date_,type_ from pick where UserID = %s", (userID))
        if rc != 0 and cursor._result.rows[0][0] == datetime.date.today() and cursor._result.rows[0][1] == "plan":
            d = {"status": "existence"}
            reponse = jsonify(d)
            reponse.status_code = 200
            return reponse
        breakfast = json_['breakfast']
        lunch = json_['lunch']
        dinner = json_['dinner']
        rc = cursor.execute("SELECT calo from food WHERE id in (%s,%s,%s)", (breakfast, dinner, lunch))
        res = cursor._rows
        s = 0
        for x in res:
            s += x['calo']
        cursor.execute("SELECT TDEE FROM user_ WHERE id = %s", (userID))
        tdee = cursor._rows[0]['TDEE']
        if tdee - s > 500:
            reponse = jsonify("not enough")
            reponse.status_code = 200
            return reponse
        elif s - tdee > 500:
            reponse = jsonify("too much")
            reponse.status_code = 200
            return reponse
        cursor.execute("INSERT into pick(userid, foodid, time_, type_, date_) VALUES (%s, %s, %s, %s, %s)", (userID, breakfast, "breakfast", "plan", datetime.date.today()))
        cursor.execute("INSERT into pick(userid, foodid, time_, type_, date_) VALUES (%s, %s, %s, %s, %s)", (userID, lunch, "lunch", "plan", datetime.date.today()))
        cursor.execute("INSERT into pick(userid, foodid, time_, type_, date_) VALUES (%s, %s, %s, %s, %s)", (userID, dinner, "dinner", "plan", datetime.date.today()))
        conn.commit()
        reponse = jsonify("OK")
        reponse.status_code = 200
        return reponse
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/plan')
def getFoodPlan():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        userID = json_['userID']
        rc = cursor.execute("SELECT foodID FROM pick WHERE UserID = %s and date_ = DATE(now())", userID)
        if rc == 0:
            reponse = jsonify("Not exist")
            reponse.status_code = 200
            return reponse
        res = cursor.fetchall()
        cursor.execute("SELECT * FROM food WHERE id in (%s, %s,%s)", (res[0]['foodID'], res[1]['foodID'], res[2]['foodID']))
        final = cursor.fetchall()
        reponse = jsonify(final)
        reponse.status_code = 200
        return reponse
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
            
@app.route('/search', methods = ['GET'])
def findByName():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        text = json_['text']
        cursor.execute("select *, match (Des) against (%s) as score from food where  match (Des) against (%s) > 0", (text, text))
        res = cursor.fetchall()
        response = jsonify(res)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/forgotpass', methods = ['GET'])
def checkQues():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        ques = json_['ques']
        ans = json_['ans']
        username = json_['username']
        rc = cursor.execute("select ques, ans from account where username = %s", username)
        if rc == 0:
            return jsonify("username is not exist")
        if ques == cursor._rows[0]['ques'] and ans == cursor._rows[0]['ans']:
            return jsonify("correct")
        else:
            return jsonify("not correct")
        
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
            
@app.route("/password", methods = ['GET'])
def getPass():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        username = json_['username']
        rc = cursor.execute("select pass from account where username = %s", username)
        if rc == 0:
            return jsonify("user is not exist")
        return jsonify(cursor._rows[0]['pass'])
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
    
@app.route("/password", methods = ['PUT'])
def updatePass():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        username = json_['username']
        newPass = json_['newPass']
        rc = cursor.execute("update account set pass = %s where username = %s",(newPass, username))
        if rc == 0:
            return jsonify("not successful")
        conn.commit()
        return jsonify("OK")
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
            
@app.route("/foodReviews", methods = ['POST'])
def reviewFood():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        foodid = json_['foodID']
        userid = json_['userID']
        cmt = json_['comment']
        star = json_['star']
        if star < 0 or star > 5:
            return jsonify("star is invalid")
        rc = cursor.execute("SELECT * from review WHERE FoodID = %s and UserID = %s", (foodid, userid))
        if rc != 0:
            rc = cursor.execute('update review set Star = %s, Comment = %s WHERE UserID = %s and FoodID = %s', (star, cmt, userid, foodid))
        else:
            cursor.execute("INSERT into review (FoodID, UserID, Comment, Star) values (%s, %s, %s,%s)", (foodid, userid, cmt, star))
        cursor.execute("select avg(star) from review where foodid= %s", foodid)
        avgStar = cursor.fetchone()
        avgStar = avgStar['avg(star)']
        cursor.execute("update food set avgStar = %s where id = %s", (avgStar, foodid))
        conn.commit()
        return jsonify("OK")
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/foodReviews')
def getReviews():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        foodid = json_['foodID']
        rc = cursor.execute("select * from review where foodID = %s", foodid)
        res = cursor.fetchall()
        return jsonify(res)
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/getListFood')
def getListFood():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        rc = cursor.execute("SELECT * FROM food order by rand() limit 40")
        res = cursor.fetchall()
        return jsonify(res)
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
    