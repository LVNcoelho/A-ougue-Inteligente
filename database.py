import os
from supabase import create_client, Client

url = os.getenv("VITE_SUPABASE_URL") or os.getenv("SUPABASE_URL")
key = os.getenv("VITE_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    raise ValueError("As chaves do Supabase não foram encontradas! Verifique as Environment Variables.")

supabase: Client = create_client(url, key)