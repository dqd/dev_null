# Limnoria IRC bot on the latest Python 3, Debian based.
FROM python:3-slim

ARG UID=1000
ARG GID=1000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*

# Limnoria with its optional dependencies, plus what the bundled plugins need.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Unprivileged user. /data holds the configuration, state and plugins.
RUN groupadd --gid "$GID" bot \
    && useradd --uid "$UID" --gid "$GID" --create-home --shell /usr/sbin/nologin bot \
    && mkdir /data \
    && chown bot:bot /data

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod 0755 /usr/local/bin/entrypoint.sh

USER bot
WORKDIR /data
VOLUME ["/data"]

ENTRYPOINT ["entrypoint.sh"]
