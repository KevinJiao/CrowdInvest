"""
Routes and views for the flask application.
"""
import sqlite3
from datetime import datetime
from flask import render_template
from flask import jsonify
from flask import request
from flask import make_response
from flask import g
import traceback
import twilio.twiml
from FlaskWebProject import app
import utils
import requests
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
    return jsonify(sym=sym, price=utils.get_quote(sym))


@app.route('/order', methods=['POST'])
def buy():
    order = request.form['order']
    sym = request.form['sym']
    val = request.form['val']
    if utils.valid_order(order, sym, val):
        r = utils.order(order, sym, val, g)
        return str(r)
    return "not valid"


@app.route('/status')
def status():
    value = utils.get_portfolio_val(g)
    portfolio = utils.get_portfolio(g)
    history = utils.get_history(g)
    trades = utils.get_trades(g)
    top = utils.get_top(g)
    cash = g.db.execute("SELECT sym, amount FROM portfolio WHERE sym = ?", ["funds"]).fetchall()[0][1]
    return jsonify(cash=cash, value=value, portfolio=portfolio, history=history, trades=trades, top=top)


@app.route('/twilio', methods=['POST', 'GET'])
def twilio():
    body = request.form['Body'].split(' ')
    resp = twilio.twiml.Response()
    myText = "unknown command. Please enter: <buy/sell TICKER #OFSHARES> to make a trade."
    if len(body) != 3:
        resp.message(myText)
        return str(resp)
    order, sym, value = body
    myText = "Nice! You put in an order to " + order.lower() + " " + value + " shares of " + sym.upper()
    resp.message(myText)
    utils.order(order, sym, value, g)
    return str(resp)


@app.route('/promptio', methods=['POST'])
def promptio():
    myJson = request.get_json()
    myText = "enter <@stock_00017 status> to check portfolio value. enter <@stock_00017 buy/sell TICKER #OFSHARES> to make a trade."
    body = myJson['message'].split(" ")
    myText = ""
    if body[0] == "status":
        myText = str(utils.get_portfolio_val(g))
    if len(body) == 3:
        order, sym, value = body
        utils.order(order, sym, value, g)
        myText = "Nice! You put in an order to " + order.lower() + " " + value + " shares of " + sym.upper()
    dat = jsonify(sendmms=False, showauthurl=False, authstate=None,
                  text=myText, speech=myText, status="OK", webhookreply=None,
                  images=[{"imageurl": None, "alttext": None}])  # insert json responses here
    resp = make_response(dat, 200, {"Content-Type": "application/json"})
    return resp
