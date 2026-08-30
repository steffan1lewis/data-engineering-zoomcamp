import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://root:root@localhost:5432/ny_taxi"
)

df = pd.read_csv("taxi_zone_lookup.csv")

print(df.head())
print(f"Rows: {len(df)}")

df.to_sql(
    name="zones",
    con=engine,
    if_exists="replace",
    index=False
)

print("Zones table created!")
