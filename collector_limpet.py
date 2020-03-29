#!/home/robotnik/opt/python-3.8.1/bin/python3

import zlib
import zmq
import simplejson
import sys
import time
from datetime import date, time, datetime
from red_squid import red_squid
from statics import colonia_coords
from common_functions import distance_finder

#Config
__relayEDDN = 'tcp://eddn.edcd.io:9500'
__timeoutEDDN = 600000
context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.setsockopt(zmq.SUBSCRIBE, b"")
subscriber.setsockopt(zmq.RCVTIMEO, __timeoutEDDN)
today = date.today()

#code begins
print(f'COLLECTOR {datetime.now()} Collector Limpet Startup successful - {today}')

while True:
    try:
        subscriber.connect(__relayEDDN)
        while True:
            __message = subscriber.recv()

            if __message == False:
                subscriber.disconnect(__relayEDDN)
                break

            __message = zlib.decompress(__message)
            __json = simplejson.loads(__message)

            # pp.pprint(__json)
            if 'Factions' in __json['message']:
                star_system = __json['message']['StarSystem']
                star_pos = __json['message']['StarPos']
                timestamp = __json['header']['gatewayTimestamp']
                distance = distance_finder(colonia_coords, star_pos)
                #print(f'COLLECTOR {datetime.now()}: {star_system}, {distance}')
                if distance < 2001:
                    print(f'COLLECTOR {datetime.now()}: {star_system}, {distance}')
                    if 'Conflicts' in __json['message']:
                        try:
                            red_squid(__json['message']['Conflicts'], star_system)
                        except:
                            print(f'COLLECTOR {datetime.now()}: ERROR from red_squid.')
            sys.stdout.flush()
    except zmq.ZMQError as e:
        print('ZMQSocketException: ' + str(e))
        sys.stdout.flush()
        subscriber.disconnect(__relayEDDN)
        time.sleep(5)