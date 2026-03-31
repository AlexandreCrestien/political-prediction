from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.communes import PaginatedCommuneResponse
from app.db.database import get_db
from app.services.communes import CommuneService
from app.schemas.communes import CommuneResponse
from typing import List, Optional

router = APIRouter(prefix="/communes", tags=["communes"])


#TODO Replace the return 0 by service.get that will be created
@router.get("/", status_code=status.HTTP_200_OK, response_model=PaginatedCommuneResponse)
async def get_and_search_communes(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter pour la pagination"),
    limit: int = Query(50, ge=1, le=100, description="Nombre maximum d'éléments à retourner pour la pagination"),
    search: str = Query(None, description="Recherche par nom de commune"),
    db: Session = Depends(get_db)
):
    total, data = CommuneService.get_all(db, skip=skip, limit=limit, search=search)
    return {
        "total": total,
        "page": (skip // limit) + 1,
        "limit": limit,
        "data": data
    }


@router.get("/commmune", status_code=status.HTTP_200_OK, response_model=List[CommuneResponse])
async def get_commune_by_code(
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




