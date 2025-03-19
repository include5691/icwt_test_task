from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String

class Category(Model):
    """Product category object."""
    
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)