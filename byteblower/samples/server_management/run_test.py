
from __future__ import print_function # Only Python 2.x
import subprocess
import time

from byteblower.byteblowerll import byteblower

server_ip = '10.113.137.22'

bb_clt = 'C:/Program Files (x86)/Excentis/ByteBlower-CLT-v2/ByteBlower-CLT.exe'
project = 'C:/TestShell/BB/CloudShellPoC.bbp'
scenario = 'CloudShellPoC'
output = 'C:/temp/bb/run17'
bb_cmd = [bb_clt, '-project', project, '-scenario', scenario, '-output', output]

bb = byteblower.ByteBlower.InstanceGet()
server = bb.ServerAdd(server_ip)
port_45 = server.PortCreate('trunk-1-45')

popen = subprocess.Popen(bb_cmd, stdout=subprocess.PIPE, universal_newlines=True)
result = port_45.ResultGet()
history = port_45.ResultHistoryGet()
# for stdout_line in iter(popen.stdout.readline, ""):
# print(stdout_line)
for _ in range(0, 100):
    result.Refresh()
    history.Refresh()
    all = result.RxAllGet()
    print('ResultGet ByteCountGet = {}'.format(all.ByteCountGet()))
    interval = history.IntervalLatestGet()
    rx_data = interval.RxAllGet()
    print('IntervalGet ByteCountGet = {}'.format(rx_data.ByteCountGet()))
    time.sleep(1)

popen.stdout.close()
return_code = popen.wait()
if return_code:
    raise subprocess.CalledProcessError(return_code, bb_cmd)

