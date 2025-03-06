from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Server is running!"})

@app.route('/vehicle', methods=['GET'])
def get_vehicle_details():
    reg_number = request.args.get('reg_number')

    if not reg_number:
        return jsonify({"error": "Please provide a vehicle registration number!"}), 400

    # 🚀 Dummy Data (Scraping or API Integration required for real data)
    vehicle_data = {
        "Vehicle Number": reg_number,
        "Owner Name": "John Doe",
        "Insurance Expiry Date": "2027-12-06",
        "Vehicle Model": "Honda City",
        "Fuel Type": "Petrol",
        "Chassis Number": "XXXX12345",
        "Engine Number": "XXXX56789",
        "Registration Date": "12-Nov-1998",
        "Owner Count": 3,
        "Is Commercial": False
    }

    return jsonify(vehicle_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # ✅ Render ke liye port set karo
    app.run(host="0.0.0.0", port=port, debug=True)
