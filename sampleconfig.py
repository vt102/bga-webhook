#!/usr/bin/env python3

import atexit
from datetime import datetime
import json
import os
import signal

debug = True
statefile = '/var/tmp/bga-webhook/state.json'

games = [
    {
        'bga': 'https://boardgamearena.com/6/stoneage?table=123456789',
        'discord': ('https://discord.com/api/webhooks/1234567890123456789/'
                    'abcdefghijklmnopqrstuvwXYZ0123456789ABCDEFGHIJKLMNOPQ'
                    'RSTUVWXYZ098765?thread_id=1234567890123456789'),
        'name': 'Test game 1'

    },
]

players = [
    {
        'bga': 'Bob',
        'discord': '123456789012345678'
    },
    {
        'bga': 'Sue',
        'discord': '876543210987654321'
    },
]

###
### Change nothing below this line
###

assert isinstance(debug, bool)
assert isinstance(statefile, str)
assert isinstance(games, list)
assert isinstance(players, list)

if not os.path.exists(statefile):
    with open(statefile, 'w+') as writer:
        json.dump({}, writer)
with open(statefile, 'r') as reader:
    state = json.load(reader)

    for game in games:
        if game['bga'] not in state:
            state[game['bga']] = {}
            state[game['bga']]['player'] = None
            state[game['bga']]['timestamp'] = datetime.now()

def on_exit():
    with open(statefile, 'w+') as writer:
        json.dump(state, writer, default=str)
atexit.register(on_exit)
signal.signal(signal.SIGTERM, on_exit)
signal.signal(signal.SIGINT, on_exit)
