# from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from typing import Dict, Any
import requests
import secrets

from applications.userprofile.models import Profile

User = get_user_model()


class GoogleOAuthInitiateView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request: Request) -> Response:
        state: str = secrets.token_urlsafe(32)
        request.session['oauth_state'] = state
        
        google_auth_url: str = 'https://accounts.google.com/o/oauth2/v2/auth' # authorization endpoint (where user logs in)
        params: Dict[str, str] = {
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
            'response_type': 'code',
            'scope': 'email profile',
            'state': state,
            'access_type': 'online',
            'prompt': 'select_account'
        }
        
        from urllib.parse import urlencode
        auth_url: str = f"{google_auth_url}?{urlencode(params)}"
        
        return Response({'auth_url': auth_url})


class GoogleOAuthCallbackView(APIView):
    def get(self, request: Request) -> Response:
        code: str | None = request.GET.get('code')
        state: str | None = request.GET.get('state')
        error: str | None = request.GET.get('error')
        
        if error:
            print('Error occured')
            # return redirect(f'{settings.FRONTEND_URL}/error_page/should/be/there/')
        
        if not code:
            print('Code was not received')
            # return redirect(f'{settings.FRONTEND_URL}/error_page/missing/code/should/be/there')
        
        stored_state: str | None = request.session.get('oauth_state')
        if not stored_state or stored_state != state:
            print('Store can not pass condition')
            # return redirect(f'{settings.FRONTEND_URL}/error_page/invalid/state')
        
        try:
            token_response = requests.post(
                'https://oauth2.googleapis.com/token', # token exchange endpoint (getting acess tokens)
                data={
                    'code': code,
                    'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
                    'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
                    'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
                    'grant_type': 'authorization_code',
                }
            )
            
            print(token_response)
            
            if token_response.status_code != 200:
                print('token response status code not equal 200')
                # return redirect(f'{settings.FRONTEND_URL}/login?error=token_exchange_failed') # sample url

            token_data: Dict[str, Any] = token_response.json()
            access_token: str | None = token_data.get('access_token')
            
            user_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo', # user info endpoint (getting user info)
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            if user_response.status_code != 200:
                print('user response status code not equal 200')
                # return redirect(f'{settings.FRONTEND_URL}/login?error=user_info_failed')
            
            google_user_data: Dict[str, Any] = user_response.json()
            email: str | None = google_user_data.get('email')
            google_id: str | None = google_user_data.get('sub')
            
            if not email:
                print('No email')
                # return redirect(f'{settings.FRONTEND_URL}/login?error=no_email')
            
            user, created = User.objects.get_or_create(email=email)
            # profile = Profile.objects.update(
            #     owner=user,
            #     username=google_user_data.get('name'),
            #     pfp=google_user_data.get('picture')
            # )
            
            SocialAccount.objects.get_or_create(
                user=user, 
                provider='google', 
                defaults={'uid': google_id}
            )
            
            refresh: RefreshToken = RefreshToken.for_user(user)
            jwt_access_token: str = str(refresh.access_token)
            jwt_refresh_token: str = str(refresh)
            
            # response: HttpResponse = redirect(f'{settings.FRONTEND_URL}/auth/success/')
            response = Response(data={
                'detail': 'Loged in successfully',
                'status': '201'
            })
            
            self._set_token_cookie(
                response,
                'access_token',
                jwt_access_token,
                max_age=settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME').total_seconds()
            )
            self._set_token_cookie(
                response,
                'refresh_token',
                jwt_refresh_token,
                max_age=settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME').total_seconds()
            )
            
            request.session.pop('oauth_state', None)
            
            return response 
        
        except Exception as e:
            print('OAuth error: ', str(e))
            # return redirect(f'{settings.FRONTEND_URL}/login/oauth/failed/')
    
    def _set_token_cookie(self, response: HttpResponse, key: str, value: str, max_age: float) -> None:
        response.set_cookie(
            key=key,
            value=value,
            max_age=int(max_age),
            path='/',
            secure=False,
            httponly=True,
            samesite='Lax'
        )
