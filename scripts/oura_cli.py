#!/usr/bin/env python3
"""
Oura database CLI.
"""

import argparse
import sys
import os
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from datetime import date, timedelta, datetime

# Add the project root to the path so we can import garmindb modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Allow OAuth over HTTP for local testing
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from garmindb.oura_config import OuraConfigManager
from garmindb.oura_client import OuraClient
from garmindb.oura_db import OuraDb
from garmindb.oura_sync import sync_data
from garmindb.oura_auth import run_auth

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)





def main():
    parser = argparse.ArgumentParser(description='Oura Database Tool')
    parser.add_argument('command', choices=['auth', 'sync'], help='Command to run')
    parser.add_argument('--days', type=int, default=7, help='Number of days to sync (default: 7)')
    args = parser.parse_args()

    config = OuraConfigManager()
    client = OuraClient(config)

    if args.command == 'auth':
        run_auth(client)
    elif args.command == 'sync':
        db_params = config.get_db_params()
        db_manager = OuraDb(db_params)
        end_date = date.today()
        start_date = end_date - timedelta(days=args.days)
        sync_data(client, db_manager, start_date, end_date)

if __name__ == '__main__':
    main()
