from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_reviewer_ids(driver):
    """
    현재 리뷰 페이지에 로딩된 리뷰들에서
    작성자 아이디(이름)만 추출

    반환값:
        List[str]
    """
    wait = WebDriverWait(driver, 15)

    #  핵심: 작성자 span이 나타날 때까지 대기
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span.pui__NMi-Dp")
        )
    )

    reviewer_ids = []

    print('ID 추출을 진행합니다.')

    # 작성자 이름이 들어있는 span들을 모두 선택
    name_elements = driver.find_elements(
        By.CSS_SELECTOR,
        "span.pui__NMi-Dp"
    )

    for elem in name_elements:
        reviewer_ids.append(elem.text.strip())
    
    print(f'name_elements: {name_elements}')
    print('ID 추출을 끝났습니다.')

    return reviewer_ids


def extract_reviewer_id(card):
    """
    리뷰 카드 하나에서
    작성자 아이디(이름) 추출
    """
    try:
        return card.find_element(
            By.CSS_SELECTOR,
            "span.pui__NMi-Dp"
        ).text.strip()
    except Exception:
        return None
