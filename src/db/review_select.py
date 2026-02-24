from sqlalchemy import text

def get_recent_hashes(engine, limit: int = 300) -> set:
    query = text("""
        SELECT review_hash
        FROM raw.review
        ORDER BY created_at DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})
        return {row[0] for row in result}