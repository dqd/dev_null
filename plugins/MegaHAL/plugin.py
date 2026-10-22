import dbm
import glob
import os
import threading

from megahal import MegaHAL as Brain
from supybot.commands import wrap
import supybot.callbacks as callbacks
import supybot.conf as conf


class MegaHAL(callbacks.Plugin):
    """Chats using MegaHAL, the Markov chain conversation simulator."""

    def __init__(self, irc):
        super().__init__(irc)
        self.lock = threading.Lock()
        data = conf.supybot.directories.data
        # Everything the bot has been told, one phrase per line. The brain can
        # always be rebuilt from this file.
        self.training_file = data.dirize("megahal")
        self.brainfile = data.dirize("megahal.brain")
        self.brain = self._open_brain()

    def _open_brain(self):
        if dbm.whichdb(self.brainfile) is not None:
            try:
                return Brain(**self._brain_options())
            except Exception:
                self.log.exception(
                    "Cannot open the MegaHAL brain %s, rebuilding it.",
                    self.brainfile,
                )
                for path in glob.glob(glob.escape(self.brainfile) + "*"):
                    os.remove(path)

        brain = Brain(**self._brain_options())

        if os.path.exists(self.training_file):
            self.log.info(
                "Training the MegaHAL brain from %s, this can take a while.",
                self.training_file,
            )
            brain.train(self.training_file)
        else:
            with open(self.training_file, "w", encoding="utf-8"):
                pass

        brain.sync()
        return brain

    def _brain_options(self):
        return {
            "order": self.registryValue("order"),
            "brainfile": self.brainfile,
            "timeout": self.registryValue("timeout"),
        }

    @wrap(["text"])
    def chat(self, irc, msg, args, text):
        """<text>

        Replies to a message.
        """
        with self.lock:
            with open(self.training_file, "a", encoding="utf-8") as f:
                f.write(text.replace("\n", " "))
                f.write("\n")

            reply = self.brain.get_reply(text)

        irc.reply(reply)

    def die(self):
        with self.lock:
            self.brain.close()

        super().die()


Class = MegaHAL
