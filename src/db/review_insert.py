def upsert_reviews(engine, df):
    df.to_sql(
        "review",
        con=engine,
        schema="raw",
        if_exists="append",
        index=False,
        method="multi",
    )
