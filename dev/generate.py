#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import subprocess
import sys
from dataclasses import dataclass

ISO = '%Y-%m-%dT%H:%M:%SZ'

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
    print(x)

    c = []
    j = c

    icons = []
    next_mile = 0
    splits = []

    trackpoints = x.findall('.//Trackpoint')
    datapoints = list(parse_trackpoints(trackpoints))
    print(list(compute_mileposts(datapoints)))

    for t in x.findall('.//Trackpoint'):
        time = dt.datetime.strptime(t.find('Time').text, ISO)
        alt = float(t.find('AltitudeMeters').text)
        distance = float(t.find('DistanceMeters').text)
        p = t.find('Position')
        lat = float(p.find('LatitudeDegrees').text)
        lon = float(p.find('LongitudeDegrees').text)
        c.append([lat, lon])
        miles = distance * 0.000621371
        if miles > next_mile:
            icons.append({
                'lat': lat,
                'lon': lon,
                'label': '{} mi'.format(next_mile),
            })
            next_mile += 1
            splits.append(next_mile)
        # TODO: DistanceMeters

    content = content.replace('$LATLNGS', json.dumps(j))
            #print(t)
    content = content.replace('$ICONS', json.dumps(icons))

    print(splits)

    #sys.stdout.write(content)
    with open('test.html', 'w') as f:
        f.write(content)

@dataclass
class Trackpoint(object):
    time: dt.datetime
    altitude_meters: float
    distance_meters: float
    latitude_degrees: float
    longitude_degrees: float

def parse_trackpoints(trackpoints):
    for t in trackpoints:
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
    for d in datapoints:
        miles = d.distance_meters * 0.000621371
        if miles > next_mile:
            # TODO: what if it jumped ahead multiple miles?
            # print('A', next_mile - previous_miles)
            # print('B', miles - previous_miles)
            fraction = (next_mile - previous_miles) / (miles - previous_miles)
            delta = d.time - previous_time
            yield previous_time + delta * fraction, next_mile
            print(fraction)
            next_mile += 1
        previous_time = d.time
        previous_miles = miles

# def compute_splits(mileposts):
#

if __name__ == '__main__':
    main(sys.argv[1:])
