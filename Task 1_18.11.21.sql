create table if not exists artist(
id serial primary key,
name varchar(100) not null
);

create table if not exists album (
id serial primary key,
name varchar (200) not null,
year_of_release integer not null
);

create table if not exists track (
id serial primary key,
name varchar (100) not null,
album_id integer not null references album(id),
tracktime NUMERIC(4,2) not null
);

create table if not exists genre (
id serial primary key,
name varchar (100) not null
);

create table if not exists compilation (
id serial primary key,
name varchar (200) not null,
year_of_release integer not null
);

create table if not exists artist_genre (
artist_id integer not null references artist(id),
genre_id integer not null references genre(id),
CONSTRAINT pk_art_gnr primary key (artist_id, genre_id)
);

create table if not exists artist_album (
artist_id integer not null references artist(id),
album_id integer not null references album(id),
CONSTRAINT pk_art_alb primary key (artist_id, album_id)
);

create table if not exists track_compilation (
track_id integer not null references track(id),
compilation_id integer not null references compilation(id),
CONSTRAINT pk_tr_coll primary key (track_id, compilation_id)
);