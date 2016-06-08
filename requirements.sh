#!/bin/bash

set -e

# Start with: ,conda-env python=3.4

conda install \
    'ipython-notebook<3' \
    docutils=0.12 \
    jinja2=2.8 \
    pygments=2.1.3 \
    pytz \
    pyyaml \

pip install \
    bottle==0.12.9 \
    https://github.com/brandon-rhodes/contingent/archive/master.zip \

