from fastapi import FastAPI
from .routes import jobs, users

# HOW TO RUN
#   uvicorn main:app --reload

# URL = https://example.com/items/foo
# Path = /items/foo

# Operation - refers to one of the HTTP "methods"
    #(POST - to create data, GET - to read data, PUT - to update data, DELETE - to delete data, OPTIONS, HEAD, PATCH, TRACE)

# @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:
    #the path /
    #using a get operation

# Path Operation = .get("/")
# decorator(in regards to python) = @something

#Here the app variable will be an "instance" of the class FastAPI.
app = FastAPI()


# v  Path Operator decorator
# @app.get("/")
# async def root():
#     return {}


app.include_router(jobs.router, prefix="/jobs")
app.include_router(users.router, prefix="/users")
