from flask import Flask, jsonify, redirect, render_template, request
import requests
import threading
import time
import os 
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# API configuration
REQUEST_QR_CODE_URL = 'https://causality.xyz/api/requestQrCode'
STATUS_CHECK_URL = 'https://causality.xyz/api/apiStatusCheck'
HEADERS = {
    'Content-Type': 'application/json',
    
}

# Recommended products dictionary

recommended_products = {
    "52": {
        "url": "https://i.ibb.co/K6rBdzw/CSR2111-COR-MODEL-UNTUCKED.jpg",
        "rec_prd" : [
        {"product_id": "002", "product_name": "Dark Blue jeans", "url": "https://i.ibb.co/DKk09Jz/ecadd7eacb28dcf58890a59a08f42c5bb4-15-11-23-2-MH-SS24-roma-629-20-front-075.jpg","price":"23.55$"},
        {"product_id": "003", "product_name": "Black streach jeans", "url": "https://i.ibb.co/ykMFDJD/black-stretch-athletic-fit-chinos-600x600-jpg.webp","price":"23.55$"}
    ]
    }
    ,
    "51": {
        "url": "https://i.ibb.co/pycTWk4/shopping.jpg",
        "rec_prd" :[
        {"product_id": "004", "product_name": "Blue shirt", "url": "https://i.ibb.co/GtqS8zt/911n4n-Ihnp-L-AC-UY1000.jpg" , "price":"23.55$"},
        {"product_id": "005", "product_name": "Green shirt", "url": "https://i.ibb.co/y0Cs7DS/Solid-Mens-Olive-33976.webp","price":"23.55$"}
    ]
    }
}



@app.route('/', methods=['GET'])
def get_qr_code():
    key = os.getenv('KEY')
    token = os.getenv('TOKEN')
    payload = {
        "key": key,
        "token": token,
    }
    
    response = requests.post(REQUEST_QR_CODE_URL, json=payload, headers=HEADERS)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        qr_code_link = data.get('qrCodeLink')
        qrcode = data.get('qrcode')
        print(data)
        # Render QR code in template
        return render_template('display_qr.html', qrCodeLink=qr_code_link, qrcode=qrcode)
    else:
        return jsonify({"error": "Failed to retrieve QR code"}), 500

@app.route('/check_status', methods=['POST'])
def check_status():
    qrcode = request.form.get('qrcode')
    start_time = time.time()
    while time.time() - start_time <= 30:
        payload = {"code": qrcode}
        response = requests.post(STATUS_CHECK_URL, json=payload, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            print(data)
            recommend = []
            if str(data.get('product_id')) in recommended_products:
                recommend = recommended_products.get(str(data.get('product_id')))["rec_prd"]
                url = recommended_products.get(str(data.get('product_id')))["url"]
            return render_template('status.html', url=url, product_id=data.get('product_id'), product_name=data.get('product_name'),recommended_products=recommend)
        time.sleep(5)

    return render_template('status.html', message="false", nfc_tag="", chip_type="", product_id="", product_name="")


@app.route('/success')
def success():
    return "QR code successfully validated!"

@app.route('/error')
def error():
    return "Error: QR code validation failed."

if __name__ == '__main__':
    app.run(debug=True)