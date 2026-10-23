Assorted commands of the dev_null bot on IRC: penis, blabol, buzzword,
haf, bot, prd, date, pivo, google, images, enwiki, cswiki, skwiki, spravci,
twitter, predpoved and tourette, plus a snarfer turning [[wiki links]] into
Wikipedia URLs on #botnik, #dev_null and #wikipedia-cs.

The "spravci" command answers with the plugins.DevNull.spravci value.

The "pivo" command looks up the dative form of a nick in
plugins.DevNull.pivoAliases, a JSON object of lower-case nicks:
/msg <yourbot> config plugins.DevNull.pivoAliases {"b42": "bečtyřicetdvojce"}
The bot's own nick is always "sobě".

The "tourette" command picks its words from expletives.txt in this directory,
one word per line; the file is read once when the plugin is loaded.
