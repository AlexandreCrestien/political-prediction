from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Any

class CommuneResponse(BaseModel):
    id: int
    years: str = Field(..., max_length=4)
    city: str
    code_insee: str
    pct_gauche: float
    pct_centre: float
    pct_droite: float
    statistics: Optional[dict[str, Any]] = None
    updated_at: datetime

    # Permet de convertir l'objet SQLAlchemy en Pydantic automatiquement
    model_config = ConfigDict(from_attributes=True)