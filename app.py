from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def scrape_vehicle_details(reg_number):
    """Scrapes vehicle details from Parivahan website"""

    url = "https://vahan.parivahan.gov.in/nrservices/faces/user/searchstatus.xhtml"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Wait for page to load

        # Enter Vehicle Number
        search_box = driver.find_element(By.ID, "regn_no1_exact")
        search_box.send_keys(reg_number)
        search_box.send_keys(Keys.RETURN)

        time.sleep(5)  # Allow data to load

        # Extract Details
        vehicle_info = {}

        try:
            vehicle_info["Vehicle Number"] = reg_number
            vehicle_info["Owner Name"] = driver.find_element(By.XPATH, "//td[contains(text(),'Owner Name')]/following-sibling::td").text
            vehicle_info["Insurance Expiry Date"] = driver.find_element(By.XPATH, "//td[contains(text(),'Insurance Validity')]/following-sibling::td").text
            vehicle_info["Registration Date"] = driver.find_element(By.XPATH, "//td[contains(text(),'Registration Date')]/following-sibling::td").text
            vehicle_info["Owner Role"] = "OWNER"
            vehicle_info["Sell Eligible"] = False
            vehicle_info["Probable Vehicle Type"] = driver.find_element(By.XPATH, "//td[contains(text(),'Vehicle Class')]/following-sibling::td").text
            vehicle_info["Vehicle Model"] = driver.find_element(By.XPATH, "//td[contains(text(),'Maker / Model')]/following-sibling::td").text
            vehicle_info["Owner Count"] = driver.find_element(By.XPATH, "//td[contains(text(),'Owner Serial No')]/following-sibling::td").text
            vehicle_info["Fuel Type"] = driver.find_element(By.XPATH, "//td[contains(text(),'Fuel Type')]/following-sibling::td").text
            vehicle_info["Chassis Number"] = driver.find_element(By.XPATH, "//td[contains(text(),'Chassis No')]/following-sibling::td").text
            vehicle_info["Engine Number"] = driver.find_element(By.XPATH, "//td[contains(text(),'Engine No')]/following-sibling::td").text
            vehicle_info["Insurance Provider"] = "HDFC ERGO General Insurance Company Ltd"  # Fake data (Real API needed)
            vehicle_info["Pincode"] = "undefined"
            vehicle_info["Is Commercial"] = False
            vehicle_info["User ID"] = "67114917ed2d815947f62b13"
            vehicle_info["Date of Insurance Expiry"] = vehicle_info["Insurance Expiry Date"]
            vehicle_info["Insurance Expired"] = False
            vehicle_info["Expiring Today"] = False
            vehicle_info["App Open"] = 1
            vehicle_info["Owner Mobile"] = "NA"
        except:
            return {"error": "Vehicle details not found or CAPTCHA detected"}

        return vehicle_info

    finally:
        driver.quit()

@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    reg_number = request.args.get('reg_number')

    if not reg_number:
        return jsonify({"error": "Please provide a vehicle registration number!"}), 400

    vehicle_data = scrape_vehicle_details(reg_number)
    return jsonify(vehicle_data)

if __name__ == '__main__':
    app.run(debug=True)
