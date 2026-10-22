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

Create the bot configuration with the wizard:

```
docker compose run --rm bot supybot-wizard
```

Answer the questions, keep the default `.` when asked where to create the
directories, and save the configuration under its default name. The
repository root is the home and working directory of the bot, so the
configuration file and the `conf`, `data`, `logs` and `backup` directories end
up right here, next to `plugins`, which the wizard adds to
`supybot.directories.plugins`, so the bundled plugins are available right
away.

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

The repository is mounted as `/home/bot`, the home and working directory of
the bot, so everything it owns lives in the repository root:

| Path      | Purpose |
| --------- | ------- |
| `*.conf`  | bot configuration, created by the wizard or [dev_null.conf](dev_null.conf) |
| `conf/`   | users, channels, ignores... |
| `data/`   | plugin data (e.g. the MegaHAL brain and training file) |
| `logs/`   | logs |
| `backup/` | backups of configuration and data |
| `plugins/` | the plugins from this repository |

The directories the bot writes to are ignored by git and created by the
entrypoint when missing. The whole repository is mounted rather than the
directories one by one because Limnoria rewrites its configuration file by
renaming a temporary file over it, which does not work on a file mounted on
its own.

An existing Limnoria installation can be moved in as well: copy its
configuration file and directories into the repository root and make sure the
paths in `supybot.directories.*` are relative or start with `/home/bot`.

The configuration of dev_null itself is in [dev_null.conf](dev_null.conf). It
lists only the settings that differ from Limnoria's defaults and is used as is:

```
docker compose up -d
```

The entrypoint starts the bot with the only `*.conf` file found in the
repository root. With more than one, set `LIMNORIA_CONFIG` in
`docker-compose.yml`.

## Extra plugins

Put your own plugins next to the bundled ones in `./plugins`, or mount another
directory and add it to `supybot.directories.plugins`:

```yaml
    volumes:
      - .:/home/bot
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

The bot runs as the user `bot` (UID 1000, GID 1000 by default). If the
repository is owned by a different user on the host, build with matching IDs:

```
LIMNORIA_UID=$(id -u) LIMNORIA_GID=$(id -g) docker compose build
```

## Starting at boot

The service has `restart: unless-stopped`, so Docker brings the bot back after
a reboot (or after the bot crashes) by itself, as long as Docker starts with
the system and the bot has been started once. On a Linux host with systemd:

```
sudo systemctl enable --now docker
docker compose up -d
```

That is all; the bot keeps restarting until it is stopped explicitly with
`docker compose stop` or `docker compose down`, after which it stays down
across reboots until started again.

## Other commands

Any command given to the container replaces the bot, for example:

```
docker compose run --rm bot supybot-adduser conf/users.conf
docker compose run --rm bot limnoria-test --plugins-dir plugins
```

## License

[WTFPL](LICENSE)
