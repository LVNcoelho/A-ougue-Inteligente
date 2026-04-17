import os
from supabase import create_client, Client

# O Vercel já injeta essas variáveis automaticamente pelo os.environ
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("ERRO: As chaves SUPABASE_URL ou SUPABASE_KEY não foram encontradas no Vercel.")

supabase: Client = create_client(url, key)
