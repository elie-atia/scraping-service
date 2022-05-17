# main.py

from flask import Flask, send_file, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary  # Adds chromedriver binary to path
from webdriver_manager.chrome import ChromeDriverManager
import time
from parsel import Selector
from selenium.webdriver.common.by import By

app = Flask(__name__)
mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
# The following options are required to make headless Chrome
# work in a Docker container
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')        
chrome_options.add_experimental_option(
    "mobileEmulation", mobile_emulation)
# Initialize a new browser
browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

BASE_URL = "https://www.google.com/maps/search/{search}/?hl=en"
SEARCH = "Movers+Miami"
FINAL_URL = BASE_URL.format(search=SEARCH)

@app.route("/")
def hello_world():
    browser.get("https://google.com")
    file_name = 'test.png'
    browser.save_screenshot(file_name)
    browser.quit()
    return send_file(file_name)

@app.route("/send_msg")
def send_msg():
    browser.get(FINAL_URL)
    time.sleep(10)
    page_content = browser.page_source
    response = Selector(page_content)
    #print('resonse variable is:',response)
    results = []
    time.sleep(5)
    response_el = response.xpath('//div[contains(@aria-label, "Results for")]/div/div[./a]')
    for el in response_el:
        #print("element append in result array")
        results.append({
            'link': el.xpath('./a/@href').extract_first(''),
            'title': el.xpath('./a/@aria-label').extract_first('')
    })
    file_name = ''
    for item in results:
        browser.get(item.get('link'))
        share_element = browser.find_element(By.XPATH, "//button[contains(@data-value, 'Share')]")
        share_element.click()
        time.sleep(2)
        file_name = 'test.png'
        browser.save_screenshot(file_name)
        return send_file(file_name)
        time.sleep(1)
    #print('RESULT ARRAY',results)
    time.sleep(10)
    browser.get('https://www.google.com/maps/place/Pro+Movers+Miami/data=!4m6!3m5!1s0x88d9b69d4a401a45:0x61c86ad507a75d03!8m2!3d25.769079!4d-80.188602!16s%2Fg%2F1td1qpj4?authuser=0&hl=en&rclk=1')
    # chat_element = browser.find_element(By.XPATH, "//button[contains(@data-value, 'Chat')]")
    # chat_element.click()
    
    browser.quit()
    return send_file(file_name)
    #return jsonify(results)
    #return page_content
   
    
   
    # browser.quit()
    # return 'send_msg ok'