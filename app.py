from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

app = Flask(__name__)

# ✅ Chrome Options for Headless Mode on Render
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # ✅ Headless mode (No GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def scrape_vehicle_details(reg_number):
    """Scrapes vehicle details from Parivahan website"""

    # ✅ Auto-install ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://vahan.parivahan.gov.in/nrservices/faces/user/searchstatus.xhtml")
        time.sleep(3)  # Wait for page to load

        # ✅ Enter Vehicle Number
        search_box = driver.find_element(By.ID, "regn_no1_exact")
        search_box.send_keys(reg_number)
        search_box.send_keys(Keys.RETURN)

        time.sleep(5)  # Allow data to load

        # ✅ Extract Details
        vehicle_info = {}

        try:
            vehicle_info["Vehicle Number"] = reg_number
            vehicle_info["Owner Name"] = driver.find_element(By.XPATH, "//td[contains(text(),'Owner Name')]/following-sibling::td").text
            vehicle_info["Registration Date"] = driver.find_element(By.XPATH, "//td[contains(text(),'Registration Date')]/following-sibling::td").text
            vehicle_info["Vehicle Model"] = driver.find_element(By.XPATH, "//td[contains(text(),'Maker / Model')]/following-sibling::td").text
            vehicle_info["Fuel Type"] = driver.find_element(By.XPATH, "//td[contains(text(),'Fuel Type')]/following-sibling::td").text
        except:
            return {"error": "Vehicle details not found or CAPTCHA detected"}

        return vehicle_info

    finally:
        driver.quit()

@app.route('/')
def home():
    return jsonify({"message": "Server is running!"})

@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    reg_number = request.args.get('reg_number')

    if not reg_number:
        return jsonify({"error": "Please provide a vehicle registration number!"}), 400

    vehicle_data = scrape_vehicle_details(reg_number)
    return jsonify(vehicle_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # ✅ Render ke liye port set karo
    app.run(host="0.0.0.0", port=port, debug=True)
