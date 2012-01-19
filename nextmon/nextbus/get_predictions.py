#!/usr/bin/python
import os
import sys

if __name__ == '__main__':
    cur_file = os.path.abspath(__file__)
    django_dir = os.path.abspath(os.path.join(os.path.dirname(cur_file), '..'))
    sys.path.append(django_dir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import datetime

import nextbus.models
import nextbus.api

def gather_predictions(agency):
    routes = nextbus.models.NBRoute.objects.filter(agency__name=agency, )
    routes_stops = []

    route_dict = {}
    stop_dict = {}
    for route in routes:
        route_dict[route.tag] = route
        if route.existent:
            for stop in route.stops.all():
                if stop.tag in stop_dict:
                    assert stop == stop_dict[stop.tag]
                stop_dict[stop.tag] = stop
                if stop.existent and stop.enabled:
                    routes_stops.append((route.tag, stop.tag, ))

    nb = nextbus.api.NextBus(agency)
    predictions = nb.predictions(routes_stops)
    cycle = nextbus.models.PredictionCycle()
    cycle.save()
    
    for prediction in predictions:
        route = route_dict[prediction.attrib['routeTag']]
        stop = stop_dict[prediction.attrib['stopTag']]
        directions = prediction.findall('direction')
        assert len(directions) <= 1, "Found more than one direction at a stop. This is abnormal (at least for Saferide)."
        dj_pred = nextbus.models.NBPrediction(
            route=route,
            stop=stop,
            cycle=cycle,
        )
        if len(directions) == 0:
            dj_pred.dir_tag = None
            dj_pred.seconds = None
            dj_pred.arrival_time = None
        else:
            direction = directions[0]
            assert len(direction) > 0, "No predictions found for %s on %s" % (route, stop, )
            dj_pred.seconds = 999999999999
            dj_pred.arrival_time = None
            dj_pred.dirTag = None
            for prediction in direction:
                seconds = int(prediction.attrib['seconds'])
                if seconds < dj_pred.seconds:
                    dj_pred.dir_tag = prediction.attrib['dirTag']
                    dj_pred.seconds = seconds
                    dj_pred.arrival_time = datetime.datetime.fromtimestamp(int(prediction.attrib['epochTime'])/1000)
        dj_pred.save()

if __name__ == '__main__':
    for agency in nextbus.models.NBAgency.objects.all():
        gather_predictions(agency.name)

