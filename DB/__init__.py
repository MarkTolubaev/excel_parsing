from .connection import Session, makeEngine
from .models import Base, getData


def init_db():
    engine = makeEngine()
    Base.metadata.create_all(engine)


__all__ = (Session, getData, init_db)
