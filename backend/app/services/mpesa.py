import requests
import base64
import re
from datetime import datetime
from app.config import (
    MPESA_BASE_URL, MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET, 
    MPESA_STK_PUSH_URL, MPESA_SHORTCODE, MPESA_PASSKEY, CALLBACK_URL
)

def get_mpesa_token():
    """Get OAuth token for M-Pesa API."""
    consumer_key_secret = f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}".encode("utf-8")
    encoded_key_secret = base64.b64encode(consumer_key_secret).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_key_secret}"
    }

    response = requests.get(f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials", headers=headers)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        raise Exception("Failed to get M-Pesa OAuth token")

def base64encoder(string_to_encode: str) -> str:
    """Encode a string to base64."""
    string_to_encode_bytes = string_to_encode.encode("ascii")
    base64_bytes = base64.b64encode(string_to_encode_bytes)
    return base64_bytes.decode("ascii")

def validate_phone_number(phone_number: str) -> bool:
    """Validate phone number format."""
    pattern = r"^(?:254|\+254|0)?((?:(?:7(?:(?:[01249][0-9])|(?:5[789])|(?:6[89])))|(?:1(?:[1][0-5])))[0-9]{6})$"
    return bool(re.match(pattern, phone_number))

def format_phone_number(phone_number: str) -> str:
    """Format phone number to E.164 format."""
    if phone_number.startswith("+"):
        return phone_number.strip("+")
    if phone_number.startswith("0"):
        return phone_number.replace("0", "254", 1)
    return phone_number

def get_encoded_password() -> str:
    """Generate the encoded password for the M-Pesa request."""
    transaction_date_time = datetime.today().strftime('%Y%m%d%H%M%S')
    passkey = (
        MPESA_SHORTCODE +
        MPESA_PASSKEY +
        transaction_date_time
    )
    return base64encoder(passkey)

def get_transaction_time() -> str:
    """Get the current transaction time in the required format."""
    return datetime.today().strftime('%Y%m%d%H%M%S')

def initiate_stk_push(phone_number, amount):
    """Initiate the M-Pesa STK Push."""
    if not validate_phone_number(phone_number):
        raise Exception("Invalid phone number format")

    formatted_phone = format_phone_number(phone_number)
    access_token = get_mpesa_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": get_encoded_password(),
        "Timestamp": get_transaction_time(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": formatted_phone,
        "PartyB": MPESA_SHORTCODE,
        "PhoneNumber": formatted_phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "House Rent",
        "TransactionDesc": "Rent Payment"
    }

    response = requests.post(f"{MPESA_BASE_URL}{MPESA_STK_PUSH_URL}", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    raise Exception(f"STK Push failed: {response.text}")
