from database.DB_connect import DBConnect
from model.album import Album
from model.connessione import Connessione


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodi(ncanzoni):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.*
from album a , track t 
where a.AlbumId =t.AlbumId 
group by t.AlbumId 
having count(t.TrackId)>%s"""

        cursor.execute(query,(ncanzoni,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni(n):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.a1 as v1, t2.a2 as v2, (t1.n1-t2.n2) as peso
from (select t.AlbumId as a1, count(t.TrackId) as n1
from track t 
group by t.AlbumId 
having count(t.TrackId)>%s) as t1,
(select t.AlbumId as a2, count(t.TrackId) as n2
from track t 
group by t.AlbumId 
having count(t.TrackId)>%s) as t2
where t1.a1<t2.a2 and t1.n1!=t2.n2"""

        cursor.execute(query,(n,n,))

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result