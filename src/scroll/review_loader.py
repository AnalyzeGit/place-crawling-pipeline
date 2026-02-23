from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def click_visible_buttons(driver, css_selector, sleep_sec=0.2):
    buttons = driver.find_elements(By.CSS_SELECTOR, css_selector)
    for btn in buttons:
        try:
            if btn.is_displayed():
                btn.click()
                time.sleep(sleep_sec)
        except Exception:
            continue


def load_all_reviews(driver, timeout: int = 10, sleep_sec: float = 1.0):
    """
    리뷰 페이지에서
    - 스크롤
    - 하단 '더보기'
    - 카드 내부 '+N(키워드 더보기)'

    를 반복하여
    더 이상 펼칠 수 없을 때까지 DOM을 완성한다.

    반환값 없음 (driver 상태만 변경)
    """

    wait = WebDriverWait(driver, timeout)
    last_height = 0

    while True:
        current_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        # 현재 화면에 보이는 키워드 +N 버튼 전부 클릭
        click_visible_buttons(
            driver,
            "a[data-pui-click-code='keywordmore']"
        )

        click_visible_buttons(
            driver,
            "a[data-pui-click-code='rvshowmore']"
        )
        if current_height == last_height:
            try:
                # 1️⃣ '펼쳐서 더보기' 텍스트(span)를 기준으로 찾고
                more_span = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "a[role='button'] span.TeItc")
                    )
                )

                # 2️⃣ 실제 클릭 대상인 부모 a로 이동해서 클릭
                more_button = more_span.find_element(By.XPATH, "..")
                more_button.click()

                time.sleep(sleep_sec)

            except Exception:
                # 더보기 버튼도 없고, 높이 변화도 없음 → 종료
                break
        else:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(sleep_sec)
            last_height = current_height