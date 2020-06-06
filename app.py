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
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def is_valid_login(username, password):
    valid_password = query_db("select password from users where username = ?", [username], one=True)
    if valid_password is None:
        return "Not a valid user", False
    if password==valid_password[0]:
        
        return "Valid user", True
    else:
        print(password, valid_password,type(valid_password), "!")
        return "Wrong password! ", False
        

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        status, is_valid = is_valid_login(request.form['username'], request.form['password'])
    return render_template('login.html', error=status)
