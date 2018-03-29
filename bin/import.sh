#!/bin/bash

set -e

function resize {
    convert "$1" -resize 600x600 -quality 90 "$2"
}

X=$HOME/dropbox/personal/Photos/darktable_exported/

resize $X/100MSDCF-DSC00118.jpg static/brandon/2018/twiddler.jpg
resize $X/100MSDCF-DSC00117.jpg static/brandon/2018/cables.jpg
