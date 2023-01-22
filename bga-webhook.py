#!/usr/bin/env python3

from datetime import datetime
import os
import re
import requests

from requests_html import HTMLSession

import config

def send_message(message, server):
    '''Send the given message to the Discord webhook

    Args:
        message: A string to be sent
        server: Discord webhook URL to send message to

    Returns:
        Always returns True; any errors will likely trigger an Exception
    '''

    print(f"Message: {message}")
    print(f"Server: {server}")

    data = {'content': message}

    r = requests.post(url=server, data=data)
    print(r)
    print(r.text)

def bga_whose_turn(bga_url):
    '''Find out whose turn it is on a given BGA game.

    Args:
        bga_url: The URL of the Board Game Area game.

    Returns:
        String of BGA player's name, if found.
        None otherwise.
    '''

    session = HTMLSession()
    r = session.get(bga_url)
    r.html.render()
    f = r.html.find('span#pagemaintitletext')

    assert len(f) == 1

    #span = f[0].html[0:100].replace('<span id="pagemaintitletext"><span style="font-weight:bold;color:#ff0000;">', '')
    matchObj = re.match( r'<span id="pagemaintitletext"><span style="font-weight:bold;color.*;">(.*)</span>.*',
                         f[0].html[0:100],
                         re.M|re.I)

    assert matchObj

    return matchObj.group(1)

def find_discord_id(player):
    '''Return the Discord ID corresponding to the BGA player name.

    Args:
        player: The BGA player name referenced in config.players[]['bga']

    Returns:
        String of the Discord ID referenced in config.players[]['discord']

    Raises:
        RuntimeError: if player can not be found in config data structure
    '''

    for p in config.players:
        if p['bga'] == player:
            return p['discord']
    raise RuntimeError


def run_game(bga_url, discord_url, name):
    '''The primary entrypoint to handle a single game.

    Args:
        bga_url: The URL of the Board Game Area game.
        discord_url: The URL of the Discord webhook used for communication to
                     players about who's turn it is.
        name: The name this game is referred to as; useful for players when
              they get a notification popup.

    Returns:
        Always returns True; any errors will likely trigger an Exception
    '''

    player = bga_whose_turn(bga_url)

    print(bga_url)
    last_player = config.state[bga_url]['player']
    last_timestamp = config.state[bga_url]['timestamp']
    print(f'last_player {last_player}')

    if player != last_player:
        config.state[bga_url]['player'] = player
        config.state[bga_url]['timestamp'] = datetime.now()
        discord_id = find_discord_id(player)
        message = f"<@{discord_id}> it's your turn in {name} "
        if not config.debug:
            send_message(message,
                         discord_url)
        else:
            print(f"Would send to discord: {message}")
        with open(config.statefile, 'w') as writer:
            print(f'writing player {player}')
            writer.write(player)
    else:
        waiting = (datetime.now() -
                   datetime.strptime(last_timestamp,
                            "%Y-%m-%d %H:%M:%S.%f")).total_seconds() / 60
        print(f'No player change for {waiting} minutes.')



if __name__ == '__main__':
    for game in config.games:
        run_game(game['bga'],
                 game['discord'],
                 game['name'])
