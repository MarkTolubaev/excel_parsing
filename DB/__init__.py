from .connection import Session, makeEngine
from .models import Base


__all__ = (Session, 'init_db')


def init_db():
    engine = makeEngine()
    Base.metadata.create_all(engine)
