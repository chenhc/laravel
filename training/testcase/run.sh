#!/bin/bash
# FileName:   run.sh
# Author:     Chen Yanfei
# @contact:   fasionchan@gmail.com
# @version:   $Id$
#
# Description:
#
# Changelog:
#
#

TRAINING_DIR="$(readlink -f "$(dirname "$0")/..")"
CASE="$1"
INPUT="$TRAINING_DIR/testcase/$CASE/input"
OUTPUT="$TRAINING_DIR/testcase/$CASE/output"
USER="$2"
EXEC="$3"
EXEC="$(find "$TRAINING_DIR/$USER/$CASE/$EXEC" -executable -type f -print | head -n 1)"

time "$EXEC" < "$INPUT" | diff - "$OUTPUT" && echo "Bingo" || echo "Shit"
