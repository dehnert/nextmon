#!/usr/bin/python
import os
import sys

if __name__ == '__main__':
    cur_file = os.path.abspath(__file__)
    django_dir = os.path.abspath(os.path.join(os.path.dirname(cur_file), '..'))
    sys.path.append(django_dir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import collections

import nextbus.models
import nextbus.api

def sync_agencies():
    for agency in nextbus.models.NBAgency.objects.all():
        print "\nAgency: %s" % (agency, )
        sync_agency(agency.name)

def sync_agency(agency):
    counter = collections.defaultdict(lambda: 0)

    nb = nextbus.api.NextBus(agency)
    nb_routes = nb.query('routeConfig').findall('route')
    nb_dict = {}
    for nb_route in nb_routes:
        nb_dict[nb_route.attrib['tag']] = nb_route

    dj_agency = nextbus.models.NBAgency.objects.get(name=agency)
    dj_routes = nextbus.models.NBRoute.objects.filter(agency=dj_agency)
    dj_dict = {}
    for dj_route in dj_routes:
        dj_dict[dj_route.tag] = dj_route
    dj_stops_dict = {}
    for dj_stop in dj_agency.nbstop_set.all():
        dj_stops_dict[dj_stop.tag] = dj_stop

    for tag, nb_route in nb_dict.items():
        if tag in dj_dict:
            if dj_dict[tag].existent:
                counter['route_kept'] += 1
            else:
                dj_dict[tag].existent = True
                dj_dict[tag].save()
                print "Readd:\troute %s" % (tag, )
                counter['route_readd'] += 1
        else:
            dj_route = nextbus.models.NBRoute(
                agency=dj_agency,
                tag=tag,
                title=nb_route.attrib['title'],
            )
            dj_route.save()
            dj_dict[tag] = dj_route
            print "Add:\troute %s" % (tag, )
            counter['route_add'] += 1
        sync_stops(counter, nb_route, dj_agency, dj_dict[tag], dj_stops_dict)

    for dj_route in dj_routes:
        if tag in nb_dict:
            pass
        else:
            dj_route.existent = False
            dj_route.save()
            print "Delete:\troute %s" % (tag, )
            counter['route_del'] += 1

    for name, val in sorted(counter.items()):
        print "%12s\t%4d" % (name, val, )

def sync_stops(counter, nb_route, dj_agency, dj_route, dj_all_stops, ):
    nb_stops = nb_route.findall('stop')
    nb_dict = {}
    for nb_stop in nb_stops:
        tag = nb_stop.attrib['tag']
        nb_dict[tag] = nb_stop
        if tag in dj_all_stops:
            dj_stop = dj_all_stops[tag]
            if dj_stop in dj_route.stops.all():
                if dj_stop.existent:
                    counter['stop_kept'] += 1
                else:
                    dj_stop.existent = True
                    dj_stop.save()
                    print "Reenable:\tstop %s" % (tag, )
                    counter['stop_reenable'] += 1
            else:
                dj_route.stops.add(dj_all_stops[tag])
                print "Add:\tstop %s to route %s" % (tag, dj_route.tag, )
                counter['stop_add'] += 1
        else:
            dj_stop = nextbus.models.NBStop(
                agency=dj_agency,
                tag=tag,
                title=nb_stop.attrib['title'],
            )
            dj_stop.save()
            dj_all_stops[tag] = dj_stop
            dj_route.stops.add(dj_stop)
            print "Create:\tstop %s on route %s" % (tag, dj_route.tag, )
            counter['stop_create'] += 1

    for dj_stop in dj_route.stops.all():
        if dj_stop.tag in nb_dict:
            pass
        else:
            dj_route.stops.remove(dj_stop)
            print "Remove:\tstop %s on route %s" % (dj_stop.tag, dj_route.tag, )
            counter['stop_remove'] += 1

if __name__ == '__main__':
    sync_agencies()
