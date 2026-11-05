###
# Copyright (c) 2012, b42
# Published under WTFPL.
#
###

import supybot.conf as conf
import supybot.registry as registry


def configure(advanced):
    conf.registerPlugin("Decide", True)


Decide = conf.registerPlugin("Decide")

conf.registerGlobalValue(
    Decide,
    "separator",
    registry.String("--", """String that separates multiple choices."""),
)

conf.registerGlobalValue(
    Decide,
    "interval",
    registry.PositiveInteger(
        6 * 60 * 60,
        """How often can the plugin change its mind (in seconds). Default is
        six hours. Change to 1 if you want to get a random answer every
        time.""",
    ),
)
