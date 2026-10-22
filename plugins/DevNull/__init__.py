"""
Assorted commands of the dev_null bot.
"""

from importlib import reload

import supybot
import supybot.world as world

__version__ = "2.0"

__author__ = supybot.Author("Pavel Mises", "dqd", "id@dqd.cz")

__contributors__ = {}

__url__ = "https://github.com/dqd/dev_null/"

from . import config
from . import plugin

reload(config)
reload(plugin)

if world.testing:
    from . import test  # noqa: F401

Class = plugin.Class
configure = config.configure
