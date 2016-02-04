CREATE TABLE planet_osm_notes(
	id integer NOT NULL,
	geom geometry NOT NULL,
	created_at timestamp,
	closed_at timestamp
);

