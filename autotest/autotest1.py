import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


def test_card_block_count(driver):
    url = "https://www.demoblaze.com/"
    expected_count = 2 # [file:1]

    driver.get(url)
    monitor_click = driver.find_element(By.XPATH, "//a [text()='Monitors']")
    monitor_click.click()
    wait = WebDriverWait(driver, 10)

    # ждем, что на странице появится текст 'Apple monitor 24'
    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "tbodyid"), "Apple monitor 24"
        )
    )  # [web:26][web:30][web:32]

    # ищем все элементы с классом 'card-block'
    cards = driver.find_elements(By.CLASS_NAME, "card-block")  # [web:1][web:2][web:9]

    assert len(cards) == expected_count, (
        f"Ожидалось {expected_count} элементов с классом 'card-block', "
        f"но найдено {len(cards)}"
    )