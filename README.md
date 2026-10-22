# dev_null

dev_null is dqd's IRC bot running on IRCnet. It is a
[Limnoria](https://limnoria.net/) bot in Docker, running on the latest
Python 3 on Debian under an unprivileged user, together with a few plugins
ported to Python 3:

- [Currency](plugins/Currency) converts between currencies.
- [DevNull](plugins/DevNull) assorted commands of the dev_null bot.
- [MegaHAL](plugins/MegaHAL) chats using the Markov chain conversation
  simulator from the [megahal3](https://pypi.org/project/megahal3/) package.
- [Weather](plugins/Weather) shows the current weather for a place.

## Quick start

Create the data directory and the bot configuration with the wizard:

```
mkdir data
docker compose run --rm bot supybot-wizard
```

Answer the questions, keep the default `.` when asked where to create the
directories, and save the configuration under its default name. The
configuration file and the `conf`, `data`, `logs` and `backup` directories
end up in `./data`. The plugins from this repository are mounted from
`./plugins` as `/data/plugins`, which the wizard adds to
`supybot.directories.plugins`, so they are available right away.

Start the bot:

```
docker compose up -d
```

Then load the plugins you want:

```
/msg <yourbot> load Currency
/msg <yourbot> load Weather
/msg <yourbot> load MegaHAL
```

## Configuration and data

Everything the bot owns lives in `./data`, mounted as `/data` in the
container:

| Path in `./data` | Purpose |
| ---------------- | ------- |
| `*.conf`         | bot configuration, created by the wizard |
| `conf/`          | users, channels, ignores... |
| `data/`          | plugin data (e.g. the MegaHAL brain and training file) |
| `logs/`          | logs |
| `backup/`        | backups of configuration and data |
| `plugins/`       | the plugins from this repository, mounted read-only from `./plugins` |

An existing Limnoria installation can be moved in as well: copy its
configuration file and directories into `./data` and make sure the paths in
`supybot.directories.*` are relative (the bot runs with `/data` as its working
directory) or start with `/data`.

The configuration of dev_null itself is in [dev_null.conf](dev_null.conf). It
lists only the settings that differ from Limnoria's defaults and can be used
instead of the wizard:

```
mkdir data
cp dev_null.conf data/
docker compose up -d
```

The entrypoint starts the bot with the only `*.conf` file found in `/data`.
With more than one, set `LIMNORIA_CONFIG` in `docker-compose.yml`.

## Extra plugins

Put your own plugins next to the bundled ones in `./plugins`, or mount another
directory and add it to `supybot.directories.plugins`:

```yaml
    volumes:
      - ./data:/data
      - ./plugins:/data/plugins:ro
      - /somewhere/else/plugins:/plugins:ro
```

```
supybot.directories.plugins: plugins, /plugins
```

Python packages needed by extra plugins go into `requirements.txt`, followed
by a rebuild:

```
docker compose build
```

## Unprivileged user

The bot runs as the user `bot` (UID 1000, GID 1000 by default). If
`./data` is owned by a different user on the host, build with matching IDs:

```
LIMNORIA_UID=$(id -u) LIMNORIA_GID=$(id -g) docker compose build
```

## Other commands

Any command given to the container replaces the bot, for example:

```
docker compose run --rm bot supybot-adduser data/conf/users.conf
docker compose run --rm bot limnoria-test --plugins-dir plugins
```

## License

[WTFPL](LICENSE)
