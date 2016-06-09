#!/bin/bash

set -e

# Start with: ,conda-env python=3.4

conda install \
    'ipython-notebook<3' \
    docutils=0.11 \
    jinja2=2.7.3 \
    pygments=1.6 \
    pytz \
    pyyaml=3.10 \

pip install \
    bottle==0.11.6 \
    https://github.com/brandon-rhodes/contingent/archive/master.zip \

