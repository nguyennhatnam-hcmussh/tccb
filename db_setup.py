from main.config import get_settings
from sqlmodel import create_engine, Session

settings = get_settings()

database_uri = settings.DATABASE_URI

connect_args = {} # "check_same_thread": True
engine = create_engine(database_uri, connect_args=connect_args, future=True) # echo=True

def get_session():
    with Session(engine) as session:
        yield session