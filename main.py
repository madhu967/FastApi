from fastapi import FastAPI,Request
from mockData import products
from dtos import ProductDTO


app = FastAPI()

@app.get("/")
def home():
    return "Welcome to the FastAPI application!"

@app.get("/products")
def get_products():
    return products

#path params..

@app.get("/product/{product_id}")
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


##body,headers = request headers, Query params


##different types of HTTP Methods

@app.post("/create_product")
def create_product(product_data:ProductDTO):
    product_data=product_data.model_dump()
    products.append(product_data)
    return{"status":"Product created successfully","data":products}


@app.put("/update_product/{product_id}")
def update_product(product_data:ProductDTO,product_id:int):

    for index,oneProduct in enumerate(products):
        if oneProduct.get("id")==product_id:
            products[index]=product_data.model_dump()
            return {"status":"Product updated successfully","data":products}

   
@app.delete("/delete_product/{product_id}")
def delete_product(product_id:int):
    for index,oneProduct in enumerate(products):
            if oneProduct.get("id")==product_id:
             deleted_product=products.pop(index)
             return {"status":"Product deleted succesfully","product":deleted_product}
    return{
        "error":"Product not found for this id"
    }
## how to call diffrenet HTTP METHODS - Any Tool?



##how to validate data -DTOS

