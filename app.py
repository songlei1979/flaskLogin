import re

from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
# secret key
app.secret_key = 'cairocoders-ednalar'

mysql = MySQL()
# MySQL connections
app.config['MYSQL_DATABASE_USER'] = 'qhejlr2ge5b5y76z'
app.config['MYSQL_DATABASE_PASSWORD'] = 'b4ehiy66g97fcq2a'
app.config['MYSQL_DATABASE_DB'] = 'cg3p5uut4q9j771z'
app.config['MYSQL_DATABASE_HOST'] = 'bmlx3df4ma7r1yh4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
mysql.init_app(app)


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute("Select * from account Where username = %s and password = %s", (username, password))
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['admin'] = account['admin']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

# create user
@app.route('/createuser', methods=['GET', 'POST'])
def createuser():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'fullname' in request.form:
        fullname = request.form["fullname"]
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute("select * from account where username=%s", (username))
        account = cursor.fetchone()
        if account:
            msg = "Account already exists"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "Invalid email address!"
        elif not username or not password or not fullname:
            msg = 'Please fill out the form'
        else:
            cursor.execute("insert into account values (null, %s, %s, %s, 0)", (fullname, username, password))
            conn.commit()

            msg = "You have successfully created an account"
    return render_template('createuser.html', msg=msg)

# home page
@app.route('/')
def home():
    # check if user is loggedin
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'], admin=session['admin'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:
        cursor.execute('Select * from account where id=%s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
