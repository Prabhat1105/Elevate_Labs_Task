
from flask import Flask, request, render_template, g, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from config import DB_CONFIG

app = Flask(__name__)

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        try:
            db = g._db = mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("DB Error: Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("DB Error: Database does not exist")
            else:
                print("DB Error:", err)
            db = None
    return db

@app.teardown_appcontext

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        try:

            if db.is_connected():
                db.close()
        except mysql.connector.errors.InternalError as e:
        
            if 'Unread result found' in str(e):
                db.close()
            else:
                raise e # Re-raise other internal errors
        except Exception:
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home/<int:user_id>')
def home(user_id):
    return render_template('home.html', user_id=user_id)


@app.route('/products')
def products():
    q = request.args.get('q','')
    db = get_db()
    

    sql = "SELECT id, name, description, price FROM products WHERE name LIKE '%%{}%%'".format(q)
    rows = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
        except mysql.connector.Error as err:
            # Displaying an error like this is also bad practice (Information Disclosure)
            return render_template('products.html', query=q, rows=[], sql=sql, error=str(err))

    return render_template('products.html', query=q, rows=rows, sql=sql)


@app.route('/login', methods=['GET','POST'])

@app.route('/login', methods=['GET','POST'])

@app.route('/login', methods=['GET','POST'])

@app.route('/login', methods=['GET','POST'])

@app.route('/login', methods=['GET','POST'])
def login():
    message = ''
    if request.method == 'POST':
        user = request.form.get('username','')
        pwd = request.form.get('password','')
        db = get_db()

        sql = "SELECT id FROM users WHERE username='{}' AND password='{}'".format(user, pwd)
        
        if db:
            try:
                with db.cursor() as cur:
                    cur.execute(sql)
                    row = cur.fetchone()
                    
                    while cur.nextset():
                        pass
                
                    if row:
                        db.commit() 
                        return redirect(url_for('home', user_id=row[0])) 
                    else:
                        message = "Login failed."
            except mysql.connector.Error as err:
                 message = "Database Error: " + str(err)
    
    return render_template('login.html', message=message)
@app.route('/secure_products')
def secure_products():
    q = request.args.get('q','')
    db = get_db()
    
    sql = "SELECT id, name, description, price FROM products WHERE name LIKE %s"
    
    rows = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(sql, ('%'+q+'%',)) 
            rows = cur.fetchall()
            cur.close()
        except mysql.connector.Error as err:
            return render_template('products.html', query=q, rows=[], sql=sql, error=str(err))

    return render_template('products.html', query=q, rows=rows, sql=sql)


@app.route('/secure_login', methods=['GET','POST'])
def secure_login():
    message = ''
    if request.method == 'POST':
        user = request.form.get('username','')
        pwd = request.form.get('password','')
        db = get_db()

        sql = "SELECT id FROM users WHERE username=%s AND password=%s"
        
        if db:
            try:
                cur = db.cursor()
                cur.execute(sql, (user, pwd)) # Pass user input as a safe tuple
                row = cur.fetchone()
                cur.close()
                if row:
                    return redirect(url_for('home', user_id=row[0])) 
                else:
                    message = "Login failed."
            except mysql.connector.Error as err:
                 message = "Database Error: " + str(err)
    
    return render_template('login.html', message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)