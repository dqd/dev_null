import supybot.conf as conf
import supybot.registry as registry


def configure(advanced):
    conf.registerPlugin("DevNull", True)


DevNull = conf.registerPlugin("DevNull")

conf.registerGlobalValue(
    DevNull,
    "spravci",
    registry.String(
        "",
        """The answer of the "spravci" command (the list of operators of
        #wikipedia-cs).""",
    ),
)

conf.registerGlobalValue(
    DevNull,
    "pivoAliases",
    registry.Json(
        {},
        """Nicks (in lower case) mapped to the form used by the "pivo"
        command, e.g. {"b42": "bečtyřicetdvojce"}. The bot's own nick is
        always "sobě".""",
    ),
)
