from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey

class Product(Model):
    """Product object."""
    
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))