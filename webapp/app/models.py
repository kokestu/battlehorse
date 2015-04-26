# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:07:56 2015

@author: Jonathan
"""

from app import db
from hashlib import md5

users_association_table = db.Table('users', db.Model.metadata,
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

sellers_association_table = db.Table('sellers', db.Model.metadata,
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('seller_id', db.Integer, db.ForeignKey('seller.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    books = db.relationship('Book',
                            secondary=users_association_table,
                            backref='users')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
               (md5(self.email.encode('utf8')).hexdigest(), size)
    
    def __repr__(self):
        return '<User %r>' % (self.nickname)
        
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname
        
class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    books = db.relationship('Book',
                            secondary=sellers_association_table,
                            backref='sellers')
    about_us = db.Column(db.String(140))
    
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
               (md5(self.email.encode('utf8')).hexdigest(), size)
    
    def __repr__(self):
        return '<Seller %r>' % (self.name)
        
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.Integer)
    title = db.Column(db.String(140))
    author = db.Column(db.String(64))

    def __repr__(self):
        return '<Book %r>' % (self.title)
        