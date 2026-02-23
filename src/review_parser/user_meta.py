from selenium.webdriver.common.by import By
import re


def extract_user_meta(card):
    """
    리뷰 카드 하나에서
    유저 메타 정보(팔로워 수, 리뷰 수, 사진 수)를 추출한다.

    반환 예:
        {
            "followers": int | None,
            "review_count": int | None,
            "photo_count": int | None
        }
    """

    meta = {
        "followers": None,
        "review_count": None,
        "photo_count": None,
    }

    try:
        # 메타 정보가 모여 있는 span들
        meta_spans = card.find_elements(
            By.CSS_SELECTOR,
            "span.pui__WN-kAf"
        )

        for span in meta_spans:
            text = span.text.strip()
            if not text:
                continue

            # 숫자 추출
            match = re.search(r"\d+", text)
            if not match:
                continue

            value = int(match.group())

            # 키워드 기준 분기
            if "팔로워" in text:
                meta["followers"] = value
            elif "리뷰" in text:
                meta["review_count"] = value
            elif "사진" in text:
                meta["photo_count"] = value

    except Exception:
        # 메타 영역 자체가 없는 경우 → 전부 None 유지
        pass

    return meta
