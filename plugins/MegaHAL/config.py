import supybot.conf as conf
import supybot.registry as registry


def configure(advanced):
    conf.registerPlugin("MegaHAL", True)


MegaHAL = conf.registerPlugin("MegaHAL")

conf.registerGlobalValue(
    MegaHAL,
    "order",
    registry.PositiveInteger(
        5,
        """Order of the Markov chain. A brain is tied to the order it was
        created with, so changing this value rebuilds the brain from the
        training file.""",
    ),
)

conf.registerGlobalValue(
    MegaHAL,
    "timeout",
    registry.PositiveFloat(
        1.0,
        """How long (in seconds) the bot looks for the best reply.""",
    ),
)
