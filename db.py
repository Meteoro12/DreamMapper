import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Load environment variables
load_dotenv()

# Database connection configuration
DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}" \
               f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT', '5432')}/{os.getenv('DATABASE_NAME')}"

# Create database engine
engine = create_engine(DATABASE_URL)

# Create a scoped session
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    pass