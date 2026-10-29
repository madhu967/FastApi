from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return "Welcome to the FastAPI application!"

@app.get("/contact")
def contact():
    return "You can connect us any time."