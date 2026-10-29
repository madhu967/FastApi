from fastapi import FastAPI,Request
from mockData import products


app = FastAPI()

@app.get("/")
def home():
    return "Welcome to the FastAPI application!"

@app.get("/products")
def get_products():
    return products

#path params..

@app.get("/product/{product_id}/{date}")
def get_one_product(product_id:int):

    #if product availale in the list of products

    product=None
    for oneproduct in products:
        if oneproduct.get("id")==product_id:
            return oneproduct
    return {
        "error": f"Product with ID {product_id} not found"
    }


## Query params

@app.get("/greet")
def greet_User(name:str,age:int):
    return f"Hello, {name}! You are {age}."

@app.get("/greeting")
def greeting_User(request:Request):
    query_params = dict(request.query_params)
    print(query_params)
    return f"Hello,{query_params.get("name")}, You are {query_params.get("age")}"