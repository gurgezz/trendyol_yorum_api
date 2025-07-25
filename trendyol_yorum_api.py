import time
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(trendyol_yorum_api)
def trendyol_yorumlari_cek(https://www.trendyol.com/tuval/kisiye-ozel-sayilarla-boyama-seti-25x35-yildonumu-dogum-gunu-etkinlik-kendin-yap-p-900748915/yorumlar, yorum_sayisi=50):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(https://www.trendyol.com/tuval/kisiye-ozel-sayilarla-boyama-seti-25x35-yildonumu-dogum-gunu-etkinlik-kendin-yap-p-900748915/yorumlar)
    time.sleep(5)
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    yorumlar = driver.find_elements(By.CLASS_NAME, "comment")
    yorum_listesi = []
    for yorum in yorumlar[:yorum_sayisi]:
        try:
            try:
                ad = yorum.find_element(By.CSS_SELECTOR, ".user-info > span").text.strip()
            except:
                ad = "Anonim"
            try:
                yazi = yorum.find_element(By.CLASS_NAME, "comment-text").text.strip()
            except:
                yazi = ""

            try:
                tarih = yorum.find_element(By.CLASS_NAME, "comment-date").text.strip()
            except:
                tarih = ""
            try:
                star_div = yorum.find_element(By.CLASS_NAME, "rating-star")
                style = star_div.get_attribute("style")
                rating = int(float(style.split(":")[1].replace("%", "").replace(";", "").strip()) / 20)
            except:
                rating = None
            try:
                img_tags = yorum.find_elements(By.CSS_SELECTOR, ".comment-images img")
                img_urls = [img.get_attribute("src") for img in img_tags if img.get_attribute("src")]
                resim_url_str = ", ".join(img_urls)
            except:
                resim_url_str = ""

            yorum_listesi.append({
                "Reviewer Name": ad,
                "Rating": rating,
                "Review Body": yazi,
                "Review Date": tarih,
                "Review Photo URLs": resim_url_str
            })
        except Exception as e:
            continue
    driver.quit()
    return yorum_listesi
@app.route('/yorumlar')
def yorumlar_endpoint():
    URUN_URL = "https://www.trendyol.com/tuval/kisiye-ozel-sayilarla-boyama-seti-25x35-yildonumu-dogum-gunu-etkinlik-kendin-yap-p-900748915/yorumlar"
    yorumlar = trendyol_yorumlari_cek(https://www.trendyol.com/tuval/kisiye-ozel-sayilarla-boyama-seti-25x35-yildonumu-dogum-gunu-etkinlik-kendin-yap-p-900748915/yorumlar, yorum_sayisi=50)
    return jsonify(yorumlar)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
