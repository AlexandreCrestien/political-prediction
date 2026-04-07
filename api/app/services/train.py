import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from app.schemas.train import TrainSettings

class TrainService:
    @staticmethod
    def run_pipeline(settings: TrainSettings, db_engine):
        try:
            # 1. Extraction
            query = "SELECT * FROM training"
            df = pd.read_sql(query, db_engine)

            if df.empty:
                print("--- ERROR: Table 'training' vide ---")
                return

            # 2. Nettoyage / Filtre (Méthode Drop pour la qualité)
            df_clean = df[
                (df['Population_active'] > 0) & 
                (df['Population avec enfants'] > 0)
            ].copy()

            # 3. Préparation X et y
            X = df_clean.drop(columns=['Code_INSEE', 'Résultat'])
            y = df_clean['Résultat']

            # 4. Split Train/Test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=settings.test_size, random_state=42
            )

            # 5. Entraînement
            model = RandomForestClassifier(
                n_estimators=settings.n_estimators,
                random_state=42
            )
            model.fit(X_train, y_train)

            # 6. Sauvegarde
            # Création du dossier models s'il n'existe pas
            os.makedirs("saved_models", exist_ok=True)
            model_path = os.path.join("saved_models", settings.model_name)
            
            joblib.dump(model, model_path)

            accuracy = model.score(X_test, y_test)
            print(f"--- TRAINING SUCCESS ---")
            print(f"Modèle sauvegardé : {model_path}")
            print(f"Précision (Test Set) : {accuracy:.4f}")

        except Exception as e:
            print(f"--- TRAINING FAILED: {str(e)} ---")