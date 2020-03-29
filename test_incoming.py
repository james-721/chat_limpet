import zlib
import zmq
import simplejson
import sys
import time
import pprint
import math

pp = pprint.PrettyPrinter(indent=4)

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
                try:
                    star_system = __json['message']['StarSystem']
                    star_pos = __json['message']['StarPos']
                    timestamp = __json['header']['gatewayTimestamp']
                    softwarename = __json['header']['softwareName']
                    distances = distance_finder(star_pos)
                    print(f'{timestamp} {star_system} {distances[1]}')
                except:
                    print('data missing')
                sys.stdout.flush()
                
        except zmq.ZMQError as e:
            print ('ZMQSocketException: ' + str(e))
            sys.stdout.flush()
            subscriber.disconnect(__relayEDDN)
            time.sleep(5)
        time.sleep(.1)

if __name__ == '__main__':
    main()