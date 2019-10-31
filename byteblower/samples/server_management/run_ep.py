
from __future__ import print_function # Only Python 2.x
import subprocess
import rpyc

ep_ip = '10.113.137.13'

mp_ip = '192.168.0.3'
ep_clt = 'C:/Users/PC1xx2G/Desktop/ByteBlowerWirelessEndpoint/$PLUGINSDIR/BBWEP/byteblower-wireless-endpoint.exe'
ep_cmd = [ep_clt, mp_ip]

c = rpyc.classic.connect(ep_ip)

popen = c.modules.subprocess.Popen(ep_cmd, stdout=c.modules.subprocess.PIPE, universal_newlines=True)
for stdout_line in iter(popen.stdout.readline, ""):
    print(stdout_line)
popen.stdout.close()
return_code = popen.wait()
if return_code:
    raise subprocess.CalledProcessError(return_code, ep_cmd)
