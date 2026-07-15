from app.database.database import Base, engine

from app.models.expense import Expense
from app.models.user import User

def init_db():
    Base.metadata.create_all(bind=engine)