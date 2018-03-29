#!/bin/bash

set -e

# Start with: ,conda-env python=3.5

conda install \
    python=3.6 \
    notebook=5.0.0 \

pip install \
    CommonMark==0.7.5 \
    docutils==0.11 \
    jinja2==2.7.3 \
    pygments==1.6 \
    pytz \
    pyyaml==3.10 \
    bottle==0.11.6 \
    https://github.com/brandon-rhodes/contingent/archive/master.zip \

