def upsert_reviews(engine, df):
    df.to_sql(
        "review",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
    )
