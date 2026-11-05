###
# Copyright (c) 2012, b42
# Published under WTFPL.
#
###

import random

from supybot.commands import wrap
import supybot.callbacks as callbacks


class Decide(callbacks.Plugin):
    """This plugin has only one command, 'decide'."""

    @wrap(["now", "text"])
    def decide(self, irc, msg, args, timestamp, text):
        """<question>

        Either gives a yes/no answer to a question, or if the question is
        a list of items separated by '--', picks one item randomly.
        """
        # make it so that the answers stay the same in one interval
        time_quotient = timestamp // self.registryValue("interval")

        # seed the generator with the part of the time we care about and
        # the (normalized) question
        rg = random.Random(str(time_quotient) + text.replace(" ", ""))

        choices = [s.strip() for s in text.split(self.registryValue("separator"))]

        if len(choices) == 1:
            choices = ["Yes", "No"]

        irc.reply(rg.choice(choices))


Class = Decide
