from __future__ import absolute_import
from errbot import BotPlugin, botcmd

from urllib2 import urlopen
from string import replace

import random
import json


def _giphy(gif):
    """
    Returns a gif for 'gif'

    Uses "production beta" API key for Giphy.
    """
    gifs = json.load(urlopen('http://api.giphy.com/'
                             'v1/gifs/search?q={}'
                             '&api_key=dc6zaTOxFJmzC'
                             '&limit=100'.format(gif)))
    random_gif = random.randint(0, len(gifs))
    random_decacher = str(random.randint(0, 1000))
    gif_url = gifs['data'][random_gif]['images']['fixed_width']['url']
    return gif_url + '?' + random_decacher


class potatoclicker(BotPlugin):

    @botcmd
    def potatogif(self, msg, args):
        """
        Returns a potato gif.
        """
        return _giphy('potato')

    @botcmd
    def potato(self, msg, args):
        """
        Incremenets the potato count for the user who calls it.
        """
        user = str(msg.frm)
        if user not in self:
            self[user] = 1
            return user + ' has one potato. ' \
                'Subsequent potatoes are granted, but only shown with ' \
                '!potatoes.'
        self[user] = self[user] + 1

    @botcmd
    def potatodice(self, msg, args):
        """
        Roll the dice, win potatoes or lose potatoes!
        """
        user = str(msg.frm)
        if user not in self:
            self[user] = -10
            return 'You haven\'t even used !potato before! You ' \
                'go negative 10 potatoes! {}'.format(_giphy('epicfail'))
        else:
            risky_potatoes = random.randint(-1000, 1000)
            self[user] = self[user] + risky_potatoes
            if risky_potatoes > 0:
                return 'You take a huge risk and it pays off! {} more ' \
                    'potatoes! {}'.format(risky_potatoes,
                                          _giphy('win'))
            elif risky_potatoes < 0:
                return 'Your risk is too much! You lose {} ' \
                    'potatoes! {}'.format(risky_potatoes * -1,
                                          _giphy('fail'))
            else:
                return '{} is boring! They gain or lose no ' \
                  'potatoes!'.format(user)

    @botcmd
    def potatoes(self, msg, args):
        """
        Prints the potato count with potatoes.
        """
        user = str(msg.frm)
        if user in self:
            potatoes = self[user]
            if potatoes == 0:
                return '{} has no potatoes!'.format(user)
            elif potatoes < 0:
                return '{} has a potato deficit!'.format(user)
            elif potatoes < 20:
                return '{} has this many potatoes: {}' \
                    .format(user, potatoes * ':sweet_potato:')
            else:
                return '{} has {} potatoes'.format(user, potatoes)
        else:
            return user + ' needs to !potato to get a potato.'

    @botcmd
    def potatowhoami(self, msg, args):
        """
        Says who you are.
        """
        return replace(str(msg.frm), '*', '')
