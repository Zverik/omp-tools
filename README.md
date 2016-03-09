# Online Mapping Party Guide

## Checklist

Before:

[ ] Choose an area depending on number of participants and time.
[ ] Decide on a date. Friday evening is recommended.
[ ] Make a pie.
[ ] Prepare pie for uploading to MapCraft and upload it.

After:

[ ] Create before-after animation
[ ] Create a diff image and HTML
[ ] Filter images and create a progress video


## Diff visualization

Download a region from GIS-Lab or Geofabrik, before the mapping party and after.
Using a mapping party area polygon, cut your region for both dates:

    osmconvert region-before.osm.pbf -B=party.poly -o=party-before.osm
    osmconvert region-after.osm.pbf  -B=party.poly -o=party-after.osm

Install Perl and GD library (for Mac OS, perbrew is recommended). Download [osmdiff.pl](http://wiki.openstreetmap.org/wiki/Osmdiff#Download_and_Hints)
and place [osmgraph.pm](http://wiki.openstreetmap.org/wiki/Osmgraph.pm#Download) into `OSM` directory.
(Actually, it has been uploaded to this repo, so never mind).
Then:

    perl osmdiff.pl party-before.osm party-after.osm party-diff.htm party-diff.png 2048

The latter number is an image width. The default value is 1024.

## Animation

Identify two points of time before and after the mapping party. But if there were remarkable changes during
the event, like adding or removing a landuse polygon covering most of the party area, consider using
images on one side of that change.

    convert -delay 150 before.png after.png -layers Optimize before-after.gif
    convert -delay 150 before.png after.png -crop 1024x700+0+100 +repage -layers Optimize before-after.gif

## Video

Just run `filter_and_label.sh` (requires imagemagick). The current directory must contain timelapse PNG images.
The script will move duplicate images to a separate folder, and then create labelled images in a new directory.

After that:

    ffmpeg -framerate 5 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p party.mp4
