#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys

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

    for t in x.findall('.//Trackpoint'):
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
        # TODO: DistanceMeters

    content = content.replace('$LATLNGS', json.dumps(j))
            #print(t)
    content = content.replace('$ICONS', json.dumps(icons))

    #sys.stdout.write(content)
    with open('test.html', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    main(sys.argv[1:])
