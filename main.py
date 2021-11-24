import yamusic
import sqluploader
from pprint import pprint
import os

if __name__ == '__main__':

    answer = input("Вы хотите получить данные(get) из базы или загрузить данные(load)? ")

    if answer == 'load':
        artist_id = input("Введите id артиста: ")

        info_loader = yamusic.YaMusic(artist_id)

        result_main_file, artist_name, genres = info_loader.get_artist_info()
        album_info = info_loader.make_album_info(result_main_file)
        compilation_info = info_loader.make_compilation_info(result_main_file)
        album_playlist = info_loader.get_album_playlist(album_info)
        compilation_playlist = info_loader.get_album_playlist(compilation_info, True)
    
        if os.path.isfile(f'{artist_id}.json'): 
            os.remove(f'{artist_id}.json') 

        database = 'testbase'
        user = 'karina'
        password = '1111'

        sql_uploader = sqluploader.SqlUpolader(database, user, password, artist_id, artist_name)

        table_artist_tuples = sql_uploader.upload_table_artist()
        # pprint('*****************')
        # pprint(table_artist_tuples)
        
        table_artist_genre = sql_uploader.upload_table_artist_genre(genres, table_artist_tuples)
        # pprint('*****************')
        # pprint(table_artist_genre)

        album = sql_uploader.upload_table_album(album_info)
        # pprint('*****************')
        # pprint(album)
        
        table_artist_album = sql_uploader.upload_table_artist_album(table_artist_tuples, album)
        # pprint('*****************')
        # pprint(table_artist_album)

        table_track_tupels = sql_uploader.upload_table_track(album_playlist, album)
        # pprint('*****************')
        # pprint(table_track_tupels)

        compilation = sql_uploader.upload_table_compilation(compilation_info)
        # pprint('*****************')
        # pprint(compilation)

        compilation_list = sql_uploader.get_track_from_compilation(compilation_playlist, compilation)

        track_compilation_tuples = sql_uploader.upload_table_track_compilation(table_track_tupels, compilation_list)
        # pprint('*****************')
        # pprint(track_compilation_tuples)

    elif answer == 'get':
        
        database = 'testbase'
        user = 'karina'
        password = '1111'

        sql_uploader = sqluploader.SqlUpolader(database, user, password)

        album_release = sql_uploader.get_album_release()
        pprint(album_release)

        track_timing = sql_uploader.get_the_longest_track()
        pprint(track_timing)

        certain_timing = sql_uploader.get_certain_timing()
        pprint(certain_timing)

        certain_compilation = sql_uploader.get_certain_compilation()
        pprint(certain_compilation)

        one_words_name = sql_uploader.get_one_words_name()
        pprint(one_words_name)

        contains_slice = sql_uploader.get_contains_slice()
        pprint(contains_slice)