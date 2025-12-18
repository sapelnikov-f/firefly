import psycopg2
from psycopg2.extras import RealDictCursor
from supabase import create_client

class DataLoader:
    def __init__(self):
        self.supabase = create_client("https://rhgazdnloccrierufgvk.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJoZ2F6ZG5sb2NjcmllcnVmZ3ZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5NjI5MDEsImV4cCI6MjA4MDUzODkwMX0.7uMMmehcpXcxQcKT398CIt_ygCA75S2E-EXP872Mkt0")

    def load_pois(self):

        response = self.supabase.table("pois").select("id, name, category, description, pass_category, geom").execute()
        return response.data

    def load_segments(self):
        response = self.supabase.table("segments").select("start_id, end_id, difficulty, is_camp, segment_description, geom, distance_m").execute()
        return response.data
    

