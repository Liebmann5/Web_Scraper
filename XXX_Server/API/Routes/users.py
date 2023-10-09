from fastapi import APIRouter
from ..models.user import User
from ..utils.database import add_user

router = APIRouter()

@router.post("/add/")
async def add_user_endpoint(user: User):
    return add_user(user)

#TODO: Get rid of this!!
@router.get("/{user_id}/jobs/")
async def get_user_jobs(user_id: int):
    # Retrieve the jobs associated with a specific user