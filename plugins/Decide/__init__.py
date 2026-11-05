###
# Copyright (c) 2012, b42
# Published under WTFPL.
#
###

"""
Provides 'decide' command, which lets the bot decide important stuff instead of
you.
"""

from importlib import reload

import supybot
import supybot.world as world

__version__ = "1.0"

__author__ = supybot.Author("b42", "b42", "b42@srck.net")

__contributors__ = {
    supybot.Author("Pavel Mises", "dqd", "id@dqd.cz"): ["port to Python 3"],
}

__url__ = "https://github.com/dqd/dev_null/"

from . import config
from . import plugin

reload(config)
reload(plugin)

if world.testing:
    from . import test  # noqa: F401

Class = plugin.Class
configure = config.configure
