import yamusic
import sqluploader
from pprint import pprint
import os

if __name__ == '__main__':

    answer = input("Вы хотите получить данные(get) из базы или загрузить данные(load)? ")

    def load_data_in_base(artist_id):
        
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

    if answer == 'load':
        data_load = input("Загрузить начальные данные в пустую базу(1) или дозагрузить данные по конкретному исполнителю(2)? ")      

        if data_load == '1':
            artist_id_list = []
            artist_id_list = ['972', '680', '118884' '79215', '3989', '443']
            for id in artist_id_list:
                artist_id = id
                load_data_in_base(artist_id)

        elif data_load == '2':
            artist_id = input("Введите id артиста: ")
            load_data_in_base(artist_id)
        
        

    elif answer == 'get':
        
        database = 'testbase'
        user = 'karina'
        password = '1111'

        sql_uploader = sqluploader.SqlUpolader(database, user, password)

        # album_release = sql_uploader.get_album_release()
        # pprint(album_release)

        # track_timing = sql_uploader.get_the_longest_track()
        # pprint(track_timing)

        # certain_timing = sql_uploader.get_certain_timing()
        # pprint(certain_timing)

        # certain_compilation = sql_uploader.get_certain_compilation()
        # pprint(certain_compilation)

        # one_words_name = sql_uploader.get_one_words_name()
        # pprint(one_words_name)

        # contains_slice = sql_uploader.get_contains_slice()
        # pprint(contains_slice)

        # result = sql_uploader.get_other_data_for_test()
        # pprint(result)