from __future__ import annotations

import os
import logging
from pathlib import Path

import joblib
import pandas as pd
from sqlalchemy.orm import Session

from app.model.classification_model import CommuneStats, PredictionResult
from app.schemas.classification_model import (CommuneStatsRow,PredictionResponse,)

logger = logging.getLogger(__name__)


MODEL_DIR = Path(os.getenv("MODEL_DIR", "models"))
MODEL_FILENAME = os.getenv("MODEL_FILENAME", "")          
REFERENCE_YEARs_OLD = str(os.getenv("REFERENCE_YEARs_OLD", "2012"))
REFERENCE_YEARs_NEW = str(os.getenv("REFERENCE_YEARs_NEW", "2022"))
PROJECTION_YEARs = str(os.getenv("PROJECTION_YEARs", "2027"))
YEARs_GAP = int(REFERENCE_YEARs_NEW) - int(REFERENCE_YEARs_OLD)       
PROJECTION_DELTA = int(PROJECTION_YEARs) - int(REFERENCE_YEARs_NEW)  

LABEL_MAP: dict[int, str] = {0: "centre", 1: "droite", 2: "gauche"}

ACTIVE_POP_COLUMNS = [
    "hommes", "femmes",
    "agriculteurs", "artisans", "cadres", "intermediaires",
    "employes", "ouvriers", "retraites", "etudiants", "inactifs",
    "age_15_24", "age_25_39", "age_40_54", "age_55_64", "age_65_79", "age_80_plus",
    "maries", "pacses", "concubinage", "veufs", "divorces", "celibataires",
]

HOUSEHOLD_COLUMNS = [
    "personne_seule", "homme_seul", "femme_seule", "colocation",
    "famille", "famille_monoparentale", "couple_sans_enfant", "couple_avec_enfants",
]

MODEL_FEATURES = ACTIVE_POP_COLUMNS + HOUSEHOLD_COLUMNS



_model_cache: dict[str, object] = {}


def _get_model_path() -> Path:
    """Return the most recent model file in MODEL_DIR, or the explicit override."""
    if MODEL_FILENAME:
        path = MODEL_DIR / MODEL_FILENAME
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        return path

    candidates = sorted(MODEL_DIR.glob("predilection_model_*"), reverse=True)
    if not candidates:
        raise FileNotFoundError(f"No model file found in {MODEL_DIR}")
    return candidates[0]


def get_model() -> tuple[object, str]:
    """Load and cache the model. Returns (pipeline, model_version_string)."""
    path = _get_model_path()
    key = str(path)
    if key not in _model_cache:
        logger.info("Loading model from %s", path)
        _model_cache[key] = joblib.load(path)
    return _model_cache[key], path.name


def _fetch_stats(db: Session, code_insee: str, years: str) -> CommuneStatsRow:
    row = (
        db.query(CommuneStats)
        .filter(CommuneStats.code_insee == code_insee, CommuneStats.years == years)
        .first()
    )
    if row is None:
        raise ValueError(
            f"Aucune statistique trouvée pour la commune {code_insee!r} "
            f"et l'année {years}."
        )
    return CommuneStatsRow.model_validate(row)



def _project_to_2027(
    old: CommuneStatsRow,
    new: CommuneStatsRow,
) -> dict[str, float]:
    """
    For every numeric field, compute a linear 2027 projection:
        projection = new_value + ((new_value - old_value) / YEARs_GAP) * PROJECTION_DELTA
    Values are floored at 0.
    """
    projected: dict[str, float] = {}
    all_fields = list(CommuneStatsRow.model_fields.keys())
    skip = {"code_insee", "years"}

    for field in all_fields:
        if field in skip:
            continue
        v_old = getattr(old, field)
        v_new = getattr(new, field)
        if v_old is None or v_new is None:
            projected[field] = v_new if v_new is not None else 0.0
            continue
        coeff = (float(v_new) - float(v_old)) / YEARs_GAP
        projected[field] = max(float(v_new) + coeff * PROJECTION_DELTA, 0.0)

    return projected


def _to_percentages(projected: dict[str, float]) -> pd.DataFrame:
    """
    Convert raw counts to percentages, then build the feature DataFrame
    in the exact column order the model was trained on.
    """
    pop_active = projected["population_active"]
    pop_enfants = projected["population_avec_enfants"]

    if pop_active <= 0:
        raise ValueError("population_active projetée est nulle ou négative.")
    if pop_enfants <= 0:
        raise ValueError("population_avec_enfants projetée est nulle ou négative.")

    features: dict[str, float] = {}

    for col in ACTIVE_POP_COLUMNS:
        raw = projected.get(col, 0.0)
        features[col] = (raw / pop_active) * 100

    for col in HOUSEHOLD_COLUMNS:
        raw = projected.get(col, 0.0)
        features[col] = (raw / pop_enfants) * 100

    return pd.DataFrame([features])[MODEL_FEATURES]



def predict(db: Session, code_insee: str) -> PredictionResponse:
    """
    Full prediction pipeline for a given commune.

    Args:
        db:          Active SQLAlchemy session.
        code_insee:  5-digit INSEE commune code.

    Returns:
        PredictionResponse with the political leaning label.

    Raises:
        ValueError:       If required DB rows are missing or data is invalid.
        FileNotFoundError: If no model file is found.
    """
    stats_old = _fetch_stats(db, code_insee, REFERENCE_YEARs_OLD)
    stats_new = _fetch_stats(db, code_insee, REFERENCE_YEARs_NEW)


    projected = _project_to_2027(stats_old, stats_new)

    X = _to_percentages(projected)
    logger.debug("Feature matrix for %s:\n%s", code_insee, X.to_dict(orient="records"))

    model, model_version = get_model()
    label_index: int = int(model.predict(X)[0])
    prediction = LABEL_MAP[label_index]

    audit = PredictionResult(
        code_insee=code_insee,
        prediction=prediction,
        predicted_label_index=label_index,
        model_version=model_version,
    )
    db.add(audit)
    db.commit()

    logger.info("Prediction for %s → %s (model: %s)", code_insee, prediction, model_version)

    return PredictionResponse(
        code_insee=code_insee,
        prediction=prediction,
        model_version=model_version,
    )