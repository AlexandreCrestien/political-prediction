from fastapi import APIRouter, status, Depends, Query

router = APIRouter(prefix="/user", tags=["user"])


#TODO Replace the return 0 by service.get that will be created
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id : int
):
    return 0 


#TODO add the schema's Create in the function parameters and add the correct return
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(

):
    return None


#TODO add the schema's Update in the function parameters and add the correct return
@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id : int    
):
    return None


#TODO add the schema's Delete in the function parameters and add the correct return
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user (
    user_id : int,
    soft_delete: bool = Query(False, alias="soft-delete", description="If True, mark as inactive. If False, permanently delete.")
) :
    return None