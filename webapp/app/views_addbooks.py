__author__ = 'blain_000'

from flask import render_template, flash, redirect, \
                  session, url_for, request, g
from flask.ext.login import login_user, logout_user, \
                            current_user, login_required
from app import app, db, lm, oid
from .forms import *
from .models import User, Seller, Book

@app.route('/addbooks/isbn', methods=['GET', 'POST'])
@login_required
def add_books_by_isbn():
    form = AddBookByISBNForm()
    if form.validate_on_submit():
        isbn_int = int(re.sub('^[0-9]', '', form.isbn.data))
        book = Book.query.filter_by(isbn=isbn_int).first()
        if book is not None:
            g.user.books.append(book)
        else:
            book = Book(isbn=isbn_int)
            db.session.add(book)
            g.user.books.append(book)
        db.session.commit()
        flash("Added book with ISBN {} to your wishlist".format(isbn_int))
        return redirect(url_for('add_books_by_isbn'))
    return render_template('addbook.html', form=form)

@app.route('/addbooks/title', methods=['GET', 'POST'])
@login_required
def add_books_by_title():
    form = AddBookByTitleForm()
    if form.validate_on_submit():
        book = (Book.query.filter_by(author=form.author.data) if form.author.data != '' else Book.query)\
            .filter_by(title=form.title.data).first()
        if book is not None:
            g.user.books.append(book)
        else:
            book = Book(title=form.title.data, author=form.author.data)
            db.session.add(book)
            g.user.books.append(book)
        db.session.commit()
        flash("Added {} by {} to your wishlist".format(form.title.data, form.author.data))
        return redirect(url_for('add_books_by_isbn'))
    return render_template('addbook.html', form=form)

@app.route('/addbooks/', methods=['GET', 'POST'])
@login_required
def add_books():
    is_seller = False
    if 'is_seller' in session:
        is_seller = session['is_seller']
    if is_seller:
        form = AddBookForm()
        if form.validate_on_submit():
            isbn_int = int(re.sub('^[0-9]', '', form.isbn.data))
            books = []
            books += Book.query.filter_by(title=form.title.data)
            books += Book.query.filter_by(isbn=isbn_int)
            if books is not None:
                for b in books[:]:
                    if b.author and b.author != form.author.data\
                            or b.title and b.title != form.title.data\
                            or b.isbn and b.isbn != isbn_int:
                        books.remove(b)
                book = Book(isbn=isbn_int, title=form.title.data, author=form.author.data)
                db.session.add(book)
                for b in books:
                    for u in b.users:
                        if not u in book.users:
                            book.users.append(u)
                    db.session.delete(b)
                g.user.books.append(book)
                print(book.sellers)
            else:
                book = Book(isbn=isbn_int, title=form.title.data, author=form.author.data)
                db.session.add(book)
                g.user.books.append(book)
            db.session.commit()
            flash("You are now selling {} by {} (ISBN: {})".format(form.title.data, form.author.data, isbn_int))
            return redirect(url_for('add_books'))
        return render_template('addbook.html', form=form)
    else:
        return redirect(url_for('add_books_by_title'))