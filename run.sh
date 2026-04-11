#!/bin/bash
cd /Users/joelgerard/dev/git/joel_garminDB/GarminDB
source .venv/bin/activate
python scripts/garmindb_cli.py --download --import --latest --all
