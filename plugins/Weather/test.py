import os
import unittest

import supybot.conf as conf
from supybot.test import PluginTestCase, network

# Nominatim rejects requests identified by made-up contact addresses, so the
# network test needs a real one.
EMAIL = os.environ.get("LIMNORIA_TEST_EMAIL")


class WeatherTestCase(PluginTestCase):
    plugins = ("Weather",)

    def testMissingEmail(self):
        self.assertError("weather Prague")

    @unittest.skipUnless(
        network and EMAIL, "network tests disabled or LIMNORIA_TEST_EMAIL unset"
    )
    def testWeather(self):
        with conf.supybot.plugins.Weather.email.context(EMAIL):
            self.assertRegexp(
                "weather Prague",
                r"^The current temperature in .+ is -?\d+(\.\d+)? °C\. Conditions in the next 1 hour: ",
            )
