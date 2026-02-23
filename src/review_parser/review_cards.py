from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_review_cards(driver):
    """
    현재 DOM에 로딩된 리뷰 카드(li) 리스트 반환
    """
    timeout = 10
    
    wait = WebDriverWait(driver, timeout)

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "li.place_apply_pui.EjjAW")
        )
    )

    cards = driver.find_elements(
        By.CSS_SELECTOR,
        "li.place_apply_pui.EjjAW"
    )

    return cards