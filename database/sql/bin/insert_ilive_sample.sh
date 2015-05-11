#!/bin/bash
# FileName:   init_ilive_schema.sh
# Author:     Chen Yanfei
# @contact:   fasionchan@gmail.com
# @version:   $Id$
#
# Description:
#
# Changelog:
#
#

if [ ! "$#" -eq 3 ]; then
    echo 'usage: insert_ilive_sample.sh database user password'
    exit 1
fi

SQLDIR="$(readlink -f "$(dirname "$0")/..")"

DATABASE="$1"
USER_OPT="-u$2"
PASSWORD_OPT="-p$3"

SQLFILE="$SQLDIR/ilive_sample.sql"

mysql $USER_OPT $PASSWORD_OPT <<EOF
USE \`$DATABASE\`;
$(cat $SQLFILE)
EOF
