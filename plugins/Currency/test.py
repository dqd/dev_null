import unittest

from supybot.test import PluginTestCase, network


class CurrencyTestCase(PluginTestCase):
    plugins = ("Currency",)

    @unittest.skipUnless(network, "network tests disabled")
    def testCurrency(self):
        self.assertRegexp("currency 10 EUR to CZK", r"^10\.00 EUR = \d+\.\d\d CZK$")
        self.assertRegexp("currency € to $", r"^1\.00 EUR = \d+\.\d\d USD$")

    @unittest.skipUnless(network, "network tests disabled")
    def testUnknownCurrency(self):
        self.assertError("currency XXX to EUR")
