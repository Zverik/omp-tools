#!/bin/bash
set -e -u
P="$(dirname "$0")"
LOCK_FILE="$P/advance_db.lock"
[ -e "$LOCK_FILE" ] && echo "Lock file is present, exiting." && exit 0
touch "$LOCK_FILE"

NIK4="/home/zverik/get-veloroad/nik4/nik4.py"
STYLE="/home/zverik/get-veloroad/osm/osm.xml"
BBOX="45.6259 43.2747 45.8102 43.3911"
STATE="$P/osmosis/state.txt"
STATS_PY="$P/party_stats.py"
STATS="$P/party_stats.csv"

[ ! -e "$STATS" ] && "$STATS_PY" > "$STATS"
SEQ_OLD="$(cat "$STATE" | grep sequence | cut -d= -f2)"
SEQ_OLD="${SEQ_OLD%?}"
"$P/openstreetmap_update"
SEQ_NEW="$(cat "$STATE" | grep sequence | cut -d= -f2)"
SEQ_NEW="${SEQ_NEW%?}"
# Uncomment this line to skip date checking
#SEQ_NEW="notequal"
if [ "$SEQ_OLD" != "$SEQ_NEW" ]; then
	DATE=$(grep timestamp $STATE | sed -e 's/^.*2016-\([0-9][0-9]\)-\([0-9][0-9]\)T\([0-9][0-9]\)\\:\([0-9][0-9]\).*$/16\1\2-\3\4/')
	"$STATS_PY" "$DATE" >> "$STATS"
	for ZOOM in 13 14; do
		mkdir -p "$P/$ZOOM"
		"$NIK4" -b $BBOX -z $ZOOM "$STYLE" "$P/$ZOOM/$DATE.png"
	done
fi

rm -f "$LOCK_FILE"
