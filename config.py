import os

from dotenv import load_dotenv
load_dotenv()
class Config:
    USER = os.getenv('USER', 'defaultuser')
    PASSWORD = os.getenv('PASSWORD', 'defaultpassword')
    Bearer = os.getenv('BEARER', 'defaultbearer')
