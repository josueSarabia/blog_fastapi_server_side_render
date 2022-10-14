from database.database import SessionLocal

def get_db():
    """ Get database sessionlocal

    Returns:
        db: database sessionlocal
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()