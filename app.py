from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import requests
from conn import *
from flask_cors import CORS
import qrcode
import io
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

app = Flask(__name__)
CORS(app)

def add_booking(booking_email, phone, ticks):
    response = supabase.table("bookings").insert({
        "booking-email": booking_email,
        "phone-number": phone,
        "no-of-tickets": ticks
    }).execute()
    
    if response.data:
        # Generate a unique booking ID
        booking_id = response.data[0]['id']
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(str(booking_id))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert QR code to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Send email with QR code
        send_email_with_qr(booking_email, booking_id, img_str)
        
        return {"success": True, "message": "Booking is made successfully", "booking_id": booking_id}
    else:
        return {"success": False, "message": "Booking is not successful"}

def send_email_with_qr(email, booking_id, qr_code_base64):
    sender_email = "chsantosh2004@gmail.com"  # Replace with your email
    sender_password = "luod qazf qdvh tvnx"  # Replace with your email password or app password
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Your Athena Museum Booking Confirmation"
    
    body = f"""
    Thank you for booking with Athena Museum!
    
    Your booking ID is: {booking_id}
    
    Please find attached your QR code for easy entry.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach QR code
    qr_code_image = base64.b64decode(qr_code_base64)
    image = MIMEImage(qr_code_image, name="booking_qr.png")
    msg.attach(image)
    
    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def get_details_of_booking_id(booking_id):
    response = supabase.table("payments").select("*").eq("booking-id", booking_id).execute()
    return response

@app.route('/api/bookings', methods=['POST'])
def add_booking_endpoint():
    data = request.json
    booking_email = data.get('booking_email')
    phone = data.get('phone')
    ticks = data.get('ticks')
    
    if not booking_email or not isinstance(booking_email, str):
        return jsonify({"error": "Invalid or missing booking email"}), 400
    if phone is None or not isinstance(phone, int):
        return jsonify({"error": "Invalid or missing phone number"}), 400
    if ticks is None or not isinstance(ticks, int):
        return jsonify({"error": "Invalid or missing number of tickets"}), 400
    
    result = add_booking(booking_email, phone, ticks)
    
    if result["success"]:
        return jsonify({"message": result["message"], "booking_id": result["booking_id"]}), 201
    else:
        return jsonify({"error": result["message"]}), 400

@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking_details(booking_id):
    response = get_details_of_booking_id(booking_id)
    
    if response.data:
        return jsonify({"data": response.data}), 200
    else:
        return jsonify({"error": "Booking not found"}), 404

@app.route('/api/websiteinformation', methods=['GET'])
def get_website_information():
    url = 'https://ease-frontend-alpha.vercel.app/'  # Updated to your new frontend URL
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Unable to fetch the website'}), 500
    
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    
    data = {
        'url': url,
        'content': text
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)