"""
    A simple example of NATDiscovery between ByteBlower ports.
    
    This example demonstrates:
       * How to transmit a single packet custom packet.
       * How to capture this packet and dissect it with SCAPI. 
       * Basic ByteBlower configuration.

    We assume that the ByteBlowers are configured through DHCP.
"""

from byteblower.byteblowerll import byteblower
import time

# Minimal config parameters.
# Adapt to your setup.when necessary.
SERVER_ADDRESS = 'byteblower-tutorial-1300.lab.byteblower.excentis.com'

UDP_SRC_PORT = 9000
UDP_DEST_PORT = 1000

WAN_MAC = '00:BB:23:22:55:12'
WAN_BB_INTERFACE = 'nontrunk-1'

LAN_MAC = '00:BB:23:21:55:13'
LAN_BB_INTERFACE = 'trunk-1-45'


# ByteBlower part of the test.
api = byteblower.ByteBlower.InstanceGet()
server = api.ServerAdd(SERVER_ADDRESS)


def create_port(interface, mac_addr):
    port = server.PortCreate(interface)
    l2 = port.Layer2EthIISet()
    l2.AddressSet(mac_addr)

    l3 = port.Layer3IPv4Set()
    l3.ProtocolDhcpGet().Perform()
    return port


wan_port = create_port(WAN_BB_INTERFACE, WAN_MAC)
wan_ip = wan_port.Layer3IPv4Get().IpGet()

lan_port = create_port(LAN_BB_INTERFACE, LAN_MAC)
lan_ip = lan_port.Layer3IPv4Get().IpGet()

# Create the requested packet.
resolved_mac = lan_port.Layer3IPv4Get().Resolve(wan_ip)

stream = lan_port.TxStreamAdd()
bb_frame = stream.FrameAdd()
sc_frame = (Ether(src=LAN_MAC, dst=resolved_mac) / 
            IP(src=lan_ip, dst=wan_ip)/
            UDP(dport=UDP_DEST_PORT, sport=UDP_SRC_PORT)/ 
            'Excentis NAT Discovery packet')

frameContent = bytearray(bytes(sc_frame))
hexbytes = ''.join((format(b, "02x") for b in frameContent))

# Prepare for receiving the response 
cap = wan_port.RxCaptureBasicAdd()
cap.FilterSet('ip and udp')
cap.Start()

# Send a single Probing frame. 
bb_frame.BytesSet(hexbytes)
stream.NumberOfFramesSet(1)
stream.InterFrameGapSet(1000 * 1000)  # 1 millisecond in nanos.

stream.Start()

# Wait for the response.

while True:
    sniffed = cap.ResultGet()
    sniffed.Refresh()

    if sniffed.PacketCountGet() > 0:
        break

    time.sleep(0.01)

cap.Stop()

# Process the response: retrieve all packets.
stream.ResultHistoryGet().Refresh()
out_time = stream.ResultHistoryGet().CumulativeLatestGet().TimestampLastGet()

for f in sniffed.FramesGet():
    data = ''.join([chr(b) for b in f.BufferGet()])
    raw = Ether(data)
    if IP in raw:
        discovered_ip = raw['IP'].getfieldval('src')
        print('Discovered IP: %s' % discovered_ip)
        break
else:       
    print('No packet received')

# Cleanup the Server. The API will implicitly clean up
#  the create objects.
api.ServerRemove(server)
