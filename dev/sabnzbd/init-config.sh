#!/usr/bin/with-contenv bash
# Seed a config on first start so SABnzbd skips the wizard and uses the fake server.
if [ ! -f /config/sabnzbd.ini ]; then
    cp /defaults-dev/sabnzbd.ini /config/sabnzbd.ini
    chown abc:abc /config/sabnzbd.ini
fi
