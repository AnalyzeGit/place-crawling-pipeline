from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless: bool = False):
    """
    Selenium Chrome Driver 생성 전용 함수
    - 브라우저 옵션 설정
    - chromedriver 자동 설치 및 연결
    - driver 객체 반환
    """

    # 크롬을 자동화에 맞게 안정적으로/일관되게 실행시키는 설정 모음
    chrome_options = Options()

    # headless 모드 설정 (True일 때만 창 없이 실행)
    if headless:
        # 크롬 창을 띄우지 말고 실행하라
        chrome_options.add_argument("--headless=new")

    # 크롤링 안정화 옵션
    chrome_options.add_argument("--no-sandbox") # 크롬 샌드박스 비활성화 (리눅스/도커 환경에서 실행 오류 방지)
    chrome_options.add_argument("--disable-dev-shm-usage") # /dev/shm 대신 디스크 사용 (메모리 부족으로 크롬이 죽는 문제 방지)
    chrome_options.add_argument("--window-size=1280,900") # 브라우저 화면 크기 고정 (반응형 레이아웃 변화 방지)

    # 실제 크롬 브라우저를 실행 + 제어 가능 상태로 만듦
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), # 크롬을 조종할 chromedriver를 자동으로 설치/연결
        options=chrome_options # 크롬 옵션
    )

    return driver
