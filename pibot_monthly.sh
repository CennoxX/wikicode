#!/bin/bash
source /home/pi/.profile
source /home/pi/.bashrc
export PYTHONPATH=/home/pi/Documents/git/core:$PYTHONPATH
cd /home/pi/Documents/git/wikicode/

# Run this twice to catch cases where the IMO category was moved
/usr/bin/python3 wikidata_newshipname.py
/usr/bin/python3 wikidata_newshipname.py
/usr/bin/python3 wikidata_viewof.py
/usr/bin/python3 commonscat_redirects.py
/usr/bin/python3 commons_date_find.py
/usr/bin/python3 cochrane.py
/usr/bin/python3 cochrane_fr.py
