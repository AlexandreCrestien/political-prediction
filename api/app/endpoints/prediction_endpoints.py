from __future__ import annotations

import logging
from typing import Generator

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.schemas.classification_model import PredictionRequest, PredictionResponse, PredictionError
from app.services.prediction import predict
from app.core.config import settings

logger = logging.getLogger(__name__)

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



router = APIRouter(tags=["Prediction"])


@router.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        404: {"model": PredictionError, "description": "Commune introuvable en base"},
        422: {"description": "Code INSEE invalide"},
        500: {"model": PredictionError, "description": "Erreur interne du serveur"},
    },
    summary="Prédire le vote politique d'une commune en 2027",
    description=(
        "À partir du Code INSEE de la commune, récupère les statistiques "
        "démographiques en base (années 2011 et 2022), projette les valeurs "
        "à 2027 par extrapolation linéaire, puis retourne la tendance "
        "politique prédite par le modèle XGBoost."
    ),
)
async def predict_commune(
    body: PredictionRequest,
    db: Session = Depends(get_db),
) -> PredictionResponse:
    """
    **Paramètre requis** : `code_insee` — code INSEE à 5 chiffres de la commune.

    **Réponse** :
    - `prediction` : `"centre"` | `"droite"` | `"gauche"`
    - `model_version` : nom du fichier modèle utilisé
    """
    try:
        return predict(db=db, code_insee=body.code_insee)

    except FileNotFoundError as exc:
        logger.exception("Model file missing")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        logger.warning("Prediction failed for %s: %s", body.code_insee, exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Unexpected error during prediction for %s", body.code_insee)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur inattendue s'est produite.",
        ) from exc