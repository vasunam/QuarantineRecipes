from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from flask import g

app = Flask(__name__)

DATABASE = 'easyRecipe.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    db_connection = get_db()
    cur = db_connection.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    db_connection = get_db()
    cur = db_connection.cursor()
    cur.execute(query, args)
    db_connection.commit()

def is_valid_login(username, password):
    valid_password = query_db("select password from users where username = ?", [username], one=True)
    if valid_password is None:
        return "Not a valid user", False
    if password==valid_password[0]:
        
        return "Valid user", True
    else:
        print(password, valid_password,type(valid_password), "!")
        return "Wrong password! ", False

def create_new_user(username, password):
    new_username = query_db("select username from users where username=?",[username], one=True)
    if new_username:
        return "User already exists!",False
    else:
        new_username = insert_db("insert into users (username, password) values (?, ?)",[username,password])
        return "User created", True
    

        

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    status = False
    if request.method == 'POST':
        status, is_valid = is_valid_login(request.form['username'], request.form['password'])
    return render_template('login.html', error=status)

# Route for handling creation of new user
@app.route('/createuser', methods=['GET', 'POST'])
def create_user():
    error = None
    status = False
    if request.method == 'POST':
        status, is_created = create_new_user(request.form['username'], request.form['password'])
        if is_created:
            return redirect('/login')
        else:
            return render_template('create_user.html', error=status)
    else:
        return render_template('create_user.html')


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
