import os
import pandas as pd

print("Current Working Directory:", os.getcwd())

files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
print("Excel files found in CWD:", files)

target_lotofacil = "Lotofácil-resultados-30-12-2025.xlsx"
target_megasena = "Mega-Sena_resultados-30-12-2025.xlsx"

print(f"Checking {target_lotofacil}: Exists? {os.path.exists(target_lotofacil)}")
print(f"Checking {target_megasena}: Exists? {os.path.exists(target_megasena)}")

# Try loading
try:
    df = pd.read_excel(target_lotofacil)
    print(f"Successfully loaded {target_lotofacil}. Columns: {df.columns[:5]}")
except Exception as e:
    print(f"Failed to load {target_lotofacil}: {e}")
