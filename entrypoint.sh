#!/bin/sh
# Starts Limnoria with the configuration found in /data.
#
# Any arguments are executed instead of the bot, which makes it possible to run
# e.g. the configuration wizard:
#
#     docker compose run --rm bot supybot-wizard
set -eu

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

# Limnoria removes missing plugin directories from the configuration, so make
# sure the plugins directory exists even when nothing is mounted there,
# together with the directories for backups and logs.
mkdir -p /data/backup /data/logs /data/plugins

if [ -z "${LIMNORIA_CONFIG:-}" ]; then
    set -- /data/*.conf
    if [ "$#" -eq 1 ] && [ -f "$1" ]; then
        LIMNORIA_CONFIG=$1
    else
        echo "Expected exactly one *.conf file in /data or LIMNORIA_CONFIG set." >&2
        echo "Create a configuration with: docker compose run --rm bot supybot-wizard" >&2
        exit 1
    fi
fi

exec supybot "$LIMNORIA_CONFIG"
