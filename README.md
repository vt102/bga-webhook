# bga-webhook

A python script that will scrape the Board Game Area game's page for
whose turn it is, then allow you to take action on it.  Currently, it
just fires a Discord webhook.

## Instructions

Rename `sampleconfig.py` to `config.py`.

Inside `config.py`, you will need to include information about the BGA
games you are watching, and the Discord webhooks to use for alerting.

You will also need to provide an association from the BGA name of a
player, and their Discord ID.

No webhooks will be fired while `debug = True`.  Change to False when you
are ready for webhooks to be fired.
