#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pytz
import subprocess
import sys
from dataclasses import dataclass

from bottle import SimpleTemplate

ISO = '%Y-%m-%dT%H:%M:%SZ'
MILES_PER_METER = 0.000621371

def main(argv):
    with open('test.template.html') as f:
        content = f.read()

    # xml = subprocess.check_output('~/usr/lib/garmin/fit2tcx',
    #                               '~/Downloads/96270558.FIT')
    xml = open('/home/brandon/tmp.tcx').read()
    xml = xml.replace(
        'xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"',
        '',
    )
    import xml.etree.ElementTree as etree
    x = etree.fromstring(xml)

    c = []

    icons = []
    next_mile = 0
    splits = []

    trackpoints = list(parse_trackpoints(x))

    from timezonefinder import TimezoneFinder
    tf = TimezoneFinder()
    name = tf.timezone_at(lng=trackpoints[0].longitude_degrees,
                          lat=trackpoints[0].latitude_degrees)
    tz = pytz.timezone(name)
    utc = pytz.utc
    print(tz)
    for p in trackpoints:
        p.time = utc.localize(p.time).astimezone(tz)

    route = [[p.latitude_degrees, p.longitude_degrees] for p in trackpoints]
    mileposts = list(compute_mileposts(trackpoints))

    icons = [
        {
            'lat': p.latitude_degrees,
            'lon': p.longitude_degrees,
            'label': '{} mi<br>{:%-I:%M} {}'.format(
                p.distance_meters * MILES_PER_METER,
                p.time,
                p.time.strftime('%p').lower(),
            ),
        }
        for p in mileposts
    ]

    def compute_splits(trackpoints, mileposts):
        previous = trackpoints[0]
        for milepost in mileposts + [trackpoints[-1]]:
            meters = milepost.distance_meters - previous.distance_meters
            duration = milepost.time - previous.time
            yield Split(
                start = previous.time,
                end = milepost.time,
                duration = duration,
                meters = meters,
                mph = mph(meters, duration),
            )
            previous = milepost

    splits = list(compute_splits(trackpoints, mileposts))

    meters = trackpoints[-1].distance_meters
    miles = meters * MILES_PER_METER
    duration = trackpoints[-1].time - trackpoints[0].time
    #mph = miles / duration.total_seconds() * 60 * 60

    template = SimpleTemplate(content)
    content = template.render(
        duration=duration,
        icons=json.dumps(icons),
        route=json.dumps(route),
        miles=miles,
        mph=mph(meters, duration),
        splits=splits,
        start=trackpoints[0].time,
    )

    print(splits)

    #sys.stdout.write(content)
    with open('test.html', 'w') as f:
        f.write(content)

@dataclass
class Trackpoint(object):
    time: dt.datetime
    altitude_meters: float = 0.0
    distance_meters: float = 0.0
    latitude_degrees: float = 0.0
    longitude_degrees: float = 0.0

@dataclass
class Split(object):
    start: dt.datetime
    end: dt.datetime
    duration: dt.timedelta
    meters: float = 0.0
    mph: float = 0.0

def mph(meters, duration):
    return meters * MILES_PER_METER / duration.total_seconds() * 60 * 60

def parse_trackpoints(document):
    elements = document.findall('.//Trackpoint')
    for t in elements:
        p = t.find('Position')
        yield Trackpoint(
            time = dt.datetime.strptime(t.find('Time').text, ISO),
            altitude_meters = float(t.find('AltitudeMeters').text),
            distance_meters = float(t.find('DistanceMeters').text),
            latitude_degrees = float(p.find('LatitudeDegrees').text),
            longitude_degrees = float(p.find('LongitudeDegrees').text),
        )

def compute_mileposts(datapoints):
    datapoints = list(datapoints)
    next_mile = 1
    previous_time = 0
    previous_miles = 0
    for point in datapoints:
        d = point
        miles = d.distance_meters * MILES_PER_METER
        while miles > next_mile:
            fraction = (next_mile - previous_miles) / (miles - previous_miles)
            delta = d.time - previous_time
            yield Trackpoint(
                time = previous_time + delta * fraction,
                distance_meters = next_mile / MILES_PER_METER,
                altitude_meters = interpolate(
                    previous_point.altitude_meters,
                    point.altitude_meters,
                    fraction,
                ),
                latitude_degrees = interpolate(
                    previous_point.latitude_degrees,
                    point.latitude_degrees,
                    fraction,
                ),
                longitude_degrees = interpolate(
                    previous_point.longitude_degrees,
                    point.longitude_degrees,
                    fraction,
                ),
            )
            print(fraction)
            next_mile += 1
        previous_time = d.time
        previous_miles = miles
        previous_point = point

def interpolate(a, b, fraction):
    return a + (b - a) * fraction

# def compute_splits(mileposts):
#

if __name__ == '__main__':
    main(sys.argv[1:])
