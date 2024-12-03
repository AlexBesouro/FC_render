from fastapi import FastAPI
from app.routers import user

# Create an instance of the FastAPI class, which represents a web application.
app = FastAPI()

#  Create a set of routes (defined in a separate router module or class) into the main FastAPI application (app)
app.include_router(user.router)


@app.get("/")
async def root():
    return  {"data": "hello"}
