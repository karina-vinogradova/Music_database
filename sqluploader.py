from pprint import pprint
import sqlalchemy

class SqlUpolader():

    def __init__(self, database, user, password, artist_id=None, artist_name=None):
        self.artist_id = artist_id
        self.artist_name = artist_name
        
        engine = sqlalchemy.create_engine(f'postgresql://{user}:{password}@localhost:5432/{database}')
        self.connection = engine.connect()

    def upload_table_artist(self):
        self.connection.execute(f"""INSERT INTO artist(id, name) 
           VALUES(DEFAULT, '{self.artist_name}');
        """)

        sel = self.connection.execute("""SELECT * FROM artist;
        """).fetchall()
        for_send = sel[-1]

        return for_send

    def upload_table_genre(self, genres):
        count = 0
        for genre in genres:
            self.connection.execute(f"""INSERT INTO genre(id, name) 
           VALUES(DEFAULT, '{genre}');
        """)
            count += 1

        sel = self.connection.execute("""SELECT * FROM genre;
        """).fetchall()
        for_send = sel[-count:]
        return for_send

    def upload_table_artist_genre(self, genres, table_artist_tuples):
        table_genre_tuples = self.upload_table_genre(genres)
        # pprint("******************")
        # pprint(table_genre_tuples)


        for i in table_genre_tuples:
            genre_id = i[0]
            self.connection.execute(f"""INSERT INTO artist_genre(artist_id, genre_id) 
        VALUES({table_artist_tuples[0]}, '{genre_id}');
        """)

        sel = self.connection.execute("""SELECT * FROM artist_genre;
        """).fetchall()
        return sel

    def upload_table_album(self, album_info):
        count = 0
        for i in album_info:
            year_of_release = i[2]
            album_title = i[1].replace('\'', '`')
            self.connection.execute(f"""INSERT INTO album(id, name, year_of_release) 
        VALUES(DEFAULT, '{album_title}', {year_of_release});
        """)
            count += 1
        
        sel = self.connection.execute("""SELECT * FROM album;
        """).fetchall()
        for_send = sel[-count:]
        return for_send

    def upload_table_artist_album(self, table_artist_tuples, album):
        artist_id = table_artist_tuples[0]
        for i in album:
            self.connection.execute(f"""INSERT INTO artist_album(artist_id, album_id) 
            VALUES({artist_id}, {i[0]});
            """)

        sel = self.connection.execute("""SELECT * FROM artist_album;
        """).fetchall()
        return sel

    def upload_table_track(self, album_playlist, album):
        count = 0
        list_with_ids = []
        list_with_playlists = []

        list_with_ids = [i[0] for i in album]

        list_with_playlists = [album_playlist[one_list] for one_list in album_playlist]

        result_list = list(zip(list_with_ids, list_with_playlists))

        for i in result_list:
            album_id = i[0]
            for track in i[1]:
                track_title = track[0].replace('\'', '`')
                timing = track[1]
                self.connection.execute(f"""INSERT INTO track(id, name, album_id, tracktime) 
                VALUES(DEFAULT, '{track_title}', {album_id}, {timing});
                """)
                count += 1

        sel = self.connection.execute("""SELECT * FROM track;
        """).fetchall()
        for_send = sel[-count:]
        return for_send

    def upload_table_compilation(self, compilation_info):
        count = 0
        for i in compilation_info:
            year_of_release = i[2]
            album_title = i[1].replace('\'', '`')
            self.connection.execute(f"""INSERT INTO compilation(id, name, year_of_release) 
        VALUES(DEFAULT, '{album_title}', {year_of_release});
        """)
            count += 1
        
        sel = self.connection.execute("""SELECT * FROM compilation;
        """).fetchall()
        for_send = sel[-count:]
        return for_send

    def get_track_from_compilation(self, compilation_playlist, compilation):
        compilation_list = []        
        for compilation_album, playlist in compilation_playlist.items():
            for track in playlist:
                if track[0] == int(self.artist_id):
                    for i in compilation:
                        if i[1] == compilation_album:
                            compilation_list.append([i[0], compilation_album, track[2]])        
        
        return compilation_list

    def upload_table_track_compilation(self, table_track_tupels, compilation_list):
        count = 0
        for item in compilation_list:
            for track in table_track_tupels:
               if  item[-1] == track[1]:
                    track_id = track[0]
                    compilation_id = item[0]

                    self.connection.execute(f"""INSERT INTO track_compilation(track_id, compilation_id) 
                VALUES('{track_id}', {compilation_id});
                """)
                    count += 1
        
        sel = self.connection.execute("""SELECT * FROM track_compilation;
        """).fetchall()
        for_send = sel[-count:]
        return for_send

# get data

    def get_album_release(self):
        
        result = self.connection.execute("""
        SELECT name, year_of_release FROM album
        WHERE year_of_release = 1982;
        """).fetchall()

        return result

    def get_the_longest_track(self):

        result = self.connection.execute("""
        SELECT name, tracktime FROM track
        ORDER BY tracktime DESC
        """).fetchone()

        return result

    def get_certain_timing(self):

        result = self.connection.execute("""
        SELECT name, tracktime FROM track
        WHERE tracktime >= 3.50
        """).fetchall()

        return result

    def get_certain_compilation(self):

        result = self.connection.execute("""
        SELECT name, year_of_release FROM compilation
        WHERE year_of_release BETWEEN 2016 and 2020
        """).fetchall()

        return result

    def get_one_words_name(self):

        result = self.connection.execute("""
        SELECT name FROM artist
        WHERE name NOT LIKE '%% %%'
        """).fetchall()

        return result

    def get_contains_slice(self):

        result = self.connection.execute("""
        SELECT name FROM track
        WHERE name LIKE '%%ill%%'
        """).fetchall()

        return result
