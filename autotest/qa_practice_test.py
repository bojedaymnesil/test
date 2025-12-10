import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(5)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_text_input(driver):
    main_url = "https://www.qa-practice.com/"
    driver.get(main_url)
    wait = WebDriverWait(driver, 5)

    #1. Ждём пока увидим элемент Text input и кликаем на него
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[@href='/elements/input/simple']")
    ))
    #2. Кликаем на ссылку, ведущую к Text input'у
    driver.find_element (By.XPATH, "//a[@href='/elements/input/simple']").click()

    #3. Ищем поле ввода текста и вводим текст
    input_field = wait.until(
        EC.element_to_be_clickable((By.ID, "id_text_string"))
    )
    text_inside_field = "Hello"

    input_field.click()
    input_field.send_keys(text_inside_field)
    input_field.send_keys(Keys.RETURN)

    #4. Проверка выведенного текста

    wait.until(EC.visibility_of_element_located(
        (By.ID, "result")
    ))

    sravnenie = driver.find_element (By.ID, "result")

    assert text_inside_field in sravnenie.text