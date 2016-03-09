#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, psycopg2, csv

DATABASE = 'dbname=gis'
BOUND_TABLE = 'grozny'

def query_stats(cur):
	"""Sends queries to the database. Comment out these you don't need."""
	MIDDLE=", {0} where ST_Contains(geom, way) and".format(BOUND_TABLE)
	LENGTH="sum(ST_Length_Spheroid(st_transform(way, 4326),'SPHEROID[\"WGS 84\",6378137,298.257223563]'))/1000 from planet_osm_line" + MIDDLE
	AREA="sum(ST_Area(st_transform(way, 4326), true))/1000000 from planet_osm_polygon" + MIDDLE
	COUNT="count(1) from planet_osm_polygon" + MIDDLE
	POI="count(1) from planet_osm_point" + MIDDLE
	result = []

	cur.execute("select 'highway=track,service;km', {0} highway in ('track', 'service');".format(LENGTH))
	result.append(cur.fetchone())
	cur.execute("select 'highway=footway,path;km', {0} highway in ('pedestrian', 'footway', 'path');".format(LENGTH))
	result.append(cur.fetchone())
	cur.execute("select 'highway roads;km', {0} highway in ('trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'living_street');".format(LENGTH))
	result.append(cur.fetchone())
	cur.execute("select 'railways;km', {0} railway is not null;".format(LENGTH))
	result.append(cur.fetchone())
	cur.execute("select 'waterways;km', {0} waterway is not null;".format(LENGTH))
	result.append(cur.fetchone())
	cur.execute("select 'barriers;km', {0} barrier is not null;".format(LENGTH))
	result.append(cur.fetchone())
	cur.execute("select 'power lines;km', {0} power in ('line', 'minor_line');".format(LENGTH))
	result.append(cur.fetchone())

	cur.execute("select 'farms;km²', {0} landuse in ('farm', 'farmland', 'vineyard', 'orchard');".format(AREA))
	result.append(cur.fetchone())
	cur.execute("select 'nature;km²', {0} landuse in ('forest', 'grass', 'meadow') or \"natural\" in ('wood', 'scrub', 'wetland', 'grassland', 'heath');".format(AREA))
	result.append(cur.fetchone())
	cur.execute("select 'landuse;km²', {0} landuse in ('residential', 'industrial', 'farmyard', 'allotments', 'cemetery', 'garages', 'construction', 'retail', 'commercial');".format(AREA))
	result.append(cur.fetchone())

	cur.execute("select 'buildings;n', {0} building is not null;".format(COUNT))
	result.append(cur.fetchone())
	cur.execute("select 'power poles;n', {0} power in ('pole', 'tower');".format(POI))
	result.append(cur.fetchone())
	cur.execute("select 'trees;n', {0} \"natural\" = 'tree';".format(POI))
	result.append(cur.fetchone())
	return result

conn = psycopg2.connect(DATABASE)
cur = conn.cursor()
result = query_stats(cur)
conn.close()
result.insert(0, ('time', '' if len(sys.argv) < 2 else sys.argv[1]))
wr = csv.writer(sys.stdout)
wr.writerow([t[0 if len(sys.argv) < 2 else 1] for t in result])
