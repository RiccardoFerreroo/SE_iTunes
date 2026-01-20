from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def carica_albums(durata_minima):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t.album_id,t.id, a.title, sum(t.milliseconds/60000) as durata
                    from album a, track t
                    where a.id = t.album_id 
                    group by a.id
                    having durata > %s"""

        cursor.execute(query, (float(durata_minima),))

        for row in cursor:
            a = Album(id=row['album_id'], title=row['title'], durata=row['durata'])
            result.append(a)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def album_playlist_map( lista_albums):
        conn = DBConnect.get_connection()
        result={}
        album_ids =[]
        for a in lista_albums:
            album_id = a.id
            album_ids.append(album_id)
        album_ids = tuple(album_ids)


        cursor = conn.cursor(dictionary=True)
        query = f""" select distinct t.album_id,pt.playlist_id 
                    from track t, playlist_track pt 
                    where pt.track_id= t.id and t.album_id in {album_ids}"""
        cursor.execute(query)
        for row in cursor:
            a_id =row['album_id']
            playlist_id = row['playlist_id']
            for oggetto in lista_albums:
                if oggetto.id == a_id:
                    if oggetto not in result:
                        result[oggetto] = set()
                    result[oggetto].add(playlist_id)

        return result


