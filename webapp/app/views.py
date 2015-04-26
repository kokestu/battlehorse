# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:00:46 2015

@author: Jonathan
"""

from flask import render_template, flash, redirect, \
                  session, url_for, request, g
from flask.ext.login import login_user, logout_user, \
                            current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, EditForm
from .models import User, Seller

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template('index.html',
                           title='Home',
                           user=user)
                           
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        session['is_seller'] = form.is_seller.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
                           
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s is not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)
                           
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)
                           
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        is_seller = False
        if 'is_seller' in session:
            is_seller = session['is_seller']
            session.pop('is_seller', None)
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        if is_seller:
            new = Seller(name=nickname, email=resp.email)
        else:
            new = User(nickname=nickname, email=resp.email)
        db.session.add(new)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
    
@app.before_request
def before_request():
    g.user = current_user