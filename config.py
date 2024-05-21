import os
from libredte import api_client

class Config:
    USER = os.getenv('USER', 'defaultuser')
    PASSWORD = os.getenv('PASSWORD', 'defaultpassword')

