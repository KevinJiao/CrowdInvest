"""
Routes and views for the flask application.
"""
import sqlite3
from datetime import datetime
from flask import render_template
from flask import jsonify
from flask import request
from flask import g
from FlaskWebProject import app
import utils
now = datetime(2016, 2, 27, 3, 7, 17, 966565)


@app.before_request
def before_request():
    g.db = sqlite3.connect("portfolio.db")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/query.html')
def emails():
    symbols = g.db.execute("SELECT sym, amount FROM portfolio").fetchall()
    print symbols
    return str(symbols)


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/history')
def history():
    """Returns a JSON object containing the history"""
    history = [100, 150, 170, 200]
    return jsonify(history=history)


@app.route('/quote')
def quote():
    sym = request.args.get('s')
    return jsonify(price=utils.get_quote(sym))


@app.route('/order', methods=['POST'])
def buy():
    order = request.form['order']
    sym = request.form['sym']
    val = request.form['val']

    r = utils.order(order, sym, val, g)
    return str(r)


@app.route('/status')
def status():
    value = utils.get_portfolio_val(g)
    portfolio = utils.get_portfolio(g)
    history = utils.history
    trades = utils.get_trades(g)
    return jsonify(value=value, portfolio=portfolio, history=history, trades=trades)


@app.route('/twilio', methods=['POST', 'GET'])
def twilio():
    body = request.form['Body'].split(' ')
    if len(body) != 3:
        return
    order, sym, value = body
    utils.order(order, sym, value)
    return "we gucci"
