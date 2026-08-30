import argparse

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--db', required=True)
    parser.add_argument('--table_name', required=True)
    parser.add_argument('--url', required=True)

    args = parser.parse_args()

    engine = create_engine(
        f'postgresql+psycopg://{args.user}:{args.password}@'
        f'{args.host}:{args.port}/{args.db}'
    )

    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]

    df_iter = pd.read_csv(
        args.url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )

    first = True

    for df_chunk in tqdm(df_iter):

        if first:
            df_chunk.head(0).to_sql(
                name=args.table_name,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        df_chunk.to_sql(
            name=args.table_name,
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))


if __name__ == '__main__':
    main()
