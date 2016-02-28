import socket
import requests

settings = []
readbuffer = ""

HOST = "irc.twitch.tv"
PORT = 6667
AUTH = "oauth:akrgpwyx45s12aahidzgdy7ntzt942"
NICK = "kjiao"
CHAT_CHANNEL = "kjiao"
while True:
    s = socket.socket()
    s.connect((HOST, PORT))

    s.send(bytes("PASS %s\r\n" % AUTH, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (NICK, HOST, NICK), "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL, "UTF-8"))
    s.send(bytes("PRIVMSG #%s :Connected\r\n" % CHAT_CHANNEL, "UTF-8"))

    while 1:
        readbuffer = readbuffer+s.recv(1024).decode("UTF-8", errors="ignore")
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            x = 0
            out = ""
            line = str.rstrip(line)
            line = str.split(line)

            for index, i in enumerate(line):
                if x == 0:
                    user = line[index]
                    user = user.split('!')[0]
                    user = user[0:12] + ": "
                if x == 3:
                    out += line[index]
                    out = out[1:]
                if x >= 4:
                    out += " " + line[index]
                x = x + 1

            # Respond to ping, squelch useless feedback given by twitch, print output and read to list
            if user == "PING: ":
                s.send(bytes("PONG tmi.twitch.tv\r\n", "UTF-8"))
            elif user == ":tmi.twitch.tv: ":
                pass
            elif user == ":tmi.twitch.: ":
                pass
            elif user == ":%s.tmi.twitch.tv: " % NICK:
                pass
            else:
                trade = out.split(' ')
                if len(trade) == 3:
                    order, sym, val = trade
                    res = requests.post("http://localhost:5555/order", data={
                        "order": order,
                        "sym": sym,
                        "val": val})
                    res = requests.post("http://crowdinvestor.azurewebsites.net/order", data={
                        "order": order,
                        "sym": sym,
                        "val": val})
                    print(res)
            with open("commands.txt", "w") as f:
                    f.write(out + '\n')
