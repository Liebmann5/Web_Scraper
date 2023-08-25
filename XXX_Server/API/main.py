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
@app.get("/")
#def users_session_jobs_applied(job_url: str, job_title: str, job_location: str, company_name: str, job_workplaceType: str, company_department: str, job_id_number: str, job_release_date: str, employment_type: str, experience_level: str, years_of_experience: int, company_industry: str):
#ok to do this because my server will have Py 3.10 which is the only compiler that matters! This code doesn't run on users devices!!!
def process_users_jobs_applied_to_this_session(jobs_applied_to_this_session: str | int | None)
    if check_for_uodate():
        if user_wants_updates() == False:
            pass
        self.@app.response()


@app.get("/post/offerCodeUpdate/")
def 



app.include_router(jobs.router, prefix="/jobs")
app.include_router(users.router, prefix="/users")



