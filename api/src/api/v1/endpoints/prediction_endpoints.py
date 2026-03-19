from fastapi import APIRouter, status, Depends, Query

router = APIRouter(prefix="/prediction", tags=["prediction"])


#TODO add the schema's Create in the function parameters and add the correct return
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_prediction(

):
    return None
