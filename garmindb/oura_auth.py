"""Oura authentication module."""

import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

logger = logging.getLogger(__name__)

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        self.server.authorization_response = self.path
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Authentication complete! You can close this window.</h1></body></html>')
    
    def log_message(self, format, *args):
        return

def run_auth(client):
    """Run the OAuth2 flow."""
    logger.info("Starting authentication flow...")
    oauth = client.authorize()
    
    # Start a local server to handle the redirect
    server_address = ('localhost', 8989)
    try:
        httpd = HTTPServer(server_address, OAuthHandler)
        logger.info("Listening on localhost:8989 for redirect...")
        httpd.handle_request()  # Handle a single request then return
        
        client.fetch_token(f'http://localhost:8989{httpd.authorization_response}')
        logger.info("Authentication successful!")
    except OSError as e:
        logger.error(f"Failed to start local server, maybe port 8989 is in use? Error: {e}")
        raise
