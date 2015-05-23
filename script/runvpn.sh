#!/bin/bash
# FileName:   runvpn.sh
# Author:     Chen Yanfei
# @contact:   fasionchan@gmail.com
# @version:   $Id$
#
# Description:
#
# Changelog:
#
#

SCRIPT_DIR="$(readlink -f "$(dirname "$0")/../script")"
TOOLKIT_DIR="$(readlink -f "$SCRIPT_DIR/../toolkit")"
CONF_DIR="$(readlink -f "$SCRIPT_DIR/../config/toolkit")"
UDPTUN_PY="$TOOLKIT_DIR/udptun.py"

source "$CONF_DIR/udptun.env"
sudo python $UDPTUN_PY -m client -a vpn.icampus.us:18800 -u $NODE -k $KEY
