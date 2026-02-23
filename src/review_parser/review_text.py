from selenium.webdriver.common.by import By


def extract_review_text(card):
    """
    리뷰 카드 하나에서
    사용자가 작성한 리뷰 본문 전체를 추출

    반환:
        str | None
    """
    try:
        review_elem = card.find_element(
            By.CSS_SELECTOR,
            "div.pui__vn15t2 a[data-pui-click-code='rvshowless']"
        )

        # <br> 태그는 Selenium에서 줄바꿈으로 자동 변환됨
        return review_elem.text.strip()

    except Exception:
        # 리뷰가 없는 경우는 거의 없지만 방어
        return None
