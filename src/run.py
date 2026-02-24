import pandas as pd

from config.settings import DB_CONN_URI
from browser.driver import create_driver
from scroll.review_loader import load_all_reviews
from navigation.review_tab import open_review_tab
from utils.review_hash import generate_review_hash
from db.connection import get_engine
from db.review_select import get_recent_hashes
from db.review_insert import upsert_reviews
from review_parser.review_cards import get_review_cards
from review_parser.designer import extract_designer_name
from review_parser.reviewer_id import extract_reviewer_id
from review_parser.review_text import extract_review_text
from review_parser.review_keywords import extract_review_keywords
from review_parser.visit_meta import extract_visit_meta
from review_parser.user_meta import extract_user_meta


def main():
    place = 'hairshop'
    place_id = "2007321729" # 크롤링 페이지 설정 (진입점)

    # 엔진 생성
    engine = get_engine(DB_CONN_URI)

    # 최근 hash 로드
    existing_hashes = get_recent_hashes(engine, limit=50)

    # 크롬 드라이버 생성
    driver = create_driver(headless=False)

    # 리뷰 탭으로 이동
    open_review_tab(driver, place=place, place_id=place_id)

    # 스크롤 내리기
    load_all_reviews(driver)

    # 리뷰 카드 추출
    cards = get_review_cards(driver)

    rows = []
    for card in cards:
        row = {
            "name": extract_reviewer_id(card),
            "designer": extract_designer_name(card),
            "review_text": extract_review_text(card),
            "keywords": extract_review_keywords(card),
            **extract_visit_meta(card),
            **extract_user_meta(card),
        }

        # hash 생성
        review_hash = generate_review_hash(
            review_text=row["review_text"],
            visit_date=row.get("visit_date"),
            designer=row["designer"],
        )

        # 
        if review_hash is None:
            continue    

        # 중단 조건
        if review_hash in existing_hashes:
            print("기존 데이터 발견 → 중단")
            break

        row["review_hash"] = review_hash

        rows.append(row)

    df = pd.DataFrame(rows)
    # df.to_csv('naver_place_2007321729.csv', index=False, encoding='utf-8-sig')

    # 데이터 적재 
    upsert_reviews(engine, df)

    # 5. 결과 확인 (디버깅용)
    print("현재 URL:", driver.current_url)
    input("엔터를 누르면 브라우저를 종료합니다...")

    driver.quit()


if __name__ == "__main__":
    main()
