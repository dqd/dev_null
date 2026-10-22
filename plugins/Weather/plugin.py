import requests
from supybot.commands import wrap
import supybot.callbacks as callbacks

SYMBOL_CODES = {
    "clearsky": "clear sky",
    "cloudy": "cloudy",
    "fair": "fair",
    "fog": "fog",
    "heavyrain": "heavy rain",
    "heavyrainandthunder": "heavy rain and thunder",
    "heavyrainshowers": "heavy rain showers",
    "heavyrainshowersandthunder": "heavy rain showers and thunder",
    "heavysleet": "heavy sleet",
    "heavysleetandthunder": "heavy sleet and thunder",
    "heavysleetshowers": "heavy sleet showers",
    "heavysleetshowersandthunder": "heavy sleet showers and thunder",
    "heavysnow": "heavy snow",
    "heavysnowandthunder": "heavy snow and thunder",
    "heavysnowshowers": "heavy snow showers",
    "heavysnowshowersandthunder": "heavy snow showers and thunder",
    "lightrain": "light rain",
    "lightrainandthunder": "light rain and thunder",
    "lightrainshowers": "light rain showers",
    "lightrainshowersandthunder": "light rain showers and thunder",
    "lightsleet": "light sleet",
    "lightsleetandthunder": "light sleet and thunder",
    "lightsleetshowers": "light sleet showers",
    "lightsnow": "light snow",
    "lightsnowandthunder": "light snow and thunder",
    "lightsnowshowers": "light snow showers",
    "lightssleetshowersandthunder": "light sleet showers and thunder",
    "lightssnowshowersandthunder": "light snow showers and thunder",
    "partlycloudy": "partly cloudy",
    "rain": "rain",
    "rainandthunder": "rain and thunder",
    "rainshowers": "rain showers",
    "rainshowersandthunder": "rain showers and thunder",
    "sleet": "sleet",
    "sleetandthunder": "sleet and thunder",
    "sleetshowers": "sleet showers",
    "sleetshowersandthunder": "sleet showers and thunder",
    "snow": "snow",
    "snowandthunder": "snow and thunder",
    "snowshowers": "snow showers",
    "snowshowersandthunder": "snow showers and thunder",
}
DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


class Weather(callbacks.Plugin):
    """Shows the current weather for a place."""

    @wrap(["text"])
    def weather(self, irc, msg, args, place):
        """<place>

        Current weather for a <place>.
        """
        email = self.registryValue("email")

        if not email:
            irc.error(
                "The email address is missing. "
                "Please configure the plugins.Weather.email directive.",
                Raise=True,
            )

        headers = {
            "User-Agent": "Limnoria ({})".format(email),
            "Accept": "application/json",
        }

        try:
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": place,
                    "addressdetails": 1,
                    "format": "jsonv2",
                    "limit": 1,
                },
                headers=headers,
                timeout=10,
            ).json()

            if (
                response
                and isinstance(response, list)
                and isinstance(response[0], dict)
                and response[0].get("lat")
                and response[0].get("lon")
            ):
                latitude = response[0]["lat"]
                longitude = response[0]["lon"]
                name = ", ".join(
                    part
                    for part in (
                        response[0].get("name") or place,
                        response[0].get("address", {}).get("country"),
                    )
                    if part
                )

                response = requests.get(
                    "https://api.met.no/weatherapi/locationforecast/2.0/compact",
                    params={
                        "lat": "{:.4f}".format(float(latitude)),
                        "lon": "{:.4f}".format(float(longitude)),
                    },
                    headers=headers,
                    timeout=10,
                ).json()

                if (
                    response
                    and response.get("properties")
                    and isinstance(response["properties"], dict)
                ):
                    properties = response["properties"]
                    weather = properties["timeseries"][0]
                    w = weather["data"]["instant"]["details"]
                    symbol_code = weather["data"]["next_1_hours"]["summary"][
                        "symbol_code"
                    ].split("_")[0]
                    irc.reply(
                        "The current temperature in {name} "
                        "is {w[air_temperature]} °C. "
                        "Conditions in the next 1 hour: {description}. "
                        "Humidity: {w[relative_humidity]} {units[relative_humidity]}. "
                        "Wind: {direction} {w[wind_speed]} {units[wind_speed]} ({time}).".format(
                            name=name,
                            description=SYMBOL_CODES.get(symbol_code, "unknown"),
                            w=w,
                            units=properties["meta"]["units"],
                            direction=DIRECTIONS[
                                int(w["wind_from_direction"] / 45) % 8
                            ],
                            time=weather["time"],
                        )
                    )
                else:
                    irc.error("Unable to fetch weather data.")
            else:
                irc.error("Unable to fetch location data.")
        except Exception as e:
            irc.error("{}: {}".format(type(e).__name__, e))


Class = Weather
