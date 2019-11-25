from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import os
from datetime import datetime
import random
import MySQLdb
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'UserSession'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'municipality'

mysql = MySQL(app)
pincode=0
flag=0

def checkUserPwdtype(email,password,accounttype):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * from User where Email=%s and Password=%s and Accounttype=%s',(email,password,accounttype))
    userpwd=cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if(len(userpwd)==0):
    	return 1
    return 0


def checkusertype(type):
	cur = mysql.connection.cursor()
	if type == "Administrator":
		flag = 1
	else:
		flag =0

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        details = request.form
        Accounttype = details['accounttype']
        Name = details['name']
        Surname = details['surname']
        MemberCount = details['members']
        Email = details['email']
        Password = details['password']
        Address = details['address']
        Phone = details['phone']
        Pincode = details['pincode']
        # RollNo = details['rollno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT max(RollNo) from User")
        data=cur.fetchall()
        # print(data[0])
        if(data[0][0] == None):
        	# print("Here")
        	RollNo = 100
        else:
        	RollNo = int(data[0][0])+1
        # print(RollNo)
        error = 'Please fill all fields'
        if (Accounttype == None or Name == None or Surname == None or MemberCount == None or Email == None or Password == None or Address == None or Phone == None or Pincode == None):
        	return render_template('signup.html',error=error)
        else:
        	cur.execute("INSERT INTO User(RollNo, Accounttype, Name, Surname, MemberCount, Email, Password, Address, Phone, Pincode) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)", (RollNo, Accounttype, Name, Surname, MemberCount, Email, Password, Address, Phone, Pincode))
        	mysql.connection.commit()
        	cur.close()
        	return redirect(url_for('login'))
    return render_template('signup.html')




@app.route('/login',methods=['GET','POST'])
def login():
	# global pincode
    if request.method == "POST":
        details = request.form
        cur = mysql.connection.cursor()
        # session['email'] = details['email']
        cur.execute("SELECT RollNo from User where Email = %s and Password = %s and Accounttype = %s",(details['email'], details['password'], details['accounttype']))
        data = cur.fetchall()
        # print(data)
        
        # print(session['RollNo'])
        # checkusertype(details['accounttype'])
        error = 'Invalid Credentials'
        if checkUserPwdtype(details['email'], details['password'], details['accounttype']):
            return render_template('login.html',error=error)
        else:
        	session['RollNo'] = data[0][0]
        	return redirect(url_for('profile'))
    return render_template('login.html')



@app.route('/profile', methods=['GET','POST'])
def profile():	
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT Name, Surname, Address, Phone, Email, MemberCount, Accounttype from User where RollNo = %s", (session['RollNo'],))
        data=cur.fetchall()
        mysql.connection.commit()
        cur.execute("SELECT * from User where Accounttype='Administrator'")
        test=cur.fetchall()
        mysql.connection.commit()
        if(len(test) == 0):
        	return render_template('profile.html', data=data)
        else:
        	cur.execute("SELECT Name, Surname from User where Accounttype = 'Administrator' and Pincode IN (SELECT Pincode from User where RollNo = %s)",[session['RollNo']])
        	admin=cur.fetchall()
        	mysql.connection.commit()
        	return render_template('profile.html', data=data, admin=admin)
    cur.close()
        


@app.route('/createrequestbutton', methods=['GET','POST'])
def createrequestbutton():
	cur = mysql.connection.cursor()
	cur.execute("SELECT Name, Surname from User where RollNo = %s",[session['RollNo']])
	nam = cur.fetchall()
	mysql.connection.commit()
	cur.close()
	return render_template('createrequest.html', surname=nam)	


@app.route('/createrequest', methods=['GET','POST'])
def createrequest():
	# nam = ""
	# print(request.method)
	# request.method = "POST"
	if request.method == "POST":
		# print("Hello")
		details = request.form
		# print(details[0])
		Type = details['requesttype']
		Description = details['desc']
		Document = request.files['document']
		Project = request.files['project']
		sta = ['Pending', 'Solved', 'Initiated']
		Status = random.choice(sta)
		Time =  datetime.now()
		# Datetime = Time.strftime("YYYY-MM-DD HH:MM:SS")
		cur = mysql.connection.cursor()
		cur.execute("SELECT max(RequestID) from Request")
		data=cur.fetchall()
		if(data[0][0] == None):
			RequestID = 200
		else:
			RequestID = int(data[0][0])+1
		cur.execute("INSERT INTO Request(RequestID, RollNo, Type, Description, Document, Project, Status, TimeDate) VALUES (%s, %s, %s,%s, %s, %s, %s, %s)", (RequestID, session['RollNo'], Type, Description, Document, Project, Status, Time))
		# cur.execute("SELECT Name, Surname from User where RollNo = %s",(session['RollNo']))
			# print("Hello!!!!", session['RollNo'])
		# nam = cur.fetchall()
		# mysql.connection.commit()
		mysql.connection.commit()
		cur.close()

		return redirect(url_for('showrequests'))
			# print(nam)
	return render_template('createrequest.html')	


@app.route('/showrequests', methods=['GET','POST'])
def showrequests():
	if request.method == "GET":
		print("Hello")
		cur = mysql.connection.cursor()
		cur.execute("SELECT RequestID, Type, Description, SUBSTR(Document,14,29),Status, TimeDate from Request where RollNo = %s", [session['RollNo']])
		data = cur.fetchall()
		# print(data)
		mysql.connection.commit()
		cur.execute("SELECT Name, Surname from User where RollNo = %s",[session['RollNo']])
		nam = cur.fetchall()
		mysql.connection.commit()
		cur.close()
	return render_template('showrequests.html', data=data, surname=nam)

@app.route('/createcomplaintbutton', methods=['GET','POST'])
def createcomplaintbutton():
	cur = mysql.connection.cursor()
	cur.execute("SELECT Name, Surname from User where RollNo = %s",[session['RollNo']])
	nam = cur.fetchall()
	mysql.connection.commit()
	cur.close()
	return render_template('createcomplaint.html', surname=nam)	

@app.route('/createcomplaint', methods=['GET','POST'])
def createcomplaint():
	if request.method == "POST":
		details = request.form
		cur = mysql.connection.cursor()
		Time =  datetime.now()
		Subject = details['subject']
		Description = details['desc']
		# Datetime = Time.strftime("%d/%m/%Y %H:%M:%S")
		cur.execute("SELECT max(ComplainID) from Complaint")
		data=cur.fetchall()
		if(data[0][0] == None):
			ComplainID = 300
		else:
			ComplainID = int(data[0][0])+1
		cur.execute("INSERT INTO Complaint(ComplainID, RollNo, Subject, Description, TimeDate) VALUES (%s, %s, %s, %s, %s)", (ComplainID, session['RollNo'], Subject, Description, Time))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('showcomplaint'))
	return render_template('createcomplaint.html')


@app.route('/showcomplaint', methods=['GET','POST'])
def showcomplaint():
	if request.method == "GET":
		cur = mysql.connection. cursor()
		cur.execute("SELECT ComplainID, Subject, Description, TimeDate from Complaint where RollNo = %s", [session['RollNo']])
		data = cur.fetchall()
		mysql.connection.commit()
		cur.execute("SELECT Name, Surname from User where RollNo = %s",[session['RollNo']])
		nam = cur.fetchall()
		mysql.connection.commit()
		cur.close()
	return render_template('showcomplaint.html', data=data, surname=nam)

@app.route('/editprofilebutton', methods=['GET','POST'])
def editprofilebutton():
	cur = mysql.connection.cursor()
	cur.execute("SELECT Name, Surname from User where RollNo = %s",[session['RollNo']])
	nam = cur.fetchall()
	mysql.connection.commit()
	cur.execute("SELECT Address from User where RollNo = %s",[session['RollNo']])
	data = cur.fetchall()
	mysql.connection.commit()
	cur.close()
	return render_template('editprofile.html', surname=nam, data=data)	



@app.route('/editprofile', methods=['GET','POST'])
def editprofile():
	# print(request.method)
	if request.method == "POST":
		details =request.form
		cur = mysql.connection.cursor()
		Name = details['name']
		# cur.execute("SELECT RollNo from User where RollNo = %s", (session['RollNo']))
		# data = cur.fetchall()
		Surname = details['surname']
		MemberCount = details['members']
		Email = details['email']
		Password = details['password']
		Phone = details['phone']
		cur.execute("UPDATE User SET Name = %s, Surname = %s, MemberCount = %s, Email = %s, Password = %s, Phone = %s where RollNo = %s", (Name, Surname, MemberCount, Email, Password, Phone, session['RollNo'],))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('profile'))
	return render_template('editprofile.html')

@app.route('/adminprofile', methods=['GET','POST'])
def adminprofile():
	if request.method == "GET":
		cur = mysql.connection.cursor()
		cur.execute("SELECT Name, Surname from User where RollNo = %s",[session['RollNo']])
		nam = cur.fetchall()
		mysql.connection.commit()
		cur.execute("SELECT Name, Surname, Address, Phone, Email from User where Accounttype = 'Administrator' and Pincode = (SELECT Pincode from User where RollNo = %s)",[session['RollNo']])
		data = cur.fetchall()
		cur.close()
	return render_template('adminprofile.html', surname=nam, data=data)

@app.route('/paymentsbutton', methods=['GET','POST'])
def paymentsbutton():
	if request.method == "GET":
		cur = mysql.connection.cursor()
		cur.execute("SELECT Name, Surname from User where RollNo = %s",[session['RollNo']])
		nam = cur.fetchall()
		mysql.connection.commit()
		sta = ['Paid','Unpaid']
		Status = random.choice(sta)
		cur.close()
	return render_template('paymentsbutton.html', surname=nam, status=Status)


@app.route('/logout', methods=['GET','POST'])
def logout():
	session.pop('RollNo', None)
	return redirect(url_for('login'))


@app.route('/faq', methods=['GET','POST'])
def faq():
	cur = mysql.connection.cursor()
	cur.execute("SELECT Name, Surname from User where RollNo = %s",[session['RollNo']])
	nam = cur.fetchall()
	mysql.connection.commit()
	cur.close()
	return render_template('faq.html', surname=nam)

@app.route('/user', methods=['GET','POST'])
def user():
	cur=mysql.connection.cursor()
	cur.execute("SELECT Accounttype from User where RollNo = %s",[session['RollNo']])
	typ = cur.fetchall()
	cur.execute("SELECT Name, Surname from User where RollNo = %s",[session['RollNo']])
	nam = cur.fetchall()
	mysql.connection.commit()
	# print(typ)
	if(typ[0][0] == "Administrator"):
		cur.execute("SELECT Name, Surname, Email, Phone from User where Accounttype = 'Citizen' and Pincode = (SELECT Pincode from User where Accounttype = 'Administrator' and Rollno = %s)",[session['RollNo']])
		mysql.connection.commit()
		data = cur.fetchall()
		return render_template('viewcitizens.html', data=data, name = nam)
	else:
		return render_template('invalid.html', name = nam)
	cur.close()

if __name__ == '__main__':
    app.run(debug=True)