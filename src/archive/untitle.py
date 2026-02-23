from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def open_and_click_review(place_id: str, timeout: int = 15, headless: bool = False):
    """
    네이버 플레이스(모바일) 매장 홈에서 '리뷰' 탭을 클릭해 리뷰 페이지 이동.
    예: place_id = '2007321729'
    """

    url = f'https://m.place.naver.com/hairshop/{place_id}/home'

    # 크롬을 자동화에 맞게 안정적으로/일관되게 실행시키는 설정 모음
    chrome_options = Options() 

    # headless가 True일 때만 "창 없이 실행하는 모드"를 켜라 
    if headless:
        # 크롬 창을 띄우지 말고 실행하라
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox") # 크롬 샌드박스 비활성화 (리눅스/도커 환경에서 실행 오류 방지)
    chrome_options.add_argument("--disable-dev-shm-usage") # /dev/shm 대신 디스크 사용 (메모리 부족으로 크롬이 죽는 문제 방지)
    chrome_options.add_argument("--window-size=1280,900") # 브라우저 화면 크기 고정 (반응형 레이아웃 변화 방지)

    # 실제 크롬 브라우저를 실행 + 제어 가능 상태로 만듦
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), # 크롬을 조종할 chromedriver를 자동으로 설치/연결
        options=chrome_options # 크롬 옵션
    )

    wait = WebDriverWait(driver, timeout)
    # 크롬 드라이버가 크롬 브라우저에게 “이 URL로 이동해라”라고 명령한 것입니다.
    driver.get(url)

    # 1) "리뷰"라는 텍스트를 가진 탭/링크 클릭 (가장 직관적)
    try:
        # 조건이 만족될 때까지 반복 체크
        review_tab = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/review']")) # EC: 무엇이 되면 기다림을 끝낼지
        )
        review_tab.click()
    except Exception:
        # 2) 텍스트 클릭이 막힐 때: href에 review가 포함된 링크를 찾아 클릭
        review_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//span[normalize-space()='리뷰']]"))
        )
        review_tab.click()

    # 리뷰 페이지 로딩 확인: URL에 /review 가 포함될 때까지 대기
    wait.until(lambda d: "/review" in d.current_url)

    return driver


if __name__ == "__main__":
    driver = open_and_click_review(place_id="2007321729", headless=False)
    print("현재 URL:", driver.current_url)
    input("엔터를 누르면 브라우저를 종료합니다...")
    # driver.quit()