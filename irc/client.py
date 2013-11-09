from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import re


class Bot(irc.IRCClient):
    nickname = "wedgebot"

    def signedOn(self):
        self.join("#en.wikipedia")

    def privmsg(self, user, channel, msg):
        print msg


class Factory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Bot()


reactor.connectTCP("irc.wikimedia.org", 6667, Factory())
reactor.run()