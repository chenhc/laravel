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
    echo 'usage: init_ilive_schema.sh database user password'
    exit 1
fi

DATABASE="$1"
USER_OPT="-u$2"
PASSWORD_OPT="-p$3"

SQLFILE='ilive.sql'

mysql $USER_OPT $PASSWORD_OPT <<EOF
DROP DATABASE IF EXISTS \`$DATABASE\`;
CREATE DATABASE \`$DATABASE\`;
USE \`$DATABASE\`;
$(cat $SQLFILE)
EOF
