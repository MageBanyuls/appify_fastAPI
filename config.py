import os

class Config:
    USER = os.getenv('USER', 'defaultuser')
    PASSWORD = os.getenv('PASSWORD', 'defaultpassword')