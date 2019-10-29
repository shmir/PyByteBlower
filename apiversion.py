from __future__ import print_function
from byteblower.byteblowerll import byteblower

try:
    instance = byteblower.ByteBlower.InstanceGet()
    print("ByteBlower API version: " + instance.APIVersionGet())

except Exception as e:
    print("Caught Exception: " + str(e))
