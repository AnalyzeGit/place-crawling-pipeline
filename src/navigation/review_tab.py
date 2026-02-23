from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_review_tab(
    driver,
    place: str,
    place_id: str,
    timeout: int = 15
):
    """
    네이버 플레이스(모바일) 매장 홈에서
    '리뷰' 탭을 클릭해 리뷰 페이지로 이동시키는 함수

    - driver: 이미 생성된 selenium driver
    - place_id: 네이버 플레이스 매장 ID
    - timeout: 대기 시간
    """

    url = f"https://m.place.naver.com/{place}/{place_id}/home"
    wait = WebDriverWait(driver, timeout)

    # 크롬 드라이버가 크롬 브라우저에게 “이 URL로 이동해라”라고 명령한 것입니다.
    driver.get(url)

    # 1순위: href에 '/review'가 포함된 링크 클릭 (가장 안정적)
    try:
        review_tab = wait.until(
            EC.element_to_be_clickable( 
                (By.CSS_SELECTOR, "a[href*='/review']") # EC: 무엇이 되면 기다림을 끝낼지
            )
        )
        review_tab.click()

    # 2순위: 텍스트 '리뷰' 기반 XPath
    except Exception:
        review_tab = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[.//span[normalize-space()='리뷰']]")
            )
        )
        review_tab.click()

    # 리뷰 페이지 진입 확인
    wait.until(lambda d: "/review" in d.current_url)

    return driver
