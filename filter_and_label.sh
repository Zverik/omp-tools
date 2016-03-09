#!/bin/bash
set -e -u
mkdir -p duplicate
mkdir -p labelled
LAST=
for i in 1*.png; do
  SZ=$(stat -f%z "$i")
  if [ "$LAST" == "$SZ" ]; then
    mv "$i" duplicate
  else
    LAST="$SZ"
    LABEL=$(perl -e '$ARGV[0] =~ /(\w\w)(\w\w)(\w\w)-(\w\w)(\w\w)/; ($m, $d, $h, $mm) = ($2, $3, $4, $5); $h+=3; if($h > 23) { $h-=24; $d++; }; if($d==30) { $d=1; $m++}; printf "%02d.%02d %02d:%02d", $d, $m, $h, $mm' "$i")
    echo "$i → $LABEL"
    convert "$i" -gravity southeast -fill blue -font "pt-sans" -pointsize 40 -annotate +10+0 "$LABEL" "labelled/$i"
  fi
done
