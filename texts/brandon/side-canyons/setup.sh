#!/bin/bash

convert ~/Downloads/raw-basemap.png \
        -crop '1300x860+260+200' \
        -rotate 270 \
        raw-basemap.png
