from fastapi import Response
import json
import requests
from requests.auth import HTTPBasicAuth
from config import Config

def peticion_get(url):
    try:
        username = Config.USER
        password = Config.PASSWORD
        print(username +' '+ password)
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, password))
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

#ho
def peticion_get_pdf(url):
    try:
        username = Config.USER
        password = Config.PASSWORD
        print(username +' '+ password)
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            filename = "documento.pdf"
            return Response(
                response.content,
                media_type='application/pdf',
                headers={"Content-Disposition": f"attachment;filename={filename}"}
            )
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
        
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()  # Esto generará una excepción para códigos de estado HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {
            "success": False,
            "message": f"HTTP error occurred: {http_err}",
            "status_code": response.status_code,
            "response_text": response.text,
            "response_headers": dict(response.headers)
        }
    except requests.exceptions.RequestException as req_err:
        return {
            "success": False,
            "message": f"Request exception occurred: {req_err}",
            "response_text": response.text if 'response' in locals() else None,
            "response_headers": dict(response.headers) if 'response' in locals() else None
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }
    

def peticion_get_rifa(url):
    try:
        token = Config.Bearer
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
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