from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def get_vehicle_details(reg_number):
    """Scrapes vehicle details from the Parivahan website using Selenium"""

    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without opening browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open Parivahan Vehicle Search Page
        url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=102"
        driver.get(url)
        time.sleep(3)  # Wait for page to load

        # Enter Vehicle Number
        search_box = driver.find_element(By.ID, "regn_no")
        search_box.send_keys(reg_number)
        search_box.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for results to load

        # Extract Vehicle Details
        vehicle_info = {}
        try:
            vehicle_info["Registration Number"] = driver.find_element(By.XPATH, "//td[contains(text(),'Registration No')]/following-sibling::td").text
            vehicle_info["Owner Name"] = driver.find_element(By.XPATH, "//td[contains(text(),'Owner Name')]/following-sibling::td").text
            vehicle_info["Vehicle Type"] = driver.find_element(By.XPATH, "//td[contains(text(),'Vehicle Class')]/following-sibling::td").text
            vehicle_info["Fuel Type"] = driver.find_element(By.XPATH, "//td[contains(text(),'Fuel Type')]/following-sibling::td").text
            vehicle_info["Chassis Number"] = driver.find_element(By.XPATH, "//td[contains(text(),'Chassis No')]/following-sibling::td").text
            vehicle_info["Engine Number"] = driver.find_element(By.XPATH, "//td[contains(text(),'Engine No')]/following-sibling::td").text
        except:
            return {"error": "Vehicle details not found or CAPTCHA detected"}

        return vehicle_info

    finally:
        driver.quit()  # Close browser session

@app.route("/", methods=["GET", "POST"])
def index():
    vehicle_data = None
    if request.method == "POST":
        reg_number = request.form["reg_number"]
        vehicle_data = get_vehicle_details(reg_number)
    
    return render_template("index.html", vehicle_data=vehicle_data)

if __name__ == "__main__":
    app.run(debug=True)
