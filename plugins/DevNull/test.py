import unittest

import supybot.conf as conf
from supybot.test import ChannelPluginTestCase, PluginTestCase, network


class DevNullTestCase(PluginTestCase):
    plugins = ("DevNull",)

    def testSimpleCommands(self):
        self.assertResponse("bot", ":)")
        self.assertRegexp("prd", r"^\*pr+d\*$")
        self.assertRegexp("blabol", r"\.$")
        self.assertRegexp("buzzword", r"^\S+ \S+ \S+$")
        self.assertRegexp("haf", r"!$")
        self.assertRegexp("tourette", r"^(\S+ ){14}\S+")

    def testDate(self):
        self.assertRegexp("date", r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d \(UTC[+-]\d+\)$")
        self.assertRegexp("date 5", r"\(UTC\+[56]\)$")

    def testPenis(self):
        self.assertRegexp("penis", r" \d+ cm$")
        self.assertError("penis nobody")

    def testPivo(self):
        # The sender and the bot are both "test" in the test harness.
        self.assertRegexp(
            "pivo", r"^\x01ACTION (.* sobě .*|has connection reset by beer)\.\x01$"
        )
        self.assertRegexp("pivo foo", r"( foo |beer)")
        with conf.supybot.plugins.DevNull.pivoAliases.context(
            {"b42": "bečtyřicetdvojce"}
        ):
            self.assertRegexp("pivo B42", r"( bečtyřicetdvojce |beer)")

    def testLinks(self):
        self.assertResponse("google", "Use Google, Luke!")
        self.assertResponse(
            "google kolik je hodin", "http://cs.lmgtfy.com/?q=kolik+je+hodin"
        )
        self.assertResponse("images", "http://images.google.cz/")
        self.assertResponse("enwiki", "https://en.wikipedia.org/")
        self.assertResponse("enwiki foo bar", "https://en.wikipedia.org/wiki/Foo_bar")
        self.assertResponse("cswiki Praha", "https://cs.wikipedia.org/wiki/Praha")
        self.assertResponse(
            "skwiki Bratislava", "https://sk.wikipedia.org/wiki/Bratislava"
        )
        self.assertResponse("twitter", "https://twitter.com/ircdump")

    def testSpravci(self):
        self.assertResponse("spravci", "nevím")

    @unittest.skipUnless(network, "network tests disabled")
    def testPredpoved(self):
        self.assertNotError("predpoved")


class DevNullChannelTestCase(ChannelPluginTestCase):
    plugins = ("DevNull",)
    channel = "#dev_null"

    def testWikiSnarfer(self):
        self.assertSnarfResponse(
            "[[Praha]]", "https://cs.wikipedia.org/wiki/Praha?redirect=no"
        )
        self.assertSnarfResponse(
            "[[en:Prague|the city]]", "https://en.wikipedia.org/wiki/Prague?redirect=no"
        )
        self.assertSnarfResponse(
            "[[commons:Category:Prague]]",
            "https://commons.wikimedia.org/wiki/Category:Prague?redirect=no",
        )
        self.assertSnarfResponse(
            "[[Praha#Historie]]", "https://cs.wikipedia.org/wiki/Praha#Historie"
        )
