"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import jsonify
from flask import request
from FlaskWebProject import app
import utils
now = datetime(2016, 2, 27, 3, 7, 17, 966565)


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

    print order, sym, val
    if order == 'B':
        utils.buy(sym, val)

    elif order == 'S':
        utils.sell(sym, val)
    return "ordered"


@app.route('/status')
def status():
    value = utils.get_portfolio_val()
    portfolio = utils.portfolio
    return jsonify(value=value, portfolio=portfolio)
