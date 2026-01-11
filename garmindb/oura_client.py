"""Oura API Client."""

__author__ = "Tom Goetz"
__copyright__ = "Copyright Tom Goetz"
__license__ = "GPL"

import requests
from requests_oauthlib import OAuth2Session
import datetime
import logging
from .oura_config import OuraConfigManager

logger = logging.getLogger(__name__)

class OuraClient:
    """Class for interacting with the Oura API."""

    AUTH_URL = 'https://cloud.ouraring.com/oauth/authorize'
    TOKEN_URL = 'https://api.ouraring.com/oauth/token'
    BASE_URL = 'https://api.ouraring.com/v2/usercollection'
    REDIRECT_URI = 'http://localhost:8989'

    def __init__(self, config_manager: OuraConfigManager):
        self.config = config_manager
        self.client_id = self.config.get_client_id()
        self.client_secret = self.config.get_client_secret()
        self.token = self.config.get_token()
        self.session = None

        if self.token:
            self.session = OAuth2Session(self.client_id, token=self.token, auto_refresh_url=self.TOKEN_URL,
                                         auto_refresh_kwargs={'client_id': self.client_id, 'client_secret': self.client_secret},
                                         token_updater=self.config.set_token)

    def authorize(self):
        """Start the authorization flow."""
        oauth = OAuth2Session(self.client_id, redirect_uri=self.REDIRECT_URI)
        authorization_url, state = oauth.authorization_url(self.AUTH_URL)
        print(f'Please go to {authorization_url} and authorize access.')
        return oauth

    def fetch_token(self, authorization_response):
        """Fetch the token from the authorization response."""
        oauth = OAuth2Session(self.client_id, redirect_uri=self.REDIRECT_URI)
        token = oauth.fetch_token(self.TOKEN_URL, authorization_response=authorization_response, client_secret=self.client_secret)
        self.config.set_token(token)
        self.session = OAuth2Session(self.client_id, token=token, auto_refresh_url=self.TOKEN_URL,
                                     auto_refresh_kwargs={'client_id': self.client_id, 'client_secret': self.client_secret},
                                     token_updater=self.config.set_token)
        return token

    def _get(self, endpoint, start_date=None, end_date=None):
        params = {}
        if start_date:
            params['start_date'] = start_date.strftime('%Y-%m-%d')
        if end_date:
            params['end_date'] = end_date.strftime('%Y-%m-%d')
        
        url = f'{self.BASE_URL}/{endpoint}'
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_personal_info(self):
        return self._get('personal_info')

    def get_daily_sleep(self, start_date, end_date):
        return self._get('daily_sleep', start_date, end_date)

    def get_daily_activity(self, start_date, end_date):
        return self._get('daily_activity', start_date, end_date)

    def get_daily_readiness(self, start_date, end_date):
        return self._get('daily_readiness', start_date, end_date)

    def get_heartrate(self, start_date, end_date):
        # Heartrate endpoint might use different time format, checking docs... 
        # Usually it's start_datetime/end_datetime. For now keying off date.
        return self._get('heartrate', start_date, end_date)

    def get_sessions(self, start_date, end_date):
        return self._get('session', start_date, end_date)

    def get_tags(self, start_date, end_date):
        return self._get('tag', start_date, end_date)

    def get_workouts(self, start_date, end_date):
        return self._get('workout', start_date, end_date)

    def get_daily_spo2(self, start_date, end_date):
        return self._get('daily_spo2', start_date, end_date)

    def get_daily_stress(self, start_date, end_date):
        return self._get('daily_stress', start_date, end_date)
    
    def get_ring_configuration(self, start_date, end_date):
         return self._get('ring_configuration', start_date, end_date)
         
    def get_heart_health(self, start_date, end_date):
         return self._get('heart_health', start_date, end_date)
