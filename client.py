from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from rq import Queue
from utils import process_diff
from worker import conn
import re


class Bot(irc.IRCClient):
    nickname = "wedgebot"

    def signedOn(self):
        self.join("#en.wikipedia")

    def privmsg(self, user, channel, msg):
        try:
            colors = re.compile("\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
            msg = colors.sub("", msg)
            diffid = msg.split("?diff=")[1].split("&oldid")[0]
            user = msg.split("* ")[1].split(" *")[0]
            self.queue.enqueue(process_diff, (diffid, user))
        except:
            pass


class Factory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        b = Bot()
        b.queue = Queue(connection=conn)
        return b


if __name__ == '__main__':
    reactor.connectTCP("irc.wikimedia.org", 6667, Factory())
    reactor.run()
