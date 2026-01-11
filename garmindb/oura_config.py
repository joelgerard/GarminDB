import os
import sys
import json
import datetime

from .garmin_connect_config_manager import GarminConnectConfigManager

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super().default(obj)

class OuraConfigManager(GarminConnectConfigManager):
    """Class that manages Oura downloads."""

    def __init__(self, config_dir=None):
        """Return a new OuraConfigManager instance."""
        super().__init__(config_dir)
        self.oura_config = self.config.get('oura', {})
        self.token_file = self.config_dir + os.sep + 'OuraTokens.json'
        self.tokens = self._load_tokens()

    def _load_tokens(self):
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_tokens(self):
        with open(self.token_file, 'w') as f:
            json.dump(self.tokens, f, indent=4, cls=DateEncoder)

    def get_client_id(self):
        """Return the Oura client ID."""
        return self.oura_config.get('client_id')

    def get_client_secret(self):
        """Return the Oura client secret."""
        return self.oura_config.get('client_secret')

    def get_token(self):
        """Return the Oura OAuth2 token."""
        return self.tokens.get('token')

    def set_token(self, token):
        """Set the Oura OAuth2 token."""
        self.tokens['token'] = token
        self._save_tokens()
