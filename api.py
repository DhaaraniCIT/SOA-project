from __future__ import print_function
import flask
import sys
from flask import Flask,request,render_template,jsonify,json
from flask_cors import CORS
from heapq import heappush, heappop, heapify
from collections import defaultdict
import base64 
import MySQLdb
import json
import math, random
from captcha.image import ImageCaptcha
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
hostname = 'localhost'
username = 'root'
password = ''
database = 'greenhorn'
values = ('id','title','description','schoolName','campaignEndDate','campaignStartDate','campaignStatusId','goalAmount','amountRaised','UserId','SportId','createdAt','coverPicture','campaignDuration')
@app.route('/campaigns',methods=['GET'])
def fast():
    userId=request.args.get('id')
    print( "Using mysqlclient (MySQLdb):" )
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    cur.execute( "SELECT * FROM campaigns  WHERE UserId="+str(userId) )
    result = cur.fetchall()
    cur = conn.cursor()
    sql2 = "SELECT firstName,lastName,profilePic FROM user"
    cur.execute( sql2 )
    result2 = cur.fetchall()
    conn.close()
    lenght = len(result)
    print("length",lenght)
    arr=[]
    dic = {}
    users = {}
    keys=('firstName','lastName','profilePictureURL')
    print("forww")
    for x in range(lenght):
        users = dict(zip(keys,result2[result[x][9]-1]))
        dic=dict(zip(values,result[x]))
        dic['user']=users
        arr.append(dic)
    return jsonify(arr)

@app.route('/campaign',methods=['GET'])
def camp():
    value = request.args.get('id')
    print( "Using mysqlclient (MySQLdb):",value )
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "SELECT * FROM campaigns where id="+value
    cur.execute( sql )
    result = cur.fetchall()
    sql2 = "SELECT firstName,lastName,profilePic FROM user"
    cur.execute( sql2 )
    result2 = cur.fetchall()
    conn.close()
    
    lenght = len(result)
    print("length",lenght)
    arr=[]
    dic = {}
    users = {}
    keys=('firstName','lastName','profilePictureURL')
    print("forww")
    for x in range(lenght):
        users = dict(zip(keys,result2[result[x][9]-1]))
        dic=dict(zip(values,result[x]))
        dic['user']=users
        arr.append(dic)
    return jsonify(arr)

@app.route('/campaign/create',methods=['POST'])
def creatcamp():
    content = request.form
    # value = int(value)
    print( "Using mysqlclient (MySQLdb):")
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "INSERT INTO campaigns (id,title,description,schoolName,campaignEndDate,campaignStateDate,campaignStatusId,goalAmount,amountRaised,UserId,SportId,createdAt,coverPicture,campaignDuration) VALUES (6,'" + content['title'] + "','" + content['description'] + "','" + content['schoolName'] + "','" + content['campaignEndDate'] + "','" + content['campaignStartDate'] + "'," + str(1) + "," + str(content['goalAmount']) + "," + str(0) + "," + str(content['userId']) + "," + str(content['sportId']) + ",'" + content['createdAt'] + "','" + content['coverPicture'] + "'," + str(content['campaignDuration']) + ")"
    cur.execute( sql )
    conn.commit()
    conn.close()
    return jsonify({"data":"added"})

@app.route('/campaign/active',methods=['GET'])
def actcamp():
    print( "Using mysqlclient (MySQLdb):" )
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "SELECT * FROM campaigns where campaignStatusId=2"
    cur.execute( sql )
    result = cur.fetchall()
    sql2 = "SELECT firstName,lastName,profilePic FROM user"
    cur.execute( sql2 )
    result2 = cur.fetchall()
    conn.close()
    lenght = len(result)
    print("length",lenght)
    arr=[]
    dic = {}
    users = {}
    keys=('firstName','lastName','profilePictureURL')
    for x in range(lenght):
        users = dict(zip(keys,result2[result[x][9]-1]))
        dic=dict(zip(values,result[x]))
        dic['user']=users
        arr.append(dic)
    return jsonify({"data":arr})


@app.route('/campaign/updateCampaignStatus',methods=['PUT'])
def updatecampstatusId():
    content = request.get_json()
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "UPDATE campaigns SET campaignStatusId=2 ,campaignEndDate='"+content['campaignEndDate']+"',campaignStateDate='"+content['campaignStartDate']+"' WHERE id='" + str(content['campaignId']) + "' AND UserId ='" + str(content['userId']) +"'"
    print(sql)
    cur.execute( sql )
    conn.commit()
    conn.close()
    return jsonify({"data":"added"})

@app.route('/campaign/updateCampaign',methods=['PUT'])
def updatecamp():
    content = request.get_json()
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "UPDATE campaigns SET title='"+content['title']+"',description='"+ content['description'] +"',schoolName='"+content['schoolName']+"',goalAmount="+str(content['goalAmount'])+",sportId="+str(content['sportId'])+",coverPicture='"+content['coverPicture']+"', campaignStateDate='"+content['campaignStartDate']+"',campaignendDate='"+content['campaignEndDate']+"',campaignDuration="+str(content['campaignDuration'])+" WHERE id='" + str(content['campaignId']) + "'"
    print(sql)
    cur.execute( sql )
    conn.commit()
    conn.close()
    return jsonify({"data":"added"})


@app.route('/login', methods =['POST'])
def login():
    content = request.get_json()
    print(request.get_json())
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = 'SELECT * FROM user WHERE email= "'+content['email']+'" AND password = "'+content['password']+'"'        
    cur.execute(sql)
    account = cur.fetchone()
    conn.close()
    print(account)
    if account:
        keys=('UserId','firstName','lastName','email','dateOfBirth','profilePictureURL','phoneNumber','token')
        account=list(account)
        account.pop(4)
        account=tuple(account)
        users={}
        user = dict(zip(keys,account))
        return jsonify({"data":user})
    else:
        return jsonify("error")
@app.route('/profile', methods =['GET'])
def profile():
    content = request.args.get('id')
    content1 = request.args.get('token')
    print(content)
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "SELECT * FROM user WHERE id="+content     
    print(sql)
    cur.execute(sql)
    account = cur.fetchone()
    conn.close()
    if account:
        keys=('UserId','firstName','lastName','email','dateOfBirth','phoneNumber','profilePictureURL')
        account=list(account)
        account.pop(4)
        account=tuple(account)
        users={}
        user = dict(zip(keys,account))
        return jsonify({"data":user})
@app.route('/profile/update', methods =['PUT'])
def profileup():
    content = request.form
    print(content)
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "UPDATE user SET firstName='"+content['firstName']+"',lastName='"+ content['lastName'] +"',phone='"+content['phoneNumber']+"',profilePic='"+content['profilePicture']+"', DOB='"+content['dateOfBirth']+"' WHERE id='" + str(content['id']) + "'"        
    print(sql)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return jsonify({"data":"updated"})

@app.route('/captcha', methods =['GET'])
def captcha():
    n1=6
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
    cap = "" 
    for i in range(n1) : 
        cap += digits[math.floor(random.random() * len(digits))]

    image = ImageCaptcha(width = 280, height = 90)
    data = image.generate(cap)
    image.write(cap, 'captcha.png')
    with open("captcha.png", "rb") as img_file:
        ing = base64.b64encode(img_file.read()).decode('utf-8')
    print(ing)
    return jsonify({"data":cap,"img":ing})
@app.route('/user/create', methods =['POST'])
def signup():
    content = request.get_json()
    print(request.get_json(),content['email'])
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = 'SELECT * FROM user WHERE email= "'+content['email']+'"'        
    cur.execute(sql)
    account = cur.fetchone()
    print(account)
    if account:
        return jsonify({"error":"User Already Exist"})
    else:
        if content['recaptcha']==content['capcha']:
            n1=100
            digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
            OTP = "" 
            for i in range(n1) : 
                OTP += digits[math.floor(random.random() * len(digits))] 
            sql = "INSERT INTO user (firstName, lastName, email, password,DOB,token) VALUES ('" + content['firstName'] + "','" + content['lastName'] + "','" + content['email'] + "','" + content['password'] + "','" + content['dateOfBirth'] +"','"+OTP+"')"
            print(sql)
            cur.execute(sql)
            conn.commit()
            return jsonify({"data":"Registeration Successfull"})
        else:
            return jsonify({"error":"CAPTCHA is incorrect"})
@app.route('/newpass', methods =['POST'])
def password():
    content = request.get_json()
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = 'SELECT * FROM user WHERE email= "'+content['email']+'"'        
    cur.execute(sql)
    account = cur.fetchone()
    print(account)
    if account:
        sql = "UPDATE user SET password='"+content['newPassword']+"' WHERE email='" + content['email'] + "'"        
        print(sql)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return jsonify({"data":"updated"})
    else:
        return jsonify({"error":"something went wrong"})

@app.route('/create-custombank-account', methods =['POST'])
def bank():
    content = request.get_json()
    print(request.get_json(),content['accNo'])
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "INSERT INTO bankdetails (userId, accno, HolderName, amount) VALUES (" + str(content['userId']) + "," + str(content['accNo']) + ",'" + content['accName'] + "'," + str(content['amount']) +")"
    print(sql)
    cur.execute(sql)
    conn.commit()
    return jsonify({"data":"Registeration Successfull"})

@app.route('/bank', methods =['POST'])
def bankdetails():
    content = request.get_json()
    print(content)
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "SELECT * FROM bankdetails WHERE userId="+str(content['id'])        
    cur.execute(sql)
    account = cur.fetchone()
    conn.close()
    print(account)
    if account:
        keys=('Id','userId','accNo','amount','accName')
        users={}
        user = dict(zip(keys,account))
    return jsonify({"data":user})

@app.route('/createWithdrawalAndPayout', methods =['POST'])
def addbankdetails():
    content = request.get_json()
    print(content)
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "INSERT INTO withdraw (UserId,campaignId,amount, transactionDate) VALUES (" +str(content['userId'])+","+ str(content['campaignId']) + "," + str(content['amount']) + ",'" + content['transactionDate'] + "')"
    print(sql)
    cur.execute(sql)
    conn.commit()
    sql2 = "SELECT SUM(amount) FROM withdraw WHERE UserId="+str(content['userId'])
    cur.execute(sql2)
    result = cur.fetchall()
    print("sum",result[0][0])
    sql3 = "UPDATE bankdetails SET amount='"+str(result[0][0])+"' WHERE userId='"+str(content['userId'])+"'"
    print(sql3)
    cur.execute(sql3)
    conn.commit()
    return jsonify({"data":"Transfer Successfull"})

@app.route('/addCampaignPost', methods =['POST'])
def campPost():
    content = request.form
    conn =MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "INSERT INTO updates (campaignId, title, description, youtubelink, picture) VALUES (" + str(content['campaignId']) + ",'" + content['title'] + "','" + content['text'] + "','" + content['videoURL'] + "','" + content['Picture'] + "')"
    cur.execute(sql)
    conn.commit()
    return jsonify({"data":"Registeration Successfull"})

@app.route('/getCampaignPostsByCampaign', methods =['GET'])
def getcampPost():
    content = request.args.get('id')
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = 'SELECT * FROM updates WHERE campaignId='+str(content)
    cur.execute(sql)
    account = cur.fetchall()
    arr=[]
    if account:
        keys=('Id','campaignId','title','text','videoURL','picture','createdAt')
        users={}
        
        lenght = len(account)
        for x in range(lenght):
            user = dict(zip(keys,account[x]))
            arr.append(user)
        return jsonify({"data":arr})
    else:
        return jsonify({"data":arr})

@app.route('/createContributor', methods =['POST'])
def campcon():
    content = request.get_json()
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "INSERT INTO contribution (campaignId, amount, firstName, lastName, email, contributionDate) VALUES (" + str(content['campaignId']) + "," + str(content['amount']) + ",'" + content['firstName'] + "','" + content['lastName'] + "','" + content['email'] + "','"+content['contributedAt']+"')"
    cur.execute(sql)
    conn.commit()
    sql = "SELECT amount FROM bankdetails WHERE userId = 0 "
    cur.execute(sql)
    amountt = cur.fetchall()
    amountt = amountt[0][0]+float(content['amountwithcharges'])
    sql = "UPDATE bankdetails set amount='"+str(amountt)+"' WHERE userId='0'"
    cur.execute(sql)
    conn.commit()
    sql2 = 'SELECT campaignId,amount from contribution WHERE campaignId='+str(content['campaignId'])
    cur.execute(sql2)
    result = cur.fetchall()
    length = len(result)
    goal=0
    for x in range(length):
        goal+=result[x][1]
    sql = "UPDATE campaigns SET amountRaised='"+str(goal)+"' WHERE id='"+str(content['campaignId'])+"'"
    cur.execute(sql)
    conn.commit()
    conn.close()
    return jsonify({"data":"Registeration Successfull"})

@app.route('/withdrawal/campaign/<int:cid>', methods =['GET'])
def withlist(cid):
    conn =MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "SELECT amount,transactionDate FROM withdraw WHERE campaignId="+str(cid)
    cur.execute(sql)
    result = cur.fetchall()
    length = len(result)
    keys=('amount','transactionDate')
    dic={}
    arr=[]
    total=0
    for x in range(length):
        total+=result[x][0]
        dic=dict(zip(keys,result[x]))
        arr.append(dic)
    conn.close()
    return jsonify({"data":arr,"withdraw":total})

@app.route('/contribution/campaign/<int:cid>', methods =['GET'])
def conlist(cid):
    conn = MySQLdb.connect("localhost","root","","greenhorn")
    cur = conn.cursor()
    sql = "SELECT firstName,lastName,email,amount,contributionDate FROM contribution WHERE campaignId="+str(cid)
    cur.execute(sql)
    result = cur.fetchall()
    length = len(result)
    keys=('firstName','lastName','email','amount','contributionDate')
    dic={}
    arr=[]
    total=0
    for x in range(length):
        total+=result[x][3]
        dic=dict(zip(keys,result[x]))
        arr.append(dic)
    conn.close()
    return jsonify({"data":arr,"contribution":total})
if __name__=='__main__':
	 app.run(debug=True) 