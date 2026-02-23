from selenium.webdriver.common.by import By
import re


def extract_visit_meta(card):
    """
    리뷰 카드 하나에서
    방문 관련 메타 정보 추출

    반환:
        {
            "visit_date": str | None,
            "visit_count": int | None,
            "is_reserved": bool
        }
    """

    meta = {
        "visit_date": None,
        "visit_count": None,
        "is_reserved": False,
    }

    try:
        container = card.find_element(
            By.CSS_SELECTOR,
            "div.pui__QKE5Pr"
        )

        # 날짜는 blind span에서만 추출
        blind_spans = container.find_elements(
            By.CSS_SELECTOR,
            "span.pui__blind"
        )

        for span in blind_spans:
            text = span.text.strip()

            # 실제 날짜 문자열만 채택
            if re.search(r"\d{4}년\s*\d+월\s*\d+일", text):
                meta["visit_date"] = text
                break

        # 나머지 정보는 기존 방식
        gfu_spans = container.find_elements(
            By.CSS_SELECTOR,
            "span.pui__gfuUIT"
        )

        for span in gfu_spans:
            text = span.text.strip()

            if "번째 방문" in text:
                m = re.search(r"\d+", text)
                if m:
                    meta["visit_count"] = int(m.group())

            elif "예약" in text:
                meta["is_reserved"] = True

    except Exception:
        pass

    return meta
