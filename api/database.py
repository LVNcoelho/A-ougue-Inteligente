import os
from supabase import create_client

# Usando o .get() para não travar se a chave demorar a carregar
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Criando o cliente de forma simples
supabase = create_client(url, key)
