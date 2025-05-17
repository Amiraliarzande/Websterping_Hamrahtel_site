from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json

def extract_product_data(url: str, output_file: str = "output.json") -> dict:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".mantine-ll7qhg"))
        )

        container = driver.find_element(By.CSS_SELECTOR, ".mantine-ll7qhg")
        html = container.get_attribute("innerHTML")

        soup = BeautifulSoup(html, "html.parser")
        result = {}

        blocks = soup.select(".mantine-1meq30c")
        for block in blocks:
            color_tag = block.select_one(".mantine-rj9ps7")
            color = color_tag.text.strip() if color_tag else "نامشخص"
            
            price_tag = block.select_one(".mantine-1erraa9")
            price = price_tag.text.strip() if price_tag else None

            old_price_tag = block.select_one(".mantine-vpcnae")
            old_price = old_price_tag.text.strip() if old_price_tag else None

            discount_tag = block.select_one(".mantine-1fdpe25")
            discount = discount_tag.text.strip() if discount_tag else None

            result[color] = {
                "قیمت": price,
                "قیمت بدون تخفیف": old_price,
                "تخفیف": discount
            }
            

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print("✅ success")
        return result

    finally:
        driver.quit()





if __name__ == "__main__":
    url = "https://hamrahtel.com/products/aura-studio-model-3-bluetooth-speaker"
    data = extract_product_data(url)
    
