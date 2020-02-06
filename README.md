# ByteBlower python package

This is a self contained, pip installable, python package to manage ByteBlower.

It wraps together the MSI ByteBlower [Python API exe installation](https://setup.byteblower.com/software.html) and the
[ByteBlower Python Examples](https://github.com/excentis/ByteBlower_python_examples) into a standard python package.   

**Note: the current version  supports only Windows and Python 2.7.**

## Loading and using the ByteBlower API
To load the ByteBlower API into python use following import statement
`from byteblowerll.byteblower import ByteBlower`

## Samples

This repository contains all public available Python examples on how to use the ByteBlower Python API. 

### Folder structure
- back2back : examples between two ByteBlower ports.
- wireless_endpoint : Examples of using the Wireless Endpoint.
- server_management: No traffic is sent in these examples, they show how to get info from the ByteBlower Server and Meeting point.

### Dependencies
- ByteBlower Python API : http://setup.byteblower.com/software.html#API
- scapy: `pip install scapy`

    warning: when using scapy >2.4.0 on Windows 10: scapy cannot find NPCAP

## Contact
[yoram@ignissoft.com](yoram@ignissoft.com)

## Todo
* restructure to embed all samples under single sub-folder
* add basic unit tests to test the new package (not functionality)
* build setup with restriction for Windows / Python 2.7

## Cheatsheet
* To register EP and get real-time statistics run the following command:

    ByteBlowerWirelessEndpoint.exe chassis-ip
    
    Note that this will open a new CMD window.

* [API documentation]([https://api.byteblower.com/python/])
