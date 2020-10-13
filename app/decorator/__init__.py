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
            return redirect(url_for('dashboard'))
        return fn(*args, **kwargs)
    return wrapper


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('email'):
                return redirect(url_for('login'))
            user = User.find_by_email(session['email']) 
            if not user.allowed(access_level):
                flash(f'Forbidden you have no permision to this page!', 'warning')
                return redirect(url_for('patient')) 
            return f(*args, **kwargs)      
        return decorated_function
    return decorator    
