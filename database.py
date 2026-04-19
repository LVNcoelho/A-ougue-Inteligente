import os
from supabase import create_client, Client

# Pega as chaves que você já configurou na Vercel e no ambiente
url: str = os.environ.get("VITE_SUPABASE_URL") or os.environ.get("SUPABASE_URL")
key: str = os.environ.get("VITE_SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_ANON_KEY")

if not url or not key:
    print("⚠️ Atenção: As chaves do Supabase não foram encontradas no ambiente!")

supabase: Client = create_client(url, key)