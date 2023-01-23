from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# Create your views here.


class FacebookAuthUser(APIView):
    def get(self, request, format=None):
        code = request.GET.get("code", "")
        print(request.__dict__)
        if code:
          print(code)
  #         data = {
  #           https://graph.facebook.com/v15.0/oauth/access_token?
  #  client_id={app-id}
  #  &redirect_uri={redirect-uri}
  #  &client_secret={app-secret}
  #  &code={code-parameter}
  #         }
          raw = requests.get("https://graph.facebook.com/v15.0/oauth/access_token")
        return Response({})

class GoogleAuthUser(APIView):
    def get(self, request, format=None):
        code = request.GET.get("code", "")
        if code:
          print("received code", code)
          data = {
            "client_id": "486855905508-5ifpvqv859hprvc37o8jqkbspqm33akj.apps.googleusercontent.com",
            "client_secret": "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",
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:80/api/gcp/auth/user/",
          }
          raw = requests.post("https://accounts.google.com/o/oauth2/token", data=data)
          body = raw.json()
          access, refresh = body.get("access_token"), body.get("refresh_token")
          print(access, refresh)
        return Response({})

# https://www.facebook.com/v15.0/dialog/oauth?
# client_id=5680464768677102
# &redirect_uri=http://localhost:80/api/gcp/auth/user/facebook/
# &state=123456

# https://accounts.google.com/o/oauth2/auth?
# scope=https://www.googleapis.com/auth/business.manage&
# response_type=code&
# access_type=offline&
# redirect_uri=http://localhost:80/api/gcp/auth/user/&
# client_id=486855905508-5ifpvqv859hprvc37o8jqkbspqm33akj.apps.googleusercontent.com

