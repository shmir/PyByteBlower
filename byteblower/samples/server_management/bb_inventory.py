"""
    Lists all ports on a ByteBlower Server

    This script needs two arguments to run:
        The ByteBlower server you'd like to get info from and its meeting point address.

"""

from byteblower.byteblowerll import byteblower
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

print('# Server')
service_info = server.ServiceInfoGet()
print('Type: {}'.format(service_info.TypeGet()))
print('Series: {}'.format(service_info.SeriesGet()))
print('Version: {}'.format(service_info.VersionGet()))
print('Machine ID: {}'.format(service_info.MachineIDGet()))

print("# Ports")
for p in server.PhysicalInterfacesGet():
    print('\tId: {}'.format(p.IdGet() + 1))
    print('\tPort: {}'.format(p.NameGet()))
    if p.ByteBlowerInterfaceCountGet() > 1:
        for i in p.ByteBlowerInterfaceGet():
            print('\t\tId: {}'.format(i.PortIdGet()))
            print('\t\tPort: {}'.format(i.NameGet()))

print("# Endpoints")
for d in meetingpoint.DeviceListGet():
    print('Endpoint: {}'.format(d.DeviceInfoGet().GivenNameGet()))
    print('Type: {}'.format(d.DeviceInfoGet().TypeGet()))
    print('Description: {}'.format(d.DeviceInfoGet().DescriptionGet()))
    network_info = d.DeviceInfoGet().NetworkInfoGet()
    print('IPv4: {}'.format(network_info.IPv4Get()))
