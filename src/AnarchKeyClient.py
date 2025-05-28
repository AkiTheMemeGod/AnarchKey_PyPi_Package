import requests as rq
import json
BASE_URL = "https://anarchkey.pythonanywhere.com/"

class AnarchKeyClient:
    def __init__(self, api_key, username):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.username = username

    def get_api_key(self, project_name):

        payload = json.dumps({
            "project_name": project_name,
            "username": self.username,
            "api_key": self.api_key
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = rq.request("POST", self.base_url + "get_api_key", headers=headers, data=payload)
        response = response.json()
        if response["api_key"]["success"]:
            return response["api_key"]
        return response["api_key"]
