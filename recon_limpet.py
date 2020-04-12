#!/home/robotnik/opt/python-3.8.1/bin/python3

import requests
# statics is where I put my tokens.
from statics import recon_url, shitlist_sectors, brolist, shitlist, hometeam
from datetime import date, time, datetime

def recon_limpet(factions, star_system,owned_by):
    flist = []
    for faction in factions:
        flist.append(faction['Name'])

    if hometeam in flist:
        if star_system in shitlist_sectors:
            message = f"**{star_system} (A Bad System)** \n"
        else:
            message = f"**{star_system}** \n"
        message = f"{message}  System Owner:  {owned_by}\n"

        for faction in factions:
            if faction['Name'] != "Pilots' Federation Local Branch":
                faction_states = ""
                faction_name = faction['Name']
                faction_name = faction_name[0:34]
                faction_inf = round(100 * faction['Influence'], 2)

                if 'ActiveStates' in faction:
                    for astate in faction['ActiveStates']:
                        faction_states = faction_states + ', ' + astate['State']
                    faction_states = faction_states[2:]
                else:
                    faction_states = faction['FactionState']
                message = f"{message}   {faction_name}:  {faction_inf}  {faction_states}\n"
        myobj = {'content': message}
        x = requests.post(recon_url, data=myobj)
        print(f'RECON {datetime.now()}: {star_system}, ({x})')