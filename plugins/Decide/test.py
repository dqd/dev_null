###
# Copyright (c) 2012, b42
# Published under WTFPL.
#
###

from supybot.test import PluginTestCase


class DecideTestCase(PluginTestCase):
    plugins = ("Decide",)

    def testOneChoice(self):
        self.assertRegexp("decide something", "^(Yes|No)$")
        self.assertRegexp("decide something with multiple words", "^(Yes|No)$")

    def testMultiChoice(self):
        self.assertRegexp("decide a -- b", "^(a|b)$")
        self.assertRegexp("decide a -- b -- c", "^(a|b|c)$")
        self.assertRegexp("decide a x -- b y -- c z -- d w", "^(a x|b y|c z|d w)$")

    def testSameAnswer(self):
        answer = self.getMsg("decide a -- b -- c -- d -- e -- f").args[1]
        for _ in range(5):
            self.assertResponse("decide a -- b -- c -- d -- e -- f", answer)

    def testError(self):
        self.assertError("decide")
