from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def scrape_reviews(url):
    """
    Scrapes Amazon reviews from a given product URL using Selenium.

    Args:
        url (str): Amazon product page URL.

    Returns:
        dict: Contains 'reviews' (list of scraped reviews) and 'category' (product category).
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  

        
        category = "Unknown"
        category_selectors = [
            "#wayfinding-breadcrumbs_feature_div ul li span.a-list-item",  
            "#wayfinding-breadcrumbs_container ul li span",                
            "#wayfinding-breadcrumbs_feature_div a"                        
        ]

        for selector in category_selectors:
            try:
                category_element = driver.find_element(By.CSS_SELECTOR, selector)
                if category_element.text.strip():
                    category = category_element.text.strip()
                    break
            except:
                continue

        
        try:
            all_reviews_link = driver.find_element(By.PARTIAL_LINK_TEXT, "See all reviews")
            all_reviews_link.click()
            time.sleep(2)
        except:
            pass  

        
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        review_elements = driver.find_elements(By.CSS_SELECTOR, ".review-text-content span")
        reviews = [element.text.strip() for element in review_elements if element.text.strip()]

        if not reviews:
            return {"error": "No reviews found on this page."}

        return {"reviews": reviews, "category": category}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()
