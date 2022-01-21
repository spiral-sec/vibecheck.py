#!/usr/bin/sh

{
    python3 -m venv .venv && \
    . .venv/bin/activate ;
    } || {
    echo "Could not set up virtualenv, please install python3.9-venv" && \
    exit 1 ; \
}

{
    pip install pyinstaller && \
        pip install -r requirements.txt ; } || {
    echo "Could not install pip modules" && exit 1 ; }

pyinstaller -F vibecheck.py && \
    staticx --strip -l /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 dist/vibecheck vibecheck
