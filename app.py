from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vehicle', methods=['POST'])
def get_vehicle_details():
    reg_number = request.form.get("reg_number")
    
    if not reg_number:
        return jsonify({"error": "Please enter a vehicle registration number!"}), 400
    
    # Dummy response (replace this with actual API/Scraper)
    vehicle_data = {
        "Registration Number": reg_number,
        "Owner Name": "John Doe",
        "Vehicle Type": "Sedan",
        "Fuel Type": "Petrol",
        "Chassis Number": "XXXXX12345",
        "Engine Number": "XXXXX56789",
        "Registration Date": "2023-05-12"
    }
    
    return jsonify(vehicle_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
