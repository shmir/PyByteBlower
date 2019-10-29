#!/usr/bin/python
from byteblower.byteblowerll import byteblower
import requests
import xml.etree.ElementTree as ET



def checkVersions(series, version):
    # url
    url = 'http://10.113.137.22/server/update2.0/latest-versions.xml'
    # creating HTTP response object from given url
    resp = requests.get(url)
    # saving the xml file
    with open('versions.xml', 'wb') as f:
        f.write(resp.content)

    tree = ET.parse('versions.xml')
    root = tree.getroot()
    if root.find('./server[@series="{}"]'.format(series)).attrib['version'] == version:
        print("up to date")
    else:
        print("there is a newer version available")




try:
    bb = byteblower.ByteBlower.InstanceGet()
    bbServer = byteblower.ByteBlower.InstanceGet().ServerAdd("10.113.137.22")

    version = bbServer.ServiceInfoGet().VersionGet()
    series = bbServer.ServiceInfoGet().SeriesGet()

    checkVersions(series, version)




except byteblower.DomainError as e:
    print "Caught DomainError: " + e.getMessage()

except byteblower.TechnicalError as e:
    print "Caught TechnicalError: " + e.getMessage()

except Exception as e:
    print(e.message)
