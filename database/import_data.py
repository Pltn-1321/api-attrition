import pandas as pd
from sqlalchemy import create_engine

# Ton import actuel
df = pd.read_csv("data/export-api/test_employees.csv")
df.insert(0, "id", range(1, len(df) + 1))
engine = create_engine(
    "postgresql://attrition_user:attrition_pass@localhost:5432/attrition_db"
)
df.to_sql("employees", engine, if_exists="replace", index=False)

print(f"✅ {len(df)} employés importés dans PostgreSQL")

# VÉRIFICATION : relire depuis la DB
df_check = pd.read_sql("SELECT * FROM employees LIMIT 10", engine)
print("\n📊 Aperçu des données dans PostgreSQL :")
print(df_check)
print(
    f"\nNombre total de lignes : {pd.read_sql('SELECT COUNT(*) FROM employees', engine).iloc[0, 0]}"
)
