import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(10)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_banner_finuslugi_click_and_redirect(driver):
    registration_url = "https://lk.finuslugi.ru/registration"

    # Шаг 1: заходим на страницу регистрации
    driver.get(registration_url)

    wait = WebDriverWait(driver, 20)

    # Шаг 2: ждём появления баннера по data-qa
    banner = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-qa='registration-promo-banner']")
        )
    )

    # Ждём, что баннер видим
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "[data-qa='registration-promo-banner']")
    ))

    # Шаг 3: получаем количество вкладок ДО клика
    current_window = driver.current_window_handle
    windows_before = driver.window_handles

    # Кликаем на баннер
    try:
        banner_link = banner.find_element(By.TAG_NAME, "a")
        banner_link.click()
    except:
        driver.execute_script("arguments[0].click();", banner)

    # Ждём, пока появится новая вкладка
    wait.until(EC.number_of_windows_to_be(len(windows_before) + 1))

    # Переходим на новую вкладку
    new_window = [w for w in driver.window_handles if w not in windows_before][0]
    driver.switch_to.window(new_window)

    # Шаг 4: ждём загрузки страницы и проверяем URL
    wait.until(EC.url_contains("promo.finuslugi.ru"))

    current_url = driver.current_url
    assert "promo.finuslugi.ru" in current_url, \
        f"Переход на promo не выполнен. URL: {current_url}"