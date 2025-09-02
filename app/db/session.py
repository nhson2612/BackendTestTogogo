from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session