# Product-Aggregator
REST API Microservice which allows users:
- to browse a product catalog
- to store a new data in an internal MySQL database 
- automatically update prices from provided Offers service

## Configuration

*Full configuration example*
```
[web]
listen=0.0.0.0:8080

[mysql]
host=db
port=3306
user=root
password=qwerty
database=db

[offers]
host=https://python.exercise.applifting.cz/api/v1/
token=***
```
### [mysql]
Provides settings for MySQL database connection.

### [offers]
Provides settings for Offers service connection.

## Install

All required packages are listed in `requirements.txt` file. 
To install them run:

    pip3 install -r requirements.txt

## Run the app
#### Run in Docker

    docker-compose up

It will start MySQL database container and once it is ready, 
will start the application container.  
*It might take some time for database to start up.*

#### Run locally

    python3 product_aggregator.py -c ./etc/product_aggregator.conf

*In this case MySQL database should be already running.*
## REST API
### Create a product
    POST /products/create
    {
        "name": String, 
        "description": String
    }
Creates a new product with specified `name` and `description`.  
Returns product's id on success, returns failure otherwise.

### Read a product
    GET /products/{id}
Returns a product with specified `id` if exists, returns failure otherwise.

### Delete a product
    DELETE /products/{id}
Returns product's `id` on success, returns failure otherwise.

### Update a product
    PUT /products/{id}
    {
        "name": String, 
        "description": String
    }
Updates existing product via `id` with specified field(s) `name`/`description`.  
Returns product's `id` on success, returns failure otherwise.

### List offers for a product
    GET /offers/{product_id}
Returns list of offers for given product's `id` on success, returns failure otherwise.