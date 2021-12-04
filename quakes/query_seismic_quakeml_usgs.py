import urllib.request
from lxml import *

# name spaces employed at USGS need to find a way to parse these from the file.
ns = {
    "q": "http://quakeml.org/xmlns/quakeml/1.2",
    "d": "http://quakeml.org/xmlns/bed/1.2",
    "catalog": "http://anss.org/xmlns/catalog/0.1",
    "tensor": "http://anss.org/xmlns/tensor/0.1"
    }


def parse_usgs_xml(filepath):
    #
    # you can import xml from online:
    url = 'https://earthquake.usgs.gov/realtime/product/phase-data/us20007z6r/us/1481210600040/quakeml.xml'
    response = urllib.request.urlopen(url)
    xmlstring = response.read()
    xroot = ElementTree.fromstring(xmlstring)

    xeventParameters = xroot.findall('d:eventParameters', ns)
    #
    for ep in xeventParameters:
        xevents = ep.findall('d:event', ns)
        print("Found %d events." % (len(xevents)))
    #
    events = []
    #
    i = 0
    for xev in xevents:
        # build an event dictionary
        ev = {}
        ev['eventid'] = xev.attrib["{http://anss.org/xmlns/catalog/0.1}eventid"]
        ev['publicID'] = xev.attrib['publicID']
        ev['eventsource'] = xev.attrib['{http://anss.org/xmlns/catalog/0.1}eventsource']
        ev['datasource'] = xev.attrib['{http://anss.org/xmlns/catalog/0.1}datasource']
        ev['preferredOriginID'] = xev.find("d:preferredOriginID", ns).text
        ev['preferredMagnitudeID'] = xev.find("d:preferredMagnitudeID", ns).text
        #
        mags = parse_magnitudes(xev)
        picks = parse_picks(xev)
        amplitudes = parse_amplitudes(xev)
        #
        preforigin = ev['preferredOriginID'].lower().split("/")[-1]
        xorigins = xev.findall('d:origin',ns)
        origins = parse_origins(xev)
        pxorigin = xev[0]
        n = 0
        for xorigin in xorigins:
            anOrigin = origins[n]
            pID = anOrigin['publicID'].lower().split("/")[-1]
            if(pID == preforigin):
                pxorigin = xorigin
            n += 1
        #
        arrivals = parse_arrivals(pxorigin)
        #
        events.append({
            'eventInfo': ev,
            'origins': origins,
            'magnitudes': mags,
            'picks': picks,
            'arrivals': arrivals,
            'amplitudes': amplitudes
            })
        #
        i += 1
        #
        print("parsed %d events." % (i))
        #
    return events


url = "https://quake.ethz.ch/quakeml/Documents?action=AttachFile&do=get&target=quakeml-1.2-RT.tgz"
response = urllib.request.urlopen(url)
text = response.read()
#with open('boxtree.tgz', 'wb') as w:
#    w.write(text)

#import tarfile
#import gzip
#with gzip.open('boxtree.tgz', 'rb') as f:
#    file_content = f.read()
#    with open('boxtree.tar', 'wb') as w:
#        w.write(text)
#    my_tar = tarfile.open('boxtree.tar')
#    my_tar.extractall('./data') # specify which folder to extract to
#    my_tar.close()
