from flet.core import row

from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def get_album_durata(durata):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """ select a.id, a.title, sum(t.milliseconds/60000) as durata
                    from album a, track t
                    where t.album_id = a.id 
                    group by a.id 
                    having sum(t.milliseconds/60000)>= %s """

        cursor.execute(query, (durata,))

        result =[Album(row['id'], row['title'], row['durata']) for row in cursor]
        #print(result)
        cursor.close()
        conn.close()
        return result
    @staticmethod
    def get_edges_a_connessi(list_a_d):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        album_ids = [a.id for a in list_a_d]
        album_ids = tuple(album_ids)

        query = f""" select album_id, playlist_id
                    from playlist_track pt, track t
                    where pt.track_id =t.id and t.album_id in {album_ids}"""
        cursor.execute(query)
        result = {}
        for row in cursor:
            album_id = row['album_id']
            playlist_id = row['playlist_id']
            if album_id not in result:
                result[album_id] = set()
            result[album_id].add(playlist_id)
        cursor.close()
        conn.close()

        return result

