
import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  


load_dotenv()


MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
MPESA_BASE_URL = "https://sandbox.safaricom.co.ke"
MPESA_OAUTH_ENDPOINT = "/oauth/v1/generate?grant_type=client_credentials"
MPESA_STK_PUSH_URL = "/mpesa/stkpush/v1/processrequest"


MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
MPESA_INITIATOR_NAME = os.getenv("MPESA_INITIATOR_NAME")
MPESA_INITIATOR_PASSWORD = os.getenv("MPESA_INITIATOR_PASSWORD")
CALLBACK_URL = os.getenv("CALLBACK_URL") 
