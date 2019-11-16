from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():

	# POST
    # if request.method == "POST":
        # details = request.form
        # firstName = details['fname']
        # lastName = details['lname']
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        # mysql.connection.commit()
        # cur.close()
        # return 'success'
    # return render_template('index.html')


    # GET
    if request.method == "GET":
    	 cur = mysql.connection.cursor()
    	 cur.execute("SELECT * from MyUsers")
    	 data=cur.fetchall()
    	 mysql.connection.commit()
    	 cur.close()
    return render_template('index.html',name=data)

if __name__ == '__main__':
    app.run(debug=True)