# utils.py
import json
import requests
from requests.auth import HTTPBasicAuth
from config import Config

def peticion_get(url):
    try:
        Username = Config.USER
        Password = Config.PASSWORD
        print(f"Username: {Username}, Password: {Password}")
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(Username, Password))
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "success": False,
                "message": f"Error: {response.status_code}",
                "response_text": response.text,
                "response_headers": dict(response.headers)
            }
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

def peticion_post(data, url):
    try:
        payload = json.dumps(data)
        username = Config.USER
        password = Config.PASSWORD

        
        headers = {'Accept': 'application/json'}
        response = requests.post(url, headers=headers, data=payload, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "message": f"Error: {response.status_code}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
