from lxml import etree, html
from io import StringIO, BytesIO
import urllib.request
from csv import reader


# https://ign-esp.maps.arcgis.com/apps/webappviewer/index.html?id=0e18d39679a54e3cb4a3b434b31a743b
# https://ign-esp.maps.arcgis.com/apps/webappviewer3d/index.html?id=7c1fe45540bb4ac0a5b7d6bcb3a96bfc


def savexml(query):
  response = urllib.request.urlopen(query)
  res = response.read()
  root = etree.fromstring(res, base_url=query)
  tree = etree.fromstring(res)
  with open('boxtree.xml', 'wb') as doc:
      doc.write(etree.tostring(tree, pretty_print=True))
  return root


class quakeml(object):
    """ Function that parses QuakeML language from XML file"""

    def __init__(self, filename):
        super()
        book = open(filename, 'r')
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(book, parser)
        self.root = tree.getroot()
        self.EV = []
        self.clean_xml_ns()

    def parse_quakeml(self):
        for ev1 in self.root:
            for ev2 in ev1.getchildren():
                event = {}
                _mag = ev2.find('origin')
                _depth = _mag.find('depth')
                event['depth'] = _depth.find('value').text
                _lon = _mag.find('longitude')
                event['lon'] = _lon.find('value').text
                _lat = _mag.find('latitude')
                event['lat'] = _lat.find('value').text

                _mag = ev2.find('magnitude')
                mag = _mag.find('mag')
                event['val'] = mag.find('value').text
                self.EV.append(event)

    def get_data(self):
        yield self.EV

    def clean_xml_ns(self):
        for element in self.root.getiterator():
            if isinstance(element, etree._Comment):
                continue
            element.tag = etree.QName(element).localname
            etree.cleanup_namespaces(self.root)


def parsecsv():
# read csv file as a list of lists
with open(filename, 'r', encoding="utf-8") as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj, delimiter=';')
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    print(list_of_rows[0])
    #print(list_of_rows)
