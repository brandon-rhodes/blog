#!/bin/bash

set -e

# Start with: ,conda-env python=3.5

conda install \
    mpmath=0.19 \
    notebook=5.0.0 \
    python=3.6 \
    sympy=1.1.1 \

pip install \
    CommonMark==0.7.5 \
    bottle==0.11.6 \
    docutils==0.11 \
    feedgen==0.6.1 \
    jinja2==2.7.3 \
    notedown==1.5.1 \
    pandoc-attributes==0.1.7 \
    pygments==1.6 \
    pytz \
    pyyaml==3.10 \
    https://github.com/brandon-rhodes/contingent/archive/master.zip \

