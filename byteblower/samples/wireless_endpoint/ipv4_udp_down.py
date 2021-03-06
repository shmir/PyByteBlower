#!/usr/bin/python
""""
This example allows the user to configure a frameblasting flow which transmits data to the wireless endpoint.

ByteBlowerPort --> WirelessEndpoint
"""

from __future__ import print_function
# We want to use the ByteBlower python API, so import it
from byteblower.byteblowerll.byteblower import ByteBlower

# We will use scapy to build the frames, scapy will be imported when needed.


configuration = {
    # Address (IP or FQDN) of the ByteBlower server to use
    'server_address': '10.5.5.144',

    # Interface on the server to create a port on.
    'server_interface': 'nontrunk-2',

    # MAC address of the ByteBlower port which will be generated
    'port_mac_address': '00:bb:01:00:00:01',

    # DHCP or IP configuration for the ByteBlower port
    # if DHCP, use "dhcp"
    'port_ip_address': 'dhcp',
    # if static, use ["ipaddress", "netmask", "gateway"]
    # 'port_ip_address': ['172.16.0.4', '255.255.252.0', '172.16.0.1'],

    # Address (IP or FQDN) of the ByteBlower Meetingpoint to use.  The wireless endpoint *must* be registered
    # on this meetingpoint.
    # Special value: None.  When the address is set to None, the server_address will be used.
    'meetingpoint_address': None,

    # UUID of the ByteBlower WirelessEndpoint to use.  This wireless endpoint *must* be registered to the meetingpoint
    # configured by meetingpoint_address.
    # Special value: None.  When the UUID is set to None, the example will automatically select the first available
    # wireless endpoint.
    # 'wireless_endpoint_uuid': None,
    'wireless_endpoint_uuid': '6d9c2347-e6c1-4eea-932e-053801de32eb',

    # Size of the frame on ethernet level. Do not include the CRC
    'frame_size': 252,

    # Number of frames to send.
    'number_of_frames': 1000,

    # How fast must the frames be sent.  e.g. every 10 milliseconds (=10000000 nanoseconds)
    'interframe_gap_nanoseconds': 10000000,

    'udp_srcport': 4096,
    'udp_dstport': 4096,
}


class Example:
    def __init__(self, **kwargs):
        self.server_address = kwargs['server_address']
        self.server_interface = kwargs['server_interface']
        self.port_mac_address = kwargs['port_mac_address']
        self.port_ip_address = kwargs['port_ip_address']

        self.meetingpoint_address = kwargs['meetingpoint_address']
        if self.meetingpoint_address is None:
            self.meetingpoint_address = self.server_address

        self.wireless_endpoint_uuid = kwargs['wireless_endpoint_uuid']

        self.frame_size = kwargs['frame_size']
        self.number_of_frames = kwargs['number_of_frames']
        self.interframe_gap_nanoseconds = kwargs['interframe_gap_nanoseconds']
        self.udp_srcport = kwargs['udp_srcport']
        self.udp_dstport = kwargs['udp_dstport']

        self.server = None
        self.port = None
        self.meetingpoint = None
        self.wireless_endpoint = None

    def run(self):
        instance = ByteBlower.InstanceGet()
        assert isinstance(instance, ByteBlower)

        # Connect to the server
        self.server = instance.ServerAdd(self.server_address)

        # create and configure the port.
        self.port = self.server.PortCreate(self.server_interface)

        # configure the MAC address on the port
        port_layer2_config = self.port.Layer2EthIISet()
        port_layer2_config.MacSet(self.port_mac_address)

        # configure the IP addressing on the port
        port_layer3_config = self.port.Layer3IPv4Set()
        if type(self.port_ip_address) is str and self.port_ip_address == 'dhcp':
            # DHCP is configured on the DHCP protocol
            dhcp_protocol = port_layer3_config.ProtocolDhcpGet()
            dhcp_protocol.Perform()
        else:
            # Static addressing
            port_layer3_config.IpSet(self.port_ip_address[0])
            port_layer3_config.NetmaskSet(self.port_ip_address[1])
            port_layer3_config.GatewaySet(self.port_ip_address[2])

        print("Created port", self.port.DescriptionGet())

        # Connect to the meetingpoint
        self.meetingpoint = instance.MeetingPointAdd(self.meetingpoint_address)

        # If no WirelessEndpoint UUID was given, search an available one.
        if self.wireless_endpoint_uuid is None:
            self.wireless_endpoint_uuid = self.select_wireless_endpoint_uuid()

        # Get the WirelessEndpoint device
        self.wireless_endpoint = self.meetingpoint.DeviceGet(self.wireless_endpoint_uuid)
        print("Using wireless endpoint", self.wireless_endpoint.DescriptionGet())

        # Now we have the correct information to start configuring the flow.

        # The ByteBlower port will transmit frames to the wireless endpoint,
        # This means we need to create a 'stream' on the ByteBlower port and a Trigger on the WirelessEndpoint

        stream = self.port.TxStreamAdd()
        stream.InterFrameGapSet(self.interframe_gap_nanoseconds)
        stream.NumberOfFramesSet(self.number_of_frames)

        # a stream needs to send some data, so lets create a frame
        # For the frame, we need:
        # - The source MAC address (MAC address of the ByteBlower port in our case)
        # - The destination MAC address.  This can be the MAC address of the WirelessEndpoint, a router, ...
        #   We need to resolve this
        # - The source IP address (The IP address of the ByteBlower port)
        # - The destination IP address (The IP address of the WirelessEndpoint)
        # - The source and destination UDP ports (we configured this on top of this script)
        # - a payload to transmit.

        network_info = self.wireless_endpoint.DeviceInfoGet().NetworkInfoGet()
        wireless_endpoint_ipv4 = network_info.IPv4Get()

        port_mac = self.port.Layer2EthIIGet().MacGet()
        port_layer3_config = self.port.Layer3IPv4Get()
        port_ipv4 = port_layer3_config.IpGet()
        # destination MAC must be resolved, since we do not know whether the WE is available on the local LAN
        destination_mac = port_layer3_config.Resolve(wireless_endpoint_ipv4)

        payload = 'a' * (self.frame_size - 42)

        from scapy.layers.inet import UDP, IP, Ether
        from scapy.all import Raw
        scapy_udp_payload = Raw(payload.encode('ascii', 'strict'))
        scapy_udp_header = UDP(dport=self.udp_dstport, sport=self.udp_srcport)
        scapy_ip_header = IP(src=port_ipv4, dst=wireless_endpoint_ipv4)
        scapy_frame = Ether(src=port_mac, dst=destination_mac) / scapy_ip_header / scapy_udp_header / scapy_udp_payload

        frame_content = bytearray(bytes(scapy_frame))

        # The ByteBlower API expects an 'str' as input for the Frame::BytesSet(), we need to convert the bytearray
        hexbytes = ''.join((format(b, "02x") for b in frame_content))

        frame = stream.FrameAdd()
        frame.BytesSet(hexbytes)

        # The trigger on the WirelessEndpoint counts received frames
        # We need
        # - the source UDP port
        # - the destination UDP port
        # - the originating IP address
        # - the duration of the session.  This can be calculated from the stream settings
        #   interframegap (nanoseconds/frame) * number of frames (frames) + some fixed rollout
        trigger = self.wireless_endpoint.RxTriggerBasicAdd()

        # Add 2 seconds of rollout, so frames in transit can be counted too
        duration_ns = self.interframe_gap_nanoseconds * self.number_of_frames + 2000000000

        trigger.DurationSet(duration_ns)
        trigger.FilterUdpSourcePortSet(self.udp_srcport)
        trigger.FilterUdpDestinationPortSet(self.udp_dstport)
        trigger.FilterSourceAddressSet(port_ipv4)

        # Now all configuration is made
        print(stream.DescriptionGet())
        print(trigger.DescriptionGet())

        # Make sure we are the only users for the wireless endpoint
        self.wireless_endpoint.Lock(True)

        # Upload the configuration to the wireless endpoint
        self.wireless_endpoint.Prepare()

        from time import sleep

        # POSIX timestamp in nanoseconds when the wireless endpoint will start
        starttime_posix = self.wireless_endpoint.Start()
        # Current POSIX timestamp on the meetingpoint
        current_time_posix = self.meetingpoint.TimestampGet()

        time_to_wait_ns = starttime_posix - current_time_posix
        # Wait 200 ms longer, to make sure the wireless endpoint has started.
        time_to_wait_ns += 200000000

        print("Waiting for", time_to_wait_ns / 1000000000.0, "to start the port")
        sleep(time_to_wait_ns / 1000000000.0)

        print("Port will transmit for", duration_ns / 1000000000.0, "seconds")
        self.port.Start()

        print("Waiting for the test to finish")
        sleep(duration_ns / 1000000000.0)

        # get the results from the wireless endpoint
        self.wireless_endpoint.ResultGet()

        self.wireless_endpoint.Lock(False)

        tx_result = stream.ResultGet()
        tx_result.Refresh()
        rx_result = trigger.ResultGet()
        rx_result.Refresh()

        print("Transmitted", tx_result.PacketCountGet(), "packets")
        print("Received   ", rx_result.PacketCountGet(), "packets")

        return {
            'tx': tx_result.PacketCountGet(),
            'rx': rx_result.PacketCountGet()
        }

    def select_wireless_endpoint_uuid(self):
        """
        Walk over all known devices on the meetingpoint.
        If the device has the status 'Available', return its UUID, otherwise return None
        :return: a string representing the UUID or None
        """
        from byteblower.byteblowerll import DeviceStatus_Available

        for device in self.meetingpoint.DeviceListGet():
            # is the status Available?
            if device.StatusGet() == DeviceStatus_Available:
                # yes, return the UUID
                return device.DeviceIdentifierGet()

        # No device found, return None
        return None


if __name__ == '__main__':
    Example(**configuration).run()
