from selenium.webdriver.common.by import By


def extract_review_keywords(card):
    """
    리뷰 카드 하나에서
    선택된 키워드들을 리스트로 추출

    반환:
        List[str]
        - 키워드 없으면 []
    """

    keywords = []

    try:
        keyword_spans = card.find_elements(
            By.CSS_SELECTOR,
            "span.pui__jhpEyP"
        )

        for span in keyword_spans:
            text = span.text.strip()
            if text:
                keywords.append(text)

    except Exception:
        # 키워드 영역 자체가 없는 경우
        pass

    return keywords
