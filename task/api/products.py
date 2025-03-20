from flask import request
from flask_appbuilder.api import BaseApi, expose
from task.models.product import Product
from task.extensions import db
from .cache import cached

class ProductsApi(BaseApi):

    resource_name = "products"

    @expose(url='', methods=["GET"])
    @cached
    def get_products(self):
        """
        Get all products
        ---
        get:
            summary: Get all products
            responses:
            200:
              description: List of products        delete:
            summary: Delete a product
        """
        products = db.session.query(Product).all()
        return self.response(200, **{"products": [product.to_json() for product in products]})

    @expose(url='', methods=["POST"])
    def create_product(self):
        """
        Create a new product
        ---
        post:
          summary: Create a new product
          requestBody:
            description: Product schema
            required: true
            content:
              application/json:
                schema:
                    type: object
                    properties:
                        name:
                        type: string
                        category_id:
                        type: integer
          responses:
            200:
              description: Product created
        """
        data = request.get_json()
        if not data or not data.get("name") or not data.get("category_id"):
            return self.response(400, **{"error": "Invalid data"})
        product = Product(name=data.get("name"), category_id=data.get("category_id"))
        db.session.add(product)
        db.session.commit()
        return self.response(200, **{"product": product.to_json()})
    
    @expose(url='/<int:product_id>', methods=["PUT"])
    def update_product(self, product_id):
        """
        Update a product
        ---
        put:
          summary: Update a product
          parameters:
          - in: path
            schema:
              type: integer
            name: product_id
            required: true
            description: The ID of the product to update.
          requestBody:
            description: Product schema
            required: true
            content:
              application/json:
                schema:
                    type: object
                    properties:
                        name:
                        type: string
                        category_id:
                        type: integer
          responses:
            200:
              description: Product updated
        """
        data = request.get_json()
        if not data or not data.get("name") and not data.get("category_id"):
            return self.response(400, **{"error": "Invalid data"})
        product = db.session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return self.response(404, **{"error": "Product not found"})
        product.name = data.get("name") or product.name
        product.category_id = data.get("category_id") or product.category_id
        db.session.commit()
        return self.response(200, **{"product": product.to_json()})
    
    @expose(url='/<int:product_id>', methods=["DELETE"])
    def delete_product(self, product_id):
        """
        Delete a product
        ---
        delete:
          summary: Delete a product
          parameters:
          - in: path
            schema:
              type: integer
            name: product_id
            required: true
            description: The ID of the product to delete.
          responses:
            200:
              description: Product deleted
        """
        product = db.session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return self.response(404, **{"error": "Product not found"})
        db.session.delete(product)
        db.session.commit()
        return self.response(200)