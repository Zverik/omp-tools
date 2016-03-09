#!/usr/bin/python
import sys, json, psycopg2

if len(sys.argv) < 4:
	print 'Usage: {0} <dbname> <tablename> <bounds.geojson>'.format(sys.argv[0])
	sys.exit(1)

with open(sys.argv[3], 'r') as f:
	geom = json.load(f)['features'][0]['geometry']

conn = psycopg2.connect('dbname={0}'.format(sys.argv[1]))
cur = conn.cursor()
cur.execute('create table {0} ( geom geometry not null )'.format(sys.argv[2]))
cur.execute('insert into {0} (geom) values (ST_Transform(ST_GeomFromGeoJSON(%s, 4326), 900913))'.format(sys.argv[2]), (json.dumps(geom),))
if geom['type'] == 'LineString':
	cur.execute('update {0} set geom=ST_MakePolygon(geom)'.format(sys.argv[2]))
conn.commit()
cur.close()
