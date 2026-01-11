#!/bin/bash
# GarminDB Daily Sync Wrapper Script
# This script is intended to be run by a macOS LaunchAgent.

# Navigate to the project directory
cd /Users/joelgerard/dev/git/GarminDB

# Load the virtual environment and run garmindb_cli.py
# We use the absolute path to the venv python to ensure it has all dependencies.
./.venv/bin/python3 scripts/garmindb_cli.py -f "/Users/joelgerard/My Drive/joel health/tree health/tree_home/.GarminDb/GarminConnectConfig.json" --sleep --all --hrv --download --import --analyze --latest

echo "GarminDB sync completed at $(date)"
