from datetime import datetime
import traceback
import math
import csv

ref = datetime(2016, 2, 27, 22, 20, 17, 410706)
markets = ['F_AD', 'F_BO', 'F_BP', 'F_C', 'F_CC', 'F_CD',
           'F_CL', 'F_CT', 'F_DX', 'F_EC', 'F_ED', 'F_ES', 'F_FC', 'F_FV', 'F_GC',
           'F_HG', 'F_HO', 'F_JY', 'F_KC', 'F_LB', 'F_LC', 'F_LN', 'F_MD', 'F_MP',
           'F_NG', 'F_NQ', 'F_NR', 'F_O', 'F_OJ', 'F_PA', 'F_PL', 'F_RB', 'F_RU',
           'F_S', 'F_SB', 'F_SF', 'F_SI', 'F_SM', 'F_TU', 'F_TY', 'F_US', 'F_W', 'F_XX',
           'F_YM']

markets += ['CASH', 'AAPL', 'ABBV', 'ABT', 'ACN', 'AEP', 'AIG', 'ALL',
            'AMGN', 'AMZN', 'APA', 'APC', 'AXP', 'BA', 'BAC', 'BAX', 'BK', 'BMY',  'BRKB', 'C',
            'CAT', 'CL', 'CMCSA', 'COF', 'COP', 'COST', 'CSCO', 'CVS', 'CVX', 'DD', 'DIS', 'DOW',
            'DVN', 'EBAY', 'EMC', 'EMR', 'EXC', 'F', 'FB', 'FCX', 'FDX', 'FOXA', 'GD', 'GE',
            'GILD', 'GM', 'GOOGL', 'GS', 'HAL', 'HD', 'HON', 'HPQ', 'IBM', 'INTC', 'JNJ', 'JPM',
            'KO', 'LLY', 'LMT', 'LOW', 'MA', 'MCD', 'MDLZ', 'MDT', 'MET', 'MMM', 'MO', 'MON',
            'MRK', 'MS', 'MSFT', 'NKE', 'NOV', 'NSC', 'ORCL', 'OXY', 'PEP', 'PFE', 'PG', 'PM',
            'QCOM', 'RTN', 'SBUX', 'SLB', 'SO', 'SPG', 'T', 'TGT', 'TWX', 'TXN', 'UNH', 'UNP',
            'UPS', 'USB', 'UTX', 'V', 'VZ', 'WAG', 'WFC', 'WMT', 'XOM']

dataDict = {}
portfolio = {}
trades = []

for symbol in markets:
    priceData = []
    filename = './FlaskWebProject/tickerData/' + symbol + '.txt'
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            priceData.append(row)
    dataDict[symbol] = priceData


def valid_order(order, sym, val):
    if order.lower() not in ['b', 'buy', 's', 'sell']:
        return False
    if sym.upper() not in markets:
        return False
    if isinstance(val, (str, unicode)):
        if not val.isdigit():
            print "val is not digit string"
            return False
        return True
    if not isinstance(val, (int, float)):
        print type(val).__name__
        return False
    return True


def get_quote(symbol):
    if symbol not in dataDict.keys():
        print symbol
        print "Symbol not in"
        return None
    now = datetime.now()
    offset = now - ref
    print offset
    return float(dataDict[symbol][int(offset.total_seconds()) // 15][1])


def order(order, sym, val, g):
    try:
        if order.lower() in ['b', 'buy']:
            buy(sym.upper(), val, g)

        elif order.lower() in ['s', 'sell']:
            sell(sym.upper(), val, g)
        else:
            return

        g.db.execute("INSERT INTO orders (trade) VALUES (?)", [str(order) + ' ' + str(sym) + ' ' + str(val)])
        g.db.commit()
    except:
        return traceback.format_exc()


def get_trades(g):
    history = []
    trades = g.db.execute("SELECT trade FROM orders ORDER BY ID DESC").fetchall(),
    for trade in trades[0]:
        history.append(trade[0])
    return history


def buy(sym, val, g):
    try:
        quote = get_quote(sym)
        if not quote:
            return quote

        g.db.execute("INSERT OR IGNORE INTO portfolio VALUES (?,?)", ['funds', 10**6])
        funds = g.db.execute("SELECT sym, amount FROM portfolio WHERE sym = ?", ["funds"]).fetchall()[0][1]
        cost = quote * float(val)
        print 'quotea: ' + str(quote)
        print 'cost: ' + str(cost)
        g.db.execute("INSERT OR IGNORE INTO portfolio VALUES (?,?)", [sym, 0])
        g.db.execute("UPDATE portfolio SET amount = amount + ? WHERE sym = ?", [val, sym])
        g.db.execute("UPDATE portfolio SET amount = ? WHERE sym = ?", [funds - cost, "funds"])
    except:
        print traceback.format_exc()


def sell(sym, val, g):
    try:
        quote = get_quote(sym)
        if not quote:
            return quote
        amount = g.db.execute("SELECT sym, amount FROM portfolio WHERE sym = ?", [sym]).fetchall()[0][1]
        funds = g.db.execute("SELECT sym, amount FROM portfolio WHERE sym = ?", ["funds"]).fetchall()[0][1]
        if float(val) > amount:
            return
        profit = quote * float(val)
        g.db.execute("UPDATE portfolio SET amount = amount - ? WHERE sym = ?", [val, sym])
        g.db.execute("UPDATE portfolio SET amount = ? WHERE sym = ?", [funds + profit, "funds"])
    except:
        print traceback.format_exc()


def get_portfolio(g):
    try:
        rows = g.db.execute("SELECT sym, amount FROM portfolio where sym != ?", ['funds']).fetchall()
        portfolio = {}
        for sym, amount in rows:
            portfolio[sym] = amount

        return portfolio
    except:
        return traceback.format_exc()


def get_portfolio_val(g):
    try:
        value = 0
        portfolio = get_portfolio(g)
        funds = g.db.execute("SELECT sym, amount FROM portfolio WHERE sym = ?", ["funds"]).fetchall()[0][1]
        for sym in portfolio:
            quote = get_quote(sym)
            print 'quoteb: ' + str(quote)
            value += quote * portfolio[sym]

        print 'portfolio: ' + str(value)
        print 'funds: ' + str(funds)
        update_history(value+funds, g)
        return value + funds
    except:
        print 'shit'
        print traceback.format_exc()


def update_history(val, g):
    try:
        latest = g.db.execute("SELECT value FROM history ORDER BY ID DESC LIMIT 1").fetchone()
        if math.fabs(val - latest[0]) > 1e-09:
            g.db.execute("INSERT INTO history (value) VALUES (?)", [val])
            g.db.commit()
    except:
        return traceback.format_exc()


def get_history(g):
    history = []
    trades = g.db.execute("SELECT value, ID FROM history ORDER BY ID DESC LIMIT 120").fetchall(),
    for trade in trades[0]:
        history.append(trade[0])
    return history


def get_top(g):
    stocks = []
    portfolio = get_portfolio(g)
    for sym in portfolio:
        quote = get_quote(sym)
        value = quote * portfolio[sym]
        stocks.append((sym, value))
    stocks = sorted(stocks, key=lambda x: -x[1])
    print stocks
    return stocks
