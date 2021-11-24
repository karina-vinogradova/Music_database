from pprint import pprint
import requests
import json
import os

class YaMusic():

    def __init__(self, artist_id):
        self.artist_id = artist_id

    def get_artist_info(self):

        url_artist = f'https://music.yandex.ru/handlers/artist.jsx?artist={self.artist_id}&what=&sort=&dir=&period=&lang=ru&external-domain=music.yandex.ru&overembed=false&ncrnd=0.9021245906754158'

        result_of_artist = requests.get(url=url_artist).json()

        with open(f'main_{self.artist_id}.json', 'w', encoding='utf-8') as write_file:
           json.dump(result_of_artist, write_file, ensure_ascii=False, indent=4)


        with open(f'main_{self.artist_id}.json', 'r', encoding='utf-8') as read_file:
            result_main_file = json.load(read_file)

        artist_genres = result_main_file['artist']['genres']
        artist_name = result_main_file['artist']['name']

        if os.path.isfile(f'main_{self.artist_id}.json'): 
            os.remove(f'main_{self.artist_id}.json')

        return result_main_file, artist_name, artist_genres

    def get_album_playlist(self, info_about_album, compilation=False):
        
        album_playlist = {}

        for album in info_about_album:
            album_id = album[0]
            album_title = album[1]

            url_album = f'https://music.yandex.ru/handlers/album.jsx?album={album_id}&lang=ru&external-domain=music.yandex.ru&overembed=false&ncrnd=0.9204520299899511'

            result_of_album = requests.get(url=url_album).json()
            

            with open(f'{self.artist_id}.json', 'w', encoding='utf-8') as write_file:
                json.dump(result_of_album, write_file, ensure_ascii=False, indent=4)


            with open(f'{self.artist_id}.json', 'r', encoding='utf-8') as read_file:
                result_file = json.load(read_file)
                track_list = []

                for i in result_file['volumes'][0]:
                    track_id = i['artists'][0]['id']
                    artist_name = i['artists'][0]['name']
                    track_name = i['title']
                    
                    min, sec = divmod(i['durationMs'] // 1000, 60)
                    timing = round(min + (sec / 100), 2)
                    
                    if compilation == False:
                        track_list.append([i['title'], timing])
                    elif compilation == True:
                        track_list.append([track_id, artist_name, track_name, timing])
                        
                album_playlist[album_title] = track_list  
                

        return album_playlist


    def make_album_info(self, result_main_file):

        albums = result_main_file['albums']
        album_info = []

        for album in albums:
            album_id = album['id']
            album_title = album['title']
            release_of_year = album['year']
            
            album_info.append([album_id,  album_title, release_of_year])
        
        return album_info

    def make_compilation_info(self, result_main_file):
        
        compilation = result_main_file['alsoAlbums']
        compilation_info = []

        for item in compilation:
            compilation_title = item['title']
            compilation_id = item['id']
            compilation_year = item['year']
            compilation_info.append([compilation_id, compilation_title, compilation_year])

        return compilation_info
    
