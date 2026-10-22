import supybot.conf as conf
import supybot.registry as registry


def configure(advanced):
    conf.registerPlugin("Weather", True)


Weather = conf.registerPlugin("Weather")

conf.registerGlobalValue(
    Weather,
    "email",
    registry.String(
        "",
        """Sets the email used in the User-Agent requests sent by the plugin.""",
        private=True,
    ),
)
