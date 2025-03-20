import datetime
import logging
from flask import request
from flask_appbuilder.api import BaseApi, expose
from task.models.sale import Sale
from task.models.product import Product
from task.extensions import db

class SalesApi(BaseApi):

    resource_name = "sales"

    @expose(url='/total', methods=["GET"])
    def get_sales_sum(self):
        """
        Get sum of all sales
        ---
        get:
            summary: Get sum of all sales
            parameters:
              - in: query
                name: start_date
                schema:
                  type: string
                  format: date  # Important: Specify the format for date strings
                description: The start date for the sales period (YYYY-MM-DD).
              - in: query
                name: end_date
                schema:
                  type: string
                  format: date  # Important: Specify the format for date strings
                description: The end date for the sales period (YYYY-MM-DD).
            responses:
            200:
              description: Sum of all sales
        """
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        if not start_date and not end_date:
            return self.response(400, **{"error": "Invalid date range"})
        if not end_date:
            end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            sales = db.session.query(Sale).filter(Sale.dttm >= start_date, Sale.dttm <= end_date).all()
            sales_sum = sum(sale.quantity for sale in sales)
            return self.response(200, **{"sales_sum": sales_sum})
        except Exception as e:
            logging.error(f"Error fetching sales sum: {e}")
            return self.response(500, **{"error": str(e)})

    @expose(url='/top-products', methods=["GET"])
    def get_top_products(self):
        """
        Get top products by sales
        ---
        get:
            summary: Get top products by sales
            parameters:
              - in: query
                name: start_date
                schema:
                  type: string
                  format: date
                description: The start date for the sales period (YYYY-MM-DD).
              - in: query
                name: end_date
                schema:
                  type: string
                  format: date
              - in: query
                name: limit
                schema:
                  type: integer
                description: The number of top products to return.
                description: The end date for the sales period (YYYY-MM-DD).
            responses:
            200:
              description: List of top products by sales
        """
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        limit = request.args.get("limit", default=10, type=int)
        if not start_date and not end_date:
            return self.response(400, **{"error": "Invalid date range"})
        if not end_date:
            end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            query = db.session.query(
                Sale.product_id,
                db.func.sum(Sale.quantity).label('total_sold'),
                Product.name,
                Product.category_id,
            ).join(
                Product, Sale.product_id == Product.id
            ).filter(
                Sale.dttm >= start_date,
                Sale.dttm <= end_date
            ).group_by(
                Sale.product_id,
                Product.name,
                Product.category_id
            ).order_by(
                db.desc('total_sold')
            ).limit(limit)
            results = query.all()
            top_products = []
            for product in results:
                top_products.append({
                    'product_id': product.product_id,
                    'name': product.name,
                    'category_id': product.category_id,
                    'total_sold': product.total_sold
                })
            return self.response(200, **{"top_products": top_products})
        except Exception as e:
            logging.error(f"Error fetching top products: {e}")
            return self.response(500, **{"error": str(e)})