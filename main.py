import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# راه‌اندازی مرورگر
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # حالت بدون رابط گرافیکی
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    url = "https://hamrahtel.com/products/poco-m6-pro-256gb-ram-8gb"
    driver.get(url)

    # منتظر بمان تا عنصر مشخص‌شده تا حداکثر 30 ثانیه ظاهر شود
    selector = ".mantine-ll7qhg"
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )

    text_output = element.text
    print("مقدار متن:", text_output)

    # مسیر فایل خروجی
    output_dir = "results"
    output_path = os.path.join(output_dir, "output.txt")

    # اگر پوشه وجود نداشت، آن را بساز
    os.makedirs(output_dir, exist_ok=True)

    # ذخیره در فایل متنی
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text_output)

finally:
    driver.quit()
