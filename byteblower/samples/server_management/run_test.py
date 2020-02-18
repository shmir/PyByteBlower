
from __future__ import print_function # Only Python 2.x
import subprocess
import time
import io
import sys

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
trigger = port_45.RxTriggerBasicAdd()
history = trigger.ResultHistoryGet()

traffic_running = False
filename = output + '/test.log'
with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
    popen = subprocess.Popen(bb_cmd, stdout=writer, stderr=writer, universal_newlines=True)
    while popen.poll() is None:
        output = reader.read()
        sys.stdout.write(output)
        if 'StartTraffic' in output:
            traffic_running = True
        elif 'StopTraffic' in output:
            traffic_running = False
        if traffic_running:
            history.Refresh()
            cumulative = history.CumulativeLatestGet()
            interval = history.IntervalLatestGet()
            print('Cumulative ByteCountGet = {}'.format(cumulative.ByteCountGet()))
            print('Interval ByteCountGet = {}'.format(interval.ByteCountGet()))
        time.sleep(1)
    output = reader.read()
    sys.stdout.write(output)

return_code = popen.wait()
if return_code:
    raise subprocess.CalledProcessError(return_code, bb_cmd)
