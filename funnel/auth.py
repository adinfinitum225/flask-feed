
m flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
        )
from werkzeug.security import check_password_hash, generate_password_hash

from funnel.db import get_db, close_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user = session.get['user']

    if user is None:
        g.user = None
    else:
        g.user = get_db().cursor().execute(
                'SELECT username, password FROM users WHERE username = %s', (username)).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        error = None

        if not username:
            error = 'You need a username to register'
        elif not password:
            error = 'Your password needs to be longer than 0 characters'
        elif password.len() < 5:
            error = 'Your password needs to be longer than 4 characters'
        elif cur.execute('SELECT username FROM users WHERE username = %s', (username)).fetchone() is not None:
            error = 'This username is already taken'

        if error is None:
            db.execute(
                    'INSERT INTO users (username, password) VALUES (%s, %s)' (username, generate_password_hash(password))
                    )
            cur.commit()
            return(redirect(url_for('auth.login')))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        user = cur.execute('SELECT username, password FROM users WHERE username = %S', (username)).fetchone()

        if user is None:
            error = 'Make sure you type your username in right'
        elif not check_password_hash(user['password'], password):
            error = 'Password doesn\'t match username'

        if error is None:
            session.clear()
            session['user'] = user['username']
            return redirect(url_for('index'))
    
        flash(error)

    return render_template('auth/login.html')
        
@bp.route('/logout')
def logout():
    pass
