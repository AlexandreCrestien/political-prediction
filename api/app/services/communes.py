from sqlalchemy.orm import Session
from sqlalchemy import select
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
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Communes).offset(skip).limit(limit).all()