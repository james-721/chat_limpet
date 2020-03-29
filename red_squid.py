#!/home/robotnik/opt/python-3.8.1/bin/python3

import zlib
import zmq
import simplejson
import sys
import time
import math
import requests
#statics is where I put my tokens.
from statics import redsquid_url

"""
 "  Configuration
"""
__relayEDDN             = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN           = 600000

"""
 "  Start
"""

def distance_finder(input_coords):
    colonia_coords = [-9530.5, -910.28125, 19808.125]
    ogmar_coords = [-9534, -905.28125, 19802.03125]
    colonia_dist = math.sqrt(((colonia_coords[0] - (input_coords[0])) ** 2) + ((colonia_coords[1] - (input_coords[1])) ** 2) + ((colonia_coords[2] - (input_coords[2]))**2))
    ogmar_dist = math.sqrt(((ogmar_coords[0] - (input_coords[0]))**2) + ((ogmar_coords[1] - (input_coords[1]))**2) + ((ogmar_coords[2] - input_coords[2])**2))
    output = [colonia_dist, ogmar_dist]
    return output

def main():
    context     = zmq.Context()
    subscriber  = context.socket(zmq.SUB)
    
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)

    while True:
        try:
            subscriber.connect(__relayEDDN)
            
            while True:
                __message   = subscriber.recv()
                
                if __message == False:
                    subscriber.disconnect(__relayEDDN)
                    break
                
                __message   = zlib.decompress(__message)
                __json      = simplejson.loads(__message)
                
                # call dumps() to ensure double quotes in output
                #pp.pprint(__json)
                if 'Factions' in __json['message']:
                    star_system = __json['message']['StarSystem']
                    star_pos = __json['message']['StarPos']
                    timestamp = __json['header']['gatewayTimestamp']
                    distances = distance_finder(star_pos)
                    if distances[0] < 2001:
                        if 'Conflicts' in __json['message']:
                            for conflict in __json['message']['Conflicts']:
                                if conflict['WarType'] == 'civilwar' or conflict['WarType'] == 'war':
                                    message = 'WAR! in  ' + star_system + ': ' + conflict['Faction1']['Name'] + '['+ str(conflict['Faction1']['WonDays']) + '] vs. ' + conflict['Faction2']['Name'] + '[' + str(conflict['Faction2']['WonDays']) +']! '
                                    myobj = {'content': message}
                                    x = requests.post(redsquid_url, data=myobj)
                                    print(f'{timestamp}: {message}, ({x})')
                time.sleep(1)
                sys.stdout.flush()
                
        except zmq.ZMQError as e:
            print ('ZMQSocketException: ' + str(e))
            sys.stdout.flush()
            subscriber.disconnect(__relayEDDN)
            time.sleep(5)
 
if __name__ == '__main__':
    main()