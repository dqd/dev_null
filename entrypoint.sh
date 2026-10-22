#!/bin/sh
# Starts Limnoria with the configuration found in its home directory.
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
# sure the plugins directory exists, together with the other directories the
# bot writes to (they are ignored by git, so a fresh clone lacks them).
if ! cd "$HOME"; then
    echo "Cannot enter $HOME (running as $(id -u):$(id -g)); the repository is mounted there." >&2
    echo "Rebuild with LIMNORIA_UID and LIMNORIA_GID set to its owner on the host:" >&2
    echo "    LIMNORIA_UID=\$(id -u) LIMNORIA_GID=\$(id -g) docker compose build" >&2
    ls -ldn "$HOME" >&2 || true
    exit 1
fi
mkdir -p backup conf data logs plugins

if [ -z "${LIMNORIA_CONFIG:-}" ]; then
    set -- ./*.conf
    if [ "$#" -eq 1 ] && [ -f "$1" ]; then
        LIMNORIA_CONFIG=$1
    else
        echo "Expected exactly one *.conf file in $HOME or LIMNORIA_CONFIG set." >&2
        echo "Create a configuration with: docker compose run --rm bot supybot-wizard" >&2
        exit 1
    fi
fi

exec supybot "$LIMNORIA_CONFIG"
