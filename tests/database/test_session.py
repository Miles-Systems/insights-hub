from app.database.database import SessionLocal
from sqlalchemy import text

session = SessionLocal()

def test_database_connection():
    try:
        result = session.execute(text("SELECT current_database();"))
        assert result.scalar() is not None
    except Exception as e:
        assert False, f"Database connection test failed: {e}"
    finally:
        session.close()