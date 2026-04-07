from pydantic import BaseModel, Field
from typing import Literal


class PredictionRequest(BaseModel):
    """
    Body of POST /predict.
    Only the commune's Code_INSEE is required — the service fetches the
    statistics from the database and projects them to 2027.
    """
    Code_INSEE: str = Field(
        ...,
        min_length=5,
        max_length=5,
        pattern=r"^\d{5}$",
        examples=["59280"],
        description="Code INSEE à 5 chiffres de la commune.",
    )


class PredictionResponse(BaseModel):
    """
    Successful prediction result.
    """
    Code_INSEE: str
    prediction: Literal["centre", "droite", "gauche"]
    model_version: str = Field(description="Nom du fichier modèle utilisé.")


class PredictionError(BaseModel):
    """
    Returned when the prediction cannot be completed.
    """
    Code_INSEE: str
    detail: str




class CommuneStatsRow(BaseModel):
    """
    Flat representation of one CommuneStats row, used inside the service.
    Column names match the SQLAlchemy model attributes.
    """
    Code_INSEE: str
    population_active: float
    population_avec_enfants: float

    hommes: float | None = None
    femmes: float | None = None

    agriculteurs: float | None = None
    artisans: float | None = None
    cadres: float | None = None
    intermediaires: float | None = None
    employes: float | None = None
    ouvriers: float | None = None
    retraites: float | None = None
    etudiants: float | None = None
    inactifs: float | None = None

    age_15_24: float | None = None
    age_25_39: float | None = None
    age_40_54: float | None = None
    age_55_64: float | None = None
    age_65_79: float | None = None
    age_80_plus: float | None = None

    maries: float | None = None
    pacses: float | None = None
    concubinage: float | None = None
    veufs: float | None = None
    divorces: float | None = None
    celibataires: float | None = None

    personne_seule: float | None = None
    homme_seul: float | None = None
    femme_seule: float | None = None
    colocation: float | None = None
    famille: float | None = None
    famille_monoparentale: float | None = None
    couple_sans_enfant: float | None = None
    couple_avec_enfants: float | None = None

    model_config = {"from_attributes": True}