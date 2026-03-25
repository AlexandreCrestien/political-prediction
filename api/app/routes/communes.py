from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.communes import CommuneService
from app.schemas.communes import CommuneResponse
from typing import List, Optional

router = APIRouter()

@router.get("/communes", response_model=List[CommuneResponse])
def read_communes(
    code_insee: str = None, 
    year: str = None, 
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques des communes. 
    Filtre optionnel par code_insee et année.
    """
    if code_insee:
        stats = CommuneService.get_by_insee(db, code_insee=code_insee, year=year)
    else:
        stats = CommuneService.get_all(db)
        
    return stats