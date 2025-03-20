# icwt_test_task
InCodeWeTrust test task

## Setup

### Create and activate venv
```shell
python3 -m venv .venv
source .venv/bin/activate # for bash
```

### Install requirements
```shell
pip install -r requirements.txt
```

### Create and fill .env file

**Variables:**
- `DATABASE_URL`: your postgres url in format `postgresql://user:pass@host:port/db`
- `SECRET_KEY`: flask secret. You may generate it using:
```shell
openssl rand -base64 15
```

### Perform alembic migration
```shell
cd task
alembic upgrade head
```

### Return to repo root and run the app
```shell
cd ..
python3 -m task.main # run as module
```

## Setup with Docker

### Create docker image
```shell
docker build -t your_login/your_repo:icwt_test .
```

### Run docker container
```shell
docker run --name icwt_test --network="host" your_login/your_repo:icwt_test
```

## Products API

__NOTE__:
In this test app I used /api/v1 base route prefix since i don't find how to change it

### Get All Products

Retrieves a list of all products.

**Endpoint:** `/api/v1/products`  
**Method:** GET  


**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Product Name",
      "category_id": 3
    },
    {
      "id": 2,
      "name": "Another Product",
      "category_id": 1
    }
  ]
}
```

**Status Codes:**
- 200: Success

### Create Product

Creates a new product.

**Endpoint:** `/api/v1/products`  
**Method:** POST  


**Request Body:**
```json
{
  "name": "New Product",
  "category_id": 2
}
```

**Response:**
```json
{
  "product": {
    "id": 3,
    "name": "New Product",
    "category_id": 2
  }
}
```

**Status Codes:**
- 200: Success
- 400: Invalid data

### Update Product

Updates an existing product.

**Endpoint:** `/api/v1/products/<product_id>`  
**Method:** PUT  


**Path Parameters:**
- `product_id`: The ID of the product to update

**Request Body:**
```json
{
  "name": "Updated Product Name",
  "category_id": 4
}
```

**Response:**
```json
{
  "product": {
    "id": 1,
    "name": "Updated Product Name",
    "category_id": 4
  }
}
```

**Status Codes:**
- 200: Success
- 400: Invalid data
- 404: Product not found

### Delete Product

Deletes a product.

**Endpoint:** `/api/v1/products/<product_id>`  
**Method:** DELETE  


**Path Parameters:**
- `product_id`: The ID of the product to delete

**Response:** Empty body with 200 status code

**Status Codes:**
- 200: Success
- 404: Product not found

## Sales API

### Get Total Sales

Calculates the sum of all sales within a specified date range.

**Endpoint:** `/api/v1/sales/total`  
**Method:** GET  

**Query Parameters:**
- `start_date` (required): The start date for the sales period (YYYY-MM-DD)
- `end_date` (optional): The end date for the sales period (YYYY-MM-DD). If not provided, defaults to the current date.

**Response:**
```json
{
  "sales_sum": 1250
}
```

**Status Codes:**
- 200: Success
- 400: Invalid date range
- 500: Server error

### Get Top Products

Retrieves the top-selling products within a specified date range.

**Endpoint:** `/api/v1/sales/top-products`  
**Method:** GET  


**Query Parameters:**
- `start_date` (required): The start date for the sales period (YYYY-MM-DD)
- `end_date` (optional): The end date for the sales period (YYYY-MM-DD). If not provided, defaults to the current date.
- `limit` (optional): The maximum number of products to return. Defaults to 10.

**Response:**
```json
{
  "top_products": [
    {
      "product_id": 1,
      "name": "Product Name",
      "category_id": 3,
      "total_sold": 150
    },
    {
      "product_id": 2,
      "name": "Another Product",
      "category_id": 1,
      "total_sold": 125
    }
  ]
}
```

**Status Codes:**
- 200: Success
- 400: Invalid date range
- 500: Server error

---
ʕ•́ᴥ•̀ʔっ♡