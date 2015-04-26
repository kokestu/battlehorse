# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 18:15:53 2015

@author: Jonathan
"""

import re
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from app.models import User

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    is_seller = BooleanField('is_seller', default=False)

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True


class AddBookByISBNForm(Form):
    isbn = StringField('isbn', validators=[DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False
        numbersonly = re.sub('[^0-9]', '', self.isbn.data)
        if len(numbersonly) != 10 and len(numbersonly) != 13:
            return False
        return True

class AddBookByTitleForm(Form):
    title = StringField('title', validators=[DataRequired(), Length(min=0, max=140)])
    author = StringField('author', validators=[Length(min=0, max=64)])

class AddBookForm(Form):
    isbn = StringField('isbn', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired(), Length(min=1, max=140)])
    author = StringField('author', validators=[DataRequired(), Length(min=1, max=64)])

    def validate(self):
        if not Form.validate(self):
            return False
        numbersonly = re.sub('[^0-9]', '', self.isbn.data)
        if len(numbersonly) != 10 and len(numbersonly) != 13:
            return False
        return True