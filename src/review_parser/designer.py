from selenium.webdriver.common.by import By


def extract_designer_name(card):
    """
    리뷰 카드 하나에서
    미용사(디자이너) 이름 추출

    반환:
        str | None
    """
    try:
        return card.find_element(
            By.CSS_SELECTOR,
            "span.pui__ETqMYH"
        ).text.strip()
    except Exception:
        # 디자이너 정보가 없는 리뷰 카드도 있음
        return None
