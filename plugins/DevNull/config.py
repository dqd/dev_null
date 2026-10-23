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

conf.registerGlobalValue(
    DevNull,
    "openaiApiKey",
    registry.String(
        "",
        """The OpenAI API key used by the "describe" command.""",
        private=True,
    ),
)

conf.registerGlobalValue(
    DevNull,
    "describeModel",
    registry.String(
        "gpt-5.4-mini",
        """The OpenAI model the "describe" command sends the image to.""",
    ),
)

conf.registerGlobalValue(
    DevNull,
    "describeMaxSize",
    registry.PositiveInteger(
        8 * 1024 * 1024,
        """The largest image, in bytes, the "describe" command downloads.""",
    ),
)

conf.registerGlobalValue(
    DevNull,
    "describePrompt",
    registry.String(
        "Describe the image in one short English sentence of at most 100 characters.",
        """The instruction sent to the model together with the image by the
        "describe" command. The reply is cut to 100 characters anyway.""",
    ),
)
