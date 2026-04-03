from sqlalchemy import Column, String, Integer, Float, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CommuneStats(Base):
    """
    Raw demographic statistics for a commune, per year.
    Requires at least year 2011 and 2022 per Code_INSEE
    to allow 2027 projection at prediction time.
    """
    __tablename__ = "commune_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code_insee = Column(String(10), nullable=False, index=True)
    annee = Column(Integer, nullable=False)

    population_active = Column(Float, nullable=False)
    population_avec_enfants = Column(Float, nullable=False)

    hommes = Column(Float, nullable=True)
    femmes = Column(Float, nullable=True)

    agriculteurs = Column(Float, nullable=True)
    artisans = Column(Float, nullable=True)
    cadres = Column(Float, nullable=True)
    intermediaires = Column(Float, nullable=True)
    employes = Column(Float, nullable=True)
    ouvriers = Column(Float, nullable=True)
    retraites = Column(Float, nullable=True)
    etudiants = Column(Float, nullable=True)
    inactifs = Column(Float, nullable=True)

    # --- Age groups ---
    age_15_24 = Column("age_15_24_ans", Float, nullable=True)
    age_25_39 = Column("age_25_39_ans", Float, nullable=True)
    age_40_54 = Column("age_40_54_ans", Float, nullable=True)
    age_55_64 = Column("age_55_64_ans", Float, nullable=True)
    age_65_79 = Column("age_65_79_ans", Float, nullable=True)
    age_80_plus = Column("age_80_ans_et_plus", Float, nullable=True)

    maries = Column(Float, nullable=True)
    pacses = Column(Float, nullable=True)
    concubinage = Column(Float, nullable=True)
    veufs = Column(Float, nullable=True)
    divorces = Column(Float, nullable=True)
    celibataires = Column(Float, nullable=True)


    personne_seule = Column(Float, nullable=True)
    homme_seul = Column(Float, nullable=True)
    femme_seule = Column(Float, nullable=True)
    colocation = Column(Float, nullable=True)
    famille = Column(Float, nullable=True)
    famille_monoparentale = Column(Float, nullable=True)
    couple_sans_enfant = Column(Float, nullable=True)
    couple_avec_enfants = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint("code_insee", "annee", name="uq_commune_annee"),
    )

    def __repr__(self) -> str:
        return f"<CommuneStats code_insee={self.code_insee!r} annee={self.annee}>"


class PredictionResult(Base):
    """
    Audit log of every prediction made via the API.
    """
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code_insee = Column(String(10), nullable=False, index=True)
    prediction = Column(String(20), nullable=False)          
    predicted_label_index = Column(Integer, nullable=False)  
    model_version = Column(String(100), nullable=True)       