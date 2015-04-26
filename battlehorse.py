from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

app = Flask(__name__)

@app.route('/')
def front_page():
    return render_template('front_page.html', dummy='')

if __name__ == '__main__':
    app.run(debug=True)
