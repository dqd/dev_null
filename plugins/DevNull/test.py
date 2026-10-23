import io

from PIL import Image

import supybot.conf as conf
from supybot.test import ChannelPluginTestCase, PluginTestCase


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

    def testDescribeNeedsKey(self):
        self.assertError("describe http://example.com/image.png")

    def testDescribeRefusesLocalAddresses(self):
        with conf.supybot.plugins.DevNull.openaiApiKey.context("test"):
            for url in (
                "http://127.0.0.1/image.png",
                "http://10.1.2.3/image.png",
                "http://192.168.1.1:8080/image.png",
                "http://169.254.169.254/latest/meta-data/",
            ):
                self.assertRegexp("describe " + url, "cannot fetch")

            # Limnoria's own URL check refuses these before the plugin does.
            self.assertError("describe http://localhost/image.png")
            self.assertError("describe ftp://example.com/image.png")

    def testDescribeHelpers(self):
        plugin = self.irc.getCallback("DevNull")
        self.assertTrue(plugin._isPublicHost("8.8.8.8"))
        self.assertTrue(plugin._isPublicHost("2001:4860:4860::8888"))
        self.assertFalse(plugin._isPublicHost("0.0.0.0"))
        self.assertFalse(plugin._isPublicHost("::1"))
        self.assertFalse(plugin._isPublicHost("fe80::1"))
        self.assertFalse(plugin._isPublicHost("224.0.0.1"))

        source = io.BytesIO()
        Image.new("RGBA", (2048, 1024), "red").save(source, "PNG")
        with Image.open(io.BytesIO(plugin._prepareImage(source.getvalue()))) as image:
            self.assertEqual(image.format, "JPEG")
            self.assertEqual(image.size, (512, 256))
        self.assertRaises(ValueError, plugin._prepareImage, b"not an image")

        self.assertEqual(plugin._shorten("a\x01b\n  c"), "ab c")
        self.assertEqual(len(plugin._shorten("x" * 200)), 100)
        self.assertTrue(plugin._shorten("x" * 200).endswith("…"))


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
