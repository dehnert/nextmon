import urllib
from lxml import etree

from StringIO import StringIO

base_url = "http://webservices.nextbus.com/service/publicXMLFeed"

enable_debug = True
enable_debug = False

def debug(string):
    if enable_debug:
        print string

def query(command, agency, args):
    all_args = [
        ('command', command, ),
        ('a', agency, ),
    ]
    all_args.extend(args)
    data = urllib.urlencode(all_args)
    url = base_url + '?' + data
    debug("URL for %s: %s" % (command, url, ))
    fd = urllib.urlopen(base_url + '?' + data)
    result = etree.parse(fd).getroot()
    error = result.find('./Error')
    if error is not None:
        raise RuntimeError('NextBus call failed: %s' % (error.text, ))
    return result

class NextBus(object):
    def __init__(self, agency):
        self.agency = agency

    def query(self, command, args={}):
        return query(command, self.agency, args)

    def predictions(self, routes_stops, ):
        args = [('stops', '%s|null|%s' % (route, stop, ), ) for route, stop in routes_stops]
        return self.query('predictionsForMultiStops', args)
