import numpy as np
import pandas as pd

cd = pd.read_csv("all.csv")
# 1️⃣ Remplacer les valeurs NaN par des valeurs adaptées
cd.fillna({
    "category": "Inconnu",  # Catégorie manquante remplacée par "Inconnu"
    "ligue": "Non spécifié",
    "type": "Non spécifié",
}, inplace=True)

# 2️⃣ Remplacement des NaN dans les colonnes numériques par 0 (ou une autre valeur pertinente)
cd["Minute_Time"].fillna(0, inplace=True)
cd["distance"].fillna(0, inplace=True)
cd["vitesse"].fillna(0, inplace=True)

# 3️⃣ Vérification et conversion des dates
cd["competition_date"] = pd.to_datetime(cd["competition_date"], errors="coerce")  # Convertit en format datetime

# 4️⃣ Suppression des lignes avec des valeurs critiques manquantes (optionnel)
cd.dropna(subset=["competition_name", "athlete", "club"], inplace=True)

# 5️⃣ Transformer les types pour correspondre aux attentes d'Elasticsearch
cd["department"] = cd["department"].astype(str)  # Elasticsearch attend souvent un string pour les codes de département

# 6️⃣ Remplacer les valeurs NaN restantes par une chaîne vide (évite les erreurs)
cd = cd.replace({np.nan: ""})

cd.to_csv('all2.csv', index=False)
