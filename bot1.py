import socket
import random
import time
settings = []
readbuffer = ""

HOST = "irc.twitch.tv"
PORT = 6667
AUTH = "oauth:tdy8nrh7b9hf71mwt8cs1fdi74r8il"
NICK = "geenaky"
CHAT_CHANNEL = "kjiao"

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


def gen_rand_order():
    order = random.choice(['buy', 'buy', 'buy', 'buy', 'sell'])
    sym = random.choice(markets)
    val = random.randint(1, 100)

    return order + ' ' + sym + ' ' + str(val)

while True:
    s = socket.socket()
    s.connect((HOST, PORT))

    s.send(bytes("PASS %s\r\n" % AUTH, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (NICK, HOST, NICK), "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL, "UTF-8"))
    s.send(bytes("PRIVMSG #%s :%s\r\n" % (CHAT_CHANNEL, gen_rand_order()), "UTF-8"))
    print (gen_rand_order())
    time.sleep(3)
