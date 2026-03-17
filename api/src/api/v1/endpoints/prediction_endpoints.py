from fastapi import APIRouter, status, Depends, Query

router = APIRouter(prefix="/prediction", tags=["prediction"])


#TODO Replace the return 0 by service.get that will be created
@router.get("/{prediction_id}", status_code=status.HTTP_200_OK)
async def get_prediction(
    prediction_id : int
):
    return 0 


#TODO add the schema's Create in the function parameters and add the correct return
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_prediction(

):
    return None



#TODO add the schema's Delete in the function parameters and add the correct return
@router.delete("/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ (
    _id : int,
    soft_delete: bool = Query(False, alias="soft-delete", description="If True, mark as inactive. If False, permanently delete.")
) :
    return None