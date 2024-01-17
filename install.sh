#!/bin/bash
pip install requests urllib3 beautifulsoup4

cd ..
cp -r wpyscan/ /usr/lib/wpyscan/
cd wpyscan
cp wpyscan /usr/bin/
chmod +x /usr/bin/wpyscan
cp wpyscan-uninstall /usr/bin/
chmod +x /usr/bin/wpyscan-uninstall

