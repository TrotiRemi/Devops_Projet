import pandas as pd

# Liste des colonnes à garder (celles qui sont dans Elasticsearch)
columns_to_keep = [
    "competition_name", "distance", "Minute_Time", "athlete", "club",
    "category", "department", "competition_date", "vitesse", "type",
    "type_course", "location", "ligue"
]

# Charger uniquement ces colonnes, en forçant les types
df = pd.read_csv("all.csv", usecols=columns_to_keep, dtype=str, low_memory=False)

# Convertir les colonnes qui doivent être des nombres
df["distance"] = pd.to_numeric(df["distance"], errors='coerce')
df["Minute_Time"] = pd.to_numeric(df["Minute_Time"], errors='coerce')
df["vitesse"] = pd.to_numeric(df["vitesse"], errors='coerce')

# Convertir les dates
df["competition_date"] = pd.to_datetime(df["competition_date"], errors='coerce')

# Sauvegarder le CSV nettoyé
df.to_csv("all2.csv", index=False)
