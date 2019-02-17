from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3


app = Flask(__name__)
app.secret_key = 'abcdef'

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        print(request.form['password'])
        username = request.form['username']
        session['username'] = username
        with sqlite3.connect('database.db') as conn:
            curs = conn.cursor()
            validation = curs.execute('SELECT * FROM LOGINDATA where name=?',(username,))
            validation_check = validation.fetchone()
            conn.commit()
            if validation_check is None:
                return render_template('login.html', username='Invalid username '+ str(username))
            elif validation_check[3] != request.form['password']:
                return render_template('login.html', username='Password is incorrect')
            else:
                return redirect(url_for('home_page'))

@app.route('/logout')
def logout():
    print(session['username'])
    session.pop('username',None)
    return redirect(url_for('home'))

@app.route('/home',methods = ['GET'])
def home_page():
    return render_template('home_page.html', username=session['username'])


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':

        try:
            with sqlite3.connect('database.db') as conn:
                curs = conn.cursor()
                curs.execute('CREATE TABLE IF NOT EXISTS LOGINDATA (name TEXT, username TEXT PRIMARY KEY, email TEXT,password TEXT)')
                conn.commit()
                curs.execute('INSERT INTO LOGINDATA (name, username, email, password) VALUES(?,?,?,?)',(request.form['name'],request.form['username'],request.form['email'],request.form['password']))
                conn.commit()

        except sqlite3.IntegrityError as error:
            return render_template('signup.html', error='Username already exists!')
        result = request.form
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug = True, port=5001)
