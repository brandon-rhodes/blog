#!/bin/bash

set -e

# Start with: ,conda-env python=3.6

conda install \
    blas=1.0 \
    cycler=0.10.0 \
    dbus=1.13.2 \
    expat=2.2.5 \
    fontconfig=2.12.6 \
    freetype=2.8 \
    glib=2.56.1 \
    gstreamer=1.14.0 \
    icu=58.2 \
    intel-openmp=2018.0.3-0 \
    jpeg=9b \
    kiwisolver=1.0.1 \
    libgfortran \
    libpng=1.6.34 \
    libxcb=1.13 \
    matplotlib=2.2.2 \
    mkl=2018.0.3 \
    mkl_fft=1.0.1 \
    mkl_random=1.0.1 \
    mpmath=0.19 \
    notebook=5.0.0 \
    numpy \
    numpy=1.14.5 \
    pcre=8.42 \
    pyparsing=2.2.0 \
    pyqt=5.9.2 \
    python=3.6 \
    pytz=2018.4 \
    qt=5.9.5 \
    sip=4.19.8 \
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

