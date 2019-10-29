"""
    Lists all ports on a ByteBlower Server

    This script needs two arguments to run:
        The ByteBlower server you'd like to get info from and its meeting point address.

"""    

import byteblowerll.byteblower as byteblower
import sys

if len(sys.argv) == 3:
    SERVER_ADDRESS = sys.argv[1]
    MEETINGPOINT_ADDRESS = sys.argv[2]
else:
    print("Expected argument: <ByteBlower-server>,  <Meeting point>")
    sys.exit(-1)

bb = byteblower.ByteBlower.InstanceGet()

server = bb.ServerAdd(SERVER_ADDRESS)
meetingpoint = bb.MeetingPointAdd(MEETINGPOINT_ADDRESS)

print("# Ports")
for p in server.PhysicalInterfacesGet():
    print('Port: {}'.format(p.NameGet()))

print("# Trunks")
for p in server.PhysicalInterfacesGet():
    if p.ByteBlowerInterfaceCountGet() > 1:
        for i in p.ByteBlowerInterfaceGet():
            print('Port: {}'.format(i.NameGet()))

print("# Endpoints")
for d in meetingpoint.DeviceListGet():
    print('Endpoint: {}'.format(d.DeviceInfoGet().GivenNameGet()))
