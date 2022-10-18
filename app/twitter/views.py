from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
# Create your views here.
import json

class TweetListApiView(APIView):
    def get(self, request, username, format=None):
        headers = {
          "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAOE7iQEAAAAAb9PqbcKWo7Ek6XHwSzw79wqWf3o%3D78GTisCFp0u3DNeQjXTa6eeg7E2LpyvOWWwd5ebZcmxgIl4STl"
        }
        raw = requests.get(f"https://api.twitter.com/2/users/by/username/{username}", headers=headers)
        data = raw.json().get("data", None)
        if data:
          id = data.get("id", "")
          raw = requests.get(f"https://api.twitter.com/2/users/{id}/tweets?max_results=100", headers=headers)
          return Response(raw.json())
        return Response({"data": {"text": "invalid username"}})
