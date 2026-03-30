from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.communes import CommuneService
from app.schemas.communes import CommuneResponse
from typing import List, Optional

router = APIRouter(prefix="/communes", tags=["communes"])


#TODO Replace the return 0 by service.get that will be created
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CommuneResponse])
async def read_communes(
    db: Session = Depends(get_db)
):
    stats = CommuneService.get_all(db)
    return stats


@router.get("/search", status_code=status.HTTP_200_OK, response_model=List[CommuneResponse])
async def search_communes(
    code_insee: str = Query(None, description="Code INSEE de la commune"),
    year: str = Query(None, description="Année des statistiques"),
    db: Session = Depends(get_db)
):
    if code_insee and year:
        stats = CommuneService.get_by_insee(db, code_insee=code_insee, year=year)
    else:
        return status.HTTP_400_BAD_REQUEST
    return stats

@router.get("/department/{department_code}", status_code=status.HTTP_200_OK, response_model=List[CommuneResponse])
async def get_communes_by_department(
    department_code: str,
    year: Optional[str] = Query(None, description="Année des statistiques"),
    db: Session = Depends(get_db)
):
    stats = CommuneService.get_by_department(db, department_code=department_code, year=year)
    return stats




