from sqlite_config import Base, engine#, User

def create_tables():
    # Create all tables that do not yet exist
    #Base.metadata.drop_all(bind=engine, tables=[User.__table__])
    Base.metadata.create_all(bind=engine)
