from fastapi import FastAPI
from .routes import jobs, users
from fastapi.responses import ORJSONResponse

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

#!!!!!!!!!!!!!!!!!!!!!!!!!!!
#I need to make a version and send the version # with all the job_data
#!!!!!!!!!!!!!!!!!!!!!!!!!!!

# v  Path Operator decorator
# @app.get("/")
# async def root():
#     return {}
@app.get("/")
#def users_session_jobs_applied(job_url: str, job_title: str, job_location: str, company_name: str, job_workplaceType: str, company_department: str, job_id_number: str, job_release_date: str, employment_type: str, experience_level: str, years_of_experience: int, company_industry: str):
#ok to do this because my server will have Py 3.10 which is the only compiler that matters! This code doesn't run on users devices!!!
def process_users_jobs_applied_to_this_session(jobs_applied_to_this_session: str | int | None)
    if check_for_update():
        if check_if_user_wants_update() == False:
            pass
        self.@app.response()


#@app.get("/post/offerCodeUpdate/")
#def

@app.put("update-available/{app_current_version}")
def check_if_user_wants_update():
    return (await def ask_user_to_decide(choice: False):
                        return ({"users_decesion_about_update": "False"} | False) )

async def check_for_update():
    app_current_version = utils.get_app_current_version()
    if users_app_current_version < app_current_version:
        return True
    return False




#-----  upload files (maybe how I can send the app code updates) 
@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
#------------------------



#-----  how I send the user the updated code(directory)
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from fastapi.responses import FileResponse

# Database setup
DATABASE_URL = "mysql+mariadb://username:password@localhost/db_name"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, index=True)
    directory = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

@app.get("/get_file/{file_id}")
async def get_file(file_id: int):
    # Initialize DB session
    db = SessionLocal()
    
    # Fetch directory from MariaDB
    db_file = db.query(File).filter(File.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    directory_path = db_file.directory
    
    # Check if file exists
    file_path = Path(directory_path)
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found on server")
    
    # Send file to user
    return FileResponse(path=str(file_path), headers={"Content-Disposition": f"attachment; filename={file_path.name}"})
#------------------------





app.include_router(jobs.router, prefix="/jobs")
app.include_router(users.router, prefix="/users")



