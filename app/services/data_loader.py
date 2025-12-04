import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import DATABASE_URL

class DataLoader:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

    def load_pois(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name, elevation, category, ST_X(geom) AS lon, ST_Y(geom) AS lat FROM pois;")
            return cur.fetchall()

    def load_segments(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, start_poi, end_poi, length_m, elev_gain FROM segments;")
            return cur.fetchall()
