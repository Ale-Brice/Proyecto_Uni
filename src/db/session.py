from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import engine
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)
<<<<<<< HEAD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
=======
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
>>>>>>> d1641e3db7eb8767eabc99a8ba0446559c4fb6a8
