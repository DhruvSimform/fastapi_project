from ..config.database import Base , engine

def create_table():
    """
    create All database tables defined in application
    """

    Base.metadata.create_all(bind = engine)