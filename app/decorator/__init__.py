from functools import wraps
from flask import redirect, url_for, flash, session



def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        correct_id = kwargs.get('id')
        if correct_id != session.get('user_id'):
            flash(f'Not Authorized', 'warning')
            return redirect(url_for('patient'))
        return fn(*args, **kwargs)    
    return wrapper

def prevent_login_signup(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            flash(f'You are logged in already', 'warning')
            return redirect(url_for('patient'))
        return fn(*args, **kwargs)    
    return wrapper

def requires_access_level(access_level):
    @wraps(fn)
    def wrapper(*args, **kwargs)
    if not session.get('email'):
        return redirect(url_for('users.login'))
        
    user = User.find_by_email(session['email'])
    elif not user.allowed(access_level):
        flash(f'You have no access to this page', 'warning')
        return redirect(url_for('index')
      return fn(*args, **kwargs)
    return wrapper
