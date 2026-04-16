import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("ERRO: Verifique suas chaves no arquivo .env")

supabase: Client = create_client(url, key)
