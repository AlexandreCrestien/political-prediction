from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.model.communes import Communes

class CommuneService:
    @staticmethod
    def get_by_insee(db: Session, code_insee: str, year: str = None):
        query = select(Communes).where(Communes.code_insee == code_insee)
        if year:
            query = query.where(Communes.years == year)
        
        result = db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None):
        # Base des requêtes
        total_query = select(func.count()).select_from(Communes)
        data_query = select(Communes)

        # Application du filtre de recherche si présent
        if search and search.lower() not in ["none", "null", ""]:
            # .ilike(f"%{search}%") cherche les noms contenant la chaîne
            filter_stmt = Communes.city.ilike(f"%{search}%")
            total_query = total_query.where(filter_stmt)
            data_query = data_query.where(filter_stmt)

        # 1. Compter le total
        total = db.execute(total_query).scalar() or 0

        # 2. Récupérer les données avec pagination
        data_query = data_query.offset(skip).limit(limit)
        data = db.execute(data_query).scalars().all()

        return total, data
    
    @staticmethod
    def get_by_department(db: Session, department_code: str, year: str = None):
        query = select(Communes).where(Communes.code_insee.startswith(department_code))
        if year:
            query = query.where(Communes.years == year)
        
        result = db.execute(query)
        return result.scalars().all()