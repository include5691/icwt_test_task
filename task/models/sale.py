from datetime import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey

class Sale(Model):
    """Sale object."""

    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    discount = Column(Float)
    dttm = Column(DateTime, nullable=False, default=datetime.now)