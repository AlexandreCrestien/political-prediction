from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_
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
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None, light: bool = False):
        if light:
            # On sélectionne uniquement les deux colonnes
            data_query = select(Communes.code_insee, Communes.city).distinct()
        else:
            data_query = select(Communes)

        total_query = select(func.count()).select_from(Communes)

        if search and search.strip():
            filter_stmt = or_(
                Communes.city.ilike(f"%{search}%"),
                Communes.code_insee.ilike(f"{search}%")
            )
            total_query = total_query.where(filter_stmt)
            data_query = data_query.where(filter_stmt)

        total = db.execute(total_query).scalar() or 0
        data_query = data_query.offset(skip).limit(limit)
        
        result = db.execute(data_query)
        
        if light:
            # mappings().all() transforme les lignes en dictionnaires {'code_insee': ..., 'city': ...}
            return total, result.mappings().all()
        
        return total, result.scalars().all()
    
    @staticmethod
    def get_by_department(db: Session, department_code: str, year: str = None, light: bool = False):
        if light:
            # Mode Carte : Sélection restreinte pour alléger les données
            query = select(
                Communes.code_insee, 
                Communes.city, 
                Communes.pct_gauche, 
                Communes.pct_centre,
                Communes.pct_droite,
                Communes.years
            )
        else:
            # Mode Tableau : Object complet (Toutes les colonnes + JSON)
            query = select(Communes)
        # Filtres communes
        query = select(Communes).where(Communes.code_insee.startswith(department_code))
        if year:
            query = query.where(Communes.years == year)

        result = db.execute(query)

        if light:
            # Pour la sélection de colonnes, on renvoie des dictionnaires
            return [dict(row) for row in result.mappings().all()]
        # Pour l'objet complet, on renvoie les instances du modèle
        return result.scalars().all()
    
    
    @staticmethod
    def get_by_region(db: Session, department_codes: list[str], year: str = "2022"):
        """
        Récupère toutes les communes pour une liste de départements (une région).
        department_codes ex: ['59', '62'] pour les Hauts-de-France (partiel)
        """
        # Construction d'une clause OR pour chaque département
        filters = [Communes.code_insee.startswith(code) for code in department_codes]
        
        query = select(Communes).where(or_(*filters))
        if year:
            query = query.where(Communes.years == year)
            
        result = db.execute(query)
        return result.scalars().all()