# test_db.py
from sqlalchemy import create_engine, text
from app.core.config import settings

try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ Connexion réussie !")
        print(f"PostgreSQL version: {result.fetchone()[0]}")
        result = conn.execute(text("SELECT COUNT(*) FROM communes_stats limit 1;"))
        print(f"Nombre de lignes dans communes_stats: {result.fetchone()[0]}")
except Exception as e:
    print(f"❌ Échec de connexion : {e}")