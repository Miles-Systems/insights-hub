from contextlib import contextmanager
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# try:
#     with engine.connect() as connection:
#         result = connection.execute(
#         text("SELECT current_database();")
#         )
#         print(f"Connected to database: {result.scalar()}")

# except SQLAlchemyError as e:
#     print(f"Error connecting to the database: {e}")


# def insert_data():
#     session = SessionLocal(bind=engine)

#     try:
#         session.execute(text("INSERT INTO documents "
#         "(filename,page_count,uploaded_at) "
#         "VALUES "
#         "('Session Test-2.pdf', 5, NOW());"))
#         session.commit()
#     except SQLAlchemyError as e:
#         print(f"Error inserting data: {e}")
#         session.rollback()
#     finally:
#         session.close()

# insert_data()
