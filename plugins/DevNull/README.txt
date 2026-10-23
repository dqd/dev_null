Assorted commands of the dev_null bot on IRC: penis, blabol, buzzword,
haf, bot, prd, date, pivo, google, images, enwiki, cswiki, skwiki, spravci,
twitter, tourette and describe, plus a snarfer turning [[wiki links]] into
Wikipedia URLs on #botnik, #dev_null and #wikipedia-cs.

The "spravci" command answers with the plugins.DevNull.spravci value.

The "pivo" command looks up the dative form of a nick in
plugins.DevNull.pivoAliases, a JSON object of lower-case nicks:
/msg <yourbot> config plugins.DevNull.pivoAliases {"b42": "bečtyřicetdvojce"}
The bot's own nick is always "sobě".

The "tourette" command picks its words from expletives.txt in this directory,
one word per line; the file is read once when the plugin is loaded.

The "describe" command downloads the image at the given URL and asks an
OpenAI model (plugins.DevNull.describeModel, gpt-5.4-mini by default) for a
one-line English description of at most 100 characters. It needs an API key in
plugins.DevNull.openaiApiKey:
/msg <yourbot> config plugins.DevNull.openaiApiKey sk-...
The image is fetched with Limnoria's own HTTP client, so
supybot.protocols.http.proxy and supybot.protocols.http.userAgents apply. Only
public http(s) hosts are fetched (loopback, private and link-local addresses
are refused, both for the given URL and for the one a redirect ends at), the
response must carry an image Content-Type and at most
plugins.DevNull.describeMaxSize bytes (8 MiB by default) are downloaded. The image is shrunk to fit 512x512 and re-encoded as
a JPEG without metadata before it is sent to OpenAI; the wording of the
request is plugins.DevNull.describePrompt. Every call costs money, so you may
want to restrict who can use the command, e.g.
/msg <yourbot> defaultcapability add -DevNull.describe
and grant the DevNull.describe capability to trusted users only.
