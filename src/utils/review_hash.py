import hashlib


def generate_review_hash(
    review_text: str,
    visit_date: str,
    designer: str,
) -> str:
    """
    리뷰 고유 식별용 해시 생성
    """

    raw = f"{review_text.strip()}|{visit_date}|{designer}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
