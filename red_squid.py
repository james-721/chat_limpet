#!/home/robotnik/opt/python-3.8.1/bin/python3

import requests
# statics is where I put my tokens.
from statics import redsquid_url, shitlist_sectors, brolist, shitlist, hometeam
from datetime import date, time, datetime

#code begins

def red_squid(conflicts,star_system):
    for conflict in conflicts:
        if conflict['WarType'] == 'civilwar' or conflict['WarType'] == 'war':
            faction1 = conflict['Faction1']['Name']
            faction2 = conflict['Faction2']['Name']
            f1score = str(conflict['Faction1']['WonDays'])
            f2score = str(conflict['Faction2']['WonDays'])
            wartype = conflict['WarType'].upper()
            message = f'**{wartype}** in {star_system}: {faction1}[{f1score}] vs. {faction2}[{f2score}]! '
            if faction1 == hometeam or faction2 == hometeam:
                message = message + f'\n Support **{hometeam}**!'
            elif faction1 in shitlist and faction2 in shitlist:
                message = message + f'\n **BRING SUFFERING TO ALL SIDES!**'
            elif faction1 in brolist and faction2 in brolist:
                message = message + f'\n These factions are both pals.  Stay out of it maybe?'
            elif faction1 in shitlist:
                message = message + f'\n BRING ME THE SOULS OF {faction1.upper()}'
            elif faction2 in shitlist:
                message = message + f'\n I TREASURE THE AGONY OF {faction2.upper()}'
            elif faction1 in brolist:
                message = message + f"\n I WANT TO TASTE {faction2.upper()}'S BONES!"
            elif faction2 in brolist:
                message = message + f'\n I DESIRE THE WAILING OF {faction1.upper()}'
            if star_system in shitlist_sectors:
                message = message + f'\n {star_system} is a designated hellsector, always fight against the controller!'
            myobj = {'content': message}
            x = requests.post(redsquid_url, data=myobj)
            print(f'REDSQUID {datetime.now()}: {message}, ({x})')