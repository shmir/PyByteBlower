
from __future__ import print_function # Only Python 2.x
import subprocess
import time

bb_clt = 'C:/Program Files (x86)/Excentis/ByteBlower-CLT-v2/ByteBlower-CLT.exe'
project = 'C:/TestShell/BB/CloudShellPoC.bbp'
scenario = 'CloudShellPoC'
output = 'C:/temp/bb/run6'
bb_cmd = [bb_clt, '-project', project, '-scenario', scenario, '-output', output]

popen = subprocess.Popen(bb_cmd, stdout=subprocess.PIPE, universal_newlines=True)
for stdout_line in iter(popen.stdout.readline, ""):
    print(stdout_line)
popen.stdout.close()
return_code = popen.wait()
if return_code:
    raise subprocess.CalledProcessError(return_code, bb_cmd)
