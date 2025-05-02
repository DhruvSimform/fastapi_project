from config.database import Base

def create_table():
    """
    create All database tables defined in application
    """

    Base.metadata.create_all()