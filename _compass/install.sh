#!/bin/bash
# install.sh - installs Compass under a "./Gem" directory

if ! which gem >/dev/null ;then
    cat >&2 <<EOF
No "gem" command; please "sudo aptitude install rubygems1.8" or "ruby1.9.1"
EOF
    exit 1
fi
BASE=$(dirname $(readlink -f $(which "$0")))
cd $BASE  # the directory where this "install.sh" lives
gem install -i Gem compass-susy-plugin
