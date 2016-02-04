CREATE TABLE planet_osm_notes(
	id integer NOT NULL PRIMARY KEY,
	geom geometry NOT NULL,
	created_at timestamp,
	closed_at timestamp
);
CREATE TABLE planet_osm_notes_comments(
	note_id integer REFERENCES planet_osm_notes (id),
	action text,
	"timestamp" timestamp,
	uid integer,
	"user" text,
	comment text
);
