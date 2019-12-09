import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
        )
from werkzeug.security import check_password_hash, generate_password_hash

from funnel.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user = session.get('user')

    if user is None:
        g.user = None
    else:
        cur = get_db().cursor()
        cur.execute(
                'SELECT username FROM users WHERE username = %s', (user,)
                )
        g.user = cur.fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT username FROM users WHERE username = %s', (username,))
        error = None

        if not username:
            error = 'You need a username to register'
        elif not password:
            error = 'Your password needs to be longer than 0 characters'
        elif len(password) < 5:
            error = 'Your password needs to be longer than 4 characters'
        elif cur.fetchone() is not None:
            error = 'This username is already taken'

        if error is None:
            cur.execute(
                    'INSERT INTO users (username, password) VALUES (%s, %s)', (username, generate_password_hash(password))
                    )
            db.commit()
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
        cur.execute('SELECT username, password FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        error = None

        if user is None:
            error = 'Make sure you type your username in right'
        elif not check_password_hash(user[1], password):
            error = 'Password doesn\'t match username'

        if error is None:
            session.clear()
            session['user'] = user[0]
            return redirect(url_for('index'))
    
        flash(error)

    return render_template('auth/login.html')
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

