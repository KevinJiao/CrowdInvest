from datetime import datetime
import traceback
import math
import csv

ref = datetime(2016, 2, 27, 11, 39, 32, 684190)
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
funds = 10**6
history = [10**6]
trades = []

for symbol in markets:
    priceData = []
    filename = './FlaskWebProject/tickerData/' + symbol + '.txt'
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            priceData.append(row)
    dataDict[symbol] = priceData


def get_quote(symbol):
    if symbol not in dataDict.keys():
        return None
    now = datetime.now()
    offset = now - ref
    return float(dataDict[symbol][offset.seconds / 15][1])


def order(order, sym, val):
    if order.lower() in ['b', 'buy']:
        buy(sym.upper(), val)

    elif order.lower() in ['s', 'sell']:
        sell(sym.upper(), val)

    global trades
    if len(trades) > 10:
        trades.pop()
    trades.insert(0, str(order) + ' ' + str(sym) + ' ' + str(val))


def buy(symbol, val):
    quote = get_quote(symbol)
    if not quote:
        return

    # if val > funds:
    #    print "insufficient funds"
    #    return
    if symbol not in portfolio:
        portfolio[symbol] = float(val)/float(quote)
    else:
        portfolio[symbol] += float(val)/float(quote)
    global funds
    funds -= float(val)


def sell(symbol, val):
    quote = get_quote(symbol)
    if not quote or symbol not in portfolio:
        return

    if portfolio[symbol] < float(val)/quote:
        portfolio[symbol] = 0
    else:
        portfolio[symbol] -= float(val)/quote


def get_portfolio_val():
    try:
        val = 0
        for sym in portfolio:
            quote = get_quote(sym)
            val += quote * portfolio[sym]

        global funds
        val += funds
        if math.fabs(val - history[0]) > 1e-09:
            update_history(val)
        return val
    except:
        print traceback.format_exc()


def update_history(val):
    try:
        if len(history) > 120:
            history.pop()
        history.insert(0, val)
    except:
        print traceback.format_exc()
