from fastapi import APIRouter
from ..models.job import job
from ..utils.database import add_job

router = APIRouter()

@router.post("/add")
async def add_job_endpoint(job: job):
    #Validate and add job data
    result = add_job(job)
    return result

@router.get("/statistics/")
async def get_job_statistics():
    #return statistics of job market stuff