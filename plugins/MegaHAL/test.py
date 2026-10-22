from supybot.test import PluginTestCase


class MegaHALTestCase(PluginTestCase):
    plugins = ("MegaHAL",)

    def testChat(self):
        self.assertNotError("chat Hello, my name is Pavel.")
        self.assertNotError("chat I like trains and penguins.")
        self.assertRegexp("chat Tell me about penguins.", ".")
