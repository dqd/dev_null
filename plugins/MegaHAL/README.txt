MegaHAL chatting bot, using the megahal3 Python package:
https://pypi.org/project/megahal3/

Everything the bot is told through the "chat" command is appended to the
"megahal" file in the data directory and the brain lives next to it as
"megahal.brain". A missing or unreadable brain is rebuilt from the training
file when the plugin loads, which can take a while on large files.

Brains created by the Python 2 version of this plugin cannot be reused,
they are rebuilt automatically.
