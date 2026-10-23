import os
import re
import time
import zlib
from datetime import datetime, timedelta
from random import choice, randint, sample
from urllib.parse import quote, urlencode

import requests

from supybot.commands import additional, optional, urlSnarfer, wrap
import supybot.ircmsgs as ircmsgs
import supybot.callbacks as callbacks


class DevNull(callbacks.PluginRegexp):
    """Assorted commands of the dev_null bot."""

    regexps = ["wikiSnarfer", "badWordsSnarfer"]

    def __init__(self, irc):
        super().__init__(irc)
        self.expletives = self._loadExpletives()

    def _loadExpletives(self):
        """Reads the words for the "tourette" command from expletives.txt
        next to this file, one per line; blank lines are skipped."""
        path = os.path.join(os.path.dirname(__file__), "expletives.txt")
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def penis(self, irc, msg, args, nick):
        """[<nick>]

        Measures the length of the user's penis.
        """

        if not nick:
            nick = msg.nick

        if not nick:
            irc.error("Zadejte nick uživatele, kterému mám změřit penis.")
            return

        try:
            hostmask = irc.state.nickToHostmask(nick).split("!", 1)
            penisLength = zlib.crc32(hostmask[1].encode("utf-8")) % 21 + 7
        except KeyError:
            irc.error("Uživateli se nedá podívat do kalhot. :'-(")
            return

        if nick == msg.nick:
            penisArray = [
                "Tak se ti mrkneme do kalhot",
                "Ukaž ho",
                "Tak ho teda vyndej",
                "Sundej si ty spoďáry",
                "Kuk",
                "Mrk",
                "Už ti ho měřím",
                "Nestyď se",
                "Hledam metr... Uz ho mam",
                "Jdem na to",
                "Ukaž se, bejku",
                "Zjistíme, jestli jsi chlap",
                "Jen ti tam přiložím pravítko",
                "Koukneme se na toho tvého macka",
            ]
        else:
            penisArray = [
                "Tak se mu mrkneme do kalhot",
                "Ať ho ukáže",
                "Ať ho teda vyndá",
                "Sundám mu ty spoďáry",
                "Kuk",
                "Mrk",
                "Už mu ho měřím",
                "Ať se nestydí",
                "Hledám metr... Už ho mám",
                "Jdem na to",
                "Ať se ukáže, bejk",
                "Zjistíme, jestli je chlap",
                "Jen mu tam přiložím pravítko",
                "Koukneme se na toho jeho macka",
            ]

        penisMsg = choice(penisArray) + "... "

        if penisLength < 10:
            penisMsg += "Trpaslík. :-("
        elif penisLength < 15:
            penisMsg += "Podprůměr. :-|"
        elif penisLength < 20:
            penisMsg += "Normálka. :-)"
        else:
            penisMsg += "Obr! :-O"

        irc.reply(penisMsg + " " + str(penisLength) + " cm", prefixNick=True)

    penis = wrap(penis, [additional("text")])

    def blabol(self, irc, msg, args):
        """takes no arguments

        Produces some management babble.
        """
        blah = [
            [
                "Kolegové,",
                "Na druhé straně",
                "Stejně tak",
                "Nesmíme však zapomínat, že",
                "Tímto způsobem",
                "Závažnost těchto problémů je natolik zřejmá, že",
                "Každodenní praxe nám potvrzuje, že",
                "Pestré a bohaté zkušenosti",
                "Poslání organizace, zejména pak",
                "Ideové úvahy nejvyššího řádu a rovněž",
            ],
            [
                "realizace plánovaných vytyčených úkolů",
                "rámec a místa výchovy kádrů",
                "stabilní a kvantitativní vzrůst a sféra naší aktivity",
                "vytvořená struktura organizace",
                "nový model organizační činnosti",
                "stálé, informačně-propagandistické zabezpečení naší práce",
                "další rozvoj různých forem činnosti",
                "upřesnění a rozvoj struktur",
                "konzultace se širokým aktivem",
                "počátek každodenní práce na poli formování pozice",
            ],
            [
                "hraje závažnou roli při utváření",
                "vyžadují od nás analýzy",
                "vyžadují nalezení a jednoznačné upřesnění",
                "napomáhá přípravě a realizaci",
                "zabezpečuje širokému okruhu specialistů účast při tvorbě",
                "ve značné míře podmiňuje vytvoření",
                "umožňuje splnit významné úkoly na rozpracování",
                "umožňuje zhodnotit význam",
                "představuje pozoruhodný experiment prověrky",
                "vyvolává proces zavádění a modernizace",
            ],
            [
                "existujících finančních a administrativních podmínek",
                "dalších směrů rozvoje",
                "systému masové účasti",
                "pozic jednotlivých účastníků k zadaným úkolům",
                "nových návrhů",
                "systému výchovy kádrů odpovídajících aktuálním potřebám",
                "směrů progresivního rozvoje",
                "odpovídajících podmínek aktivizace",
                "modelu rozvoje",
                "forem působení",
            ],
        ]

        bla = ""

        for b in blah:
            bla += choice(b) + " "

        irc.reply(bla[0:-1] + ".", prefixNick=True)

    def buzzword(self, irc, msg, args):
        """takes no arguments

        Write a buzzword.
        """

        words = [
            [
                "integrated",
                "total",
                "systematized",
                "parallel",
                "functional",
                "responsive",
                "optional",
                "synchronized",
                "compatible",
                "balanced",
            ],
            [
                "management",
                "organizational",
                "monitored",
                "reciprocal",
                "digital",
                "logistical",
                "transitional",
                "incremental",
                "third-generation",
                "policy",
            ],
            [
                "options",
                "flexibility",
                "capability",
                "mobility",
                "programming",
                "concept",
                "time-phase",
                "projection",
                "hardware",
                "hardware",
            ],
        ]

        irc.reply(choice(words[0]) + " " + choice(words[1]) + " " + choice(words[2]))

    def haf(self, irc, msg, args):
        """takes no arguments

        Imitates animal sounds.
        """
        animals = [
            "Haf",
            "Mňau",
            "Búúú",
            "Krááá",
            "Béée",
            "Méée",
            "Í-ááá",
            "Wraaau",
            "Vrrr",
            "Vruuummm",
            "Vzuuummm",
            "Bzzz",
            "Kvááák",
            "Kvííí",
            "Chro",
            "Kvíííík",
            "Kvo",
            "Huhu",
            "Wow",
            "Joj",
            "Blah",
        ]
        irc.reply(choice(animals) + "!", prefixNick=True)

    def bot(self, irc, msg, args):
        """takes no arguments

        Compatible function with Lambdabot.
        """
        irc.reply(":)", prefixNick=False)

    def prd(self, irc, msg, args):
        """takes no arguments

        Farts.
        """
        irc.reply("*p" + ("r" * randint(1, 10)) + "d*", prefixNick=False)

    def date(self, irc, msg, args, zone):
        """[<timezone>]

        The actual date and time.
        """
        try:
            shift = int(zone)
        except (TypeError, ValueError):
            shift = 1

        if shift > 12:
            shift %= 12
        elif shift < -12:
            shift %= -12

        shift -= 1

        shifted_date = (datetime.now() + timedelta(shift / 24.0)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        localtime = time.localtime()

        irc.reply(
            "%s (UTC%+d)" % (shifted_date, shift + (2 if localtime.tm_isdst else 1)),
            prefixNick=False,
        )

    date = wrap(date, [additional("text")])

    def pivo(self, irc, msg, args, nick):
        """[<nick>]

        Brings a beer to the user.
        """

        if not nick:
            nick = msg.nick

        if nick.lower() == irc.nick.lower():
            nick = "sobě"
        else:
            # Dative forms of nicks, e.g. {"b42": "bečtyřicetdvojce"}.
            aliases = self.registryValue("pivoAliases")
            nick = aliases.get(nick.lower()) or nick

        answers = [
            "otevřel " + nick + " oroseného lahváče",
            "načepoval " + nick + " tuplák světlého ležáku",
            "donesl " + nick + " vychlazenou plechovku",
            "namíchal " + nick + " půllitr řezaného",
            "přinesl " + nick + " korbel černého piva, je prý dobré na prsa",
            "nabídnul " + nick + " výživné kvasnicové pivo",
            "vnutil " + nick + " škopek Starobrna pro dobré sraní",
            "has connection reset by beer",
        ]

        irc.reply(choice(answers) + ".", action=True)

    pivo = wrap(pivo, [additional("text")])

    def google(self, irc, msg, args, q):
        """[<question>]

        Promotes the use of the Google search engine.
        """

        if q:
            irc.reply("http://cs.lmgtfy.com/?" + urlencode({"q": q}))
        else:
            irc.reply("Use Google, Luke!")

    google = wrap(google, [optional("text")])

    def images(self, irc, msg, args, q):
        """[<question>]

        Link to Google Images.
        """

        if q:
            irc.reply("http://images.google.cz/images?" + urlencode({"q": q}))
        else:
            irc.reply("http://images.google.cz/")

    images = wrap(images, [optional("text")])

    def _wiki(self, link, version):
        wikipedia = "https://" + version + ".wikipedia.org/"

        if link:
            link = link[0].upper() + link[1:].replace(" ", "_")
            return wikipedia + "wiki/" + quote(link, safe="/:#")
        return wikipedia

    def enwiki(self, irc, msg, args, q):
        """[<question>]

        Returns a link to the English Wikipedia.
        """
        irc.reply(self._wiki(q, "en"))

    enwiki = wrap(enwiki, [optional("text")])

    def cswiki(self, irc, msg, args, q):
        """[<question>]

        Returns a link to the Czech Wikipedia.
        """
        irc.reply(self._wiki(q, "cs"))

    cswiki = wrap(cswiki, [optional("text")])

    def skwiki(self, irc, msg, args, q):
        """[<question>]

        Returns a link to the Slovak Wikipedia.
        """
        irc.reply(self._wiki(q, "sk"))

    skwiki = wrap(skwiki, [optional("text")])

    def _urlify(self, s):
        if s:
            s = quote(s.replace(" ", "_")).replace("%23", "#")
            s = s[0].upper() + s[1:]
        return s

    def wikiSnarfer(self, irc, msg, match):
        r"\[\[[^\]]+\]\]"

        channel = msg.args[0]
        text = msg.args[1]

        if (
            not irc.isChannel(channel)
            or channel not in ["#botnik", "#dev_null", "#wikipedia-cs"]
            or "cslinky" in (x.lower() for x in irc.state.channels[channel].users)
        ):
            return

        for x in re.findall(r"(\[\[[^\]]+\]\])", text):
            x = x[2:-2]
            domain = "cs"
            wm = False

            if "|" in x:
                x = x[: x.index("|")]

            if ":" in x:
                s = x.split(":")

                if s[0] in ["meta", "commons"]:
                    wm = True
                    domain = s[0]
                    s = s[1:]
                elif len(s[0]) in [2, 3] and s[0] == s[0].lower():
                    domain = s[0]
                    s = s[1:]

                article = ":".join(map(self._urlify, s))
            else:
                article = self._urlify(x)

            if wm:
                r = "https://%s.wikimedia.org/wiki/%s" % (domain, article)
            else:
                r = "https://%s.wikipedia.org/wiki/%s" % (domain, article)

            if "#" not in r:
                r += "?redirect=no"

            irc.reply(r, prefixNick=False)

    wikiSnarfer = urlSnarfer(wikiSnarfer)

    def badWordsSnarfer(self, irc, msg, match):
        r"It's Madeleine Czura"

        channel = msg.args[0]

        if not irc.isChannel(channel):
            return

        if irc.state.channels[channel].isOp(irc.nick) and not irc.state.channels[
            channel
        ].isOp(msg.nick):
            irc.queueMsg(ircmsgs.kick(channel, msg.nick, "KTHXBYE!"))
            irc.noReply()

    badWordsSnarfer = urlSnarfer(badWordsSnarfer)

    def spravci(self, irc, msg, args):
        """takes no arguments

        Lists the operators of #wikipedia-cs.
        """
        irc.reply(self.registryValue("spravci") or "nevím", prefixNick=False)

    def twitter(self, irc, msg, args, q):
        """[<message>]

        Replies with Twitter account.
        """
        irc.reply("https://twitter.com/ircdump")

    twitter = wrap(twitter, [optional("text")])

    def predpoved(self, irc, msg, args):
        """takes no arguments

        Shows the weather forecast from Meteocentrum."""

        try:
            response = requests.get(
                "https://www.meteocentrum.cz/predpoved-pocasi/cz/740/brno",
                headers={"User-Agent": "Limnoria"},
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException:
            return irc.reply("Chyba spojení.")

        r = re.search(r'property="og:description"\s+content="([^"]+)', response.text)

        if r:
            return irc.reply(r.group(1).strip())

        return irc.reply("Změnil se formát předpovědi. Co teď budeme dělat?")

    predpoved = wrap(predpoved)

    def tourette(self, irc, msg, args):
        """takes no arguments

        Simulates Tourette syndrome."""
        return irc.reply(" ".join(sample(self.expletives, 15)))

    tourette = wrap(tourette)


Class = DevNull
