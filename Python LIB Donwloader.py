# Dependencies: pip install requests beautifulsoup4
# Tested on Python3.8.6, beautifulsoup4==4.9.3, requests==2.25.1

import random
import requests
import subprocess
from bs4 import BeautifulSoup

pypi_index = 'https://pypi.python.org/simple/'
print(f'GET list of packages from {pypi_index}')
try:
    resp = requests.get(pypi_index, timeout=5)
except requests.exceptions.RequestException:
    print('ERROR: Could not GET the pypi index. Check your internet connection.')
    exit(1)

print(f'NOW parsing the HTML (this could take a couple of seconds...)')
try:
    soup = BeautifulSoup(resp.text, 'html.parser')
    body = soup.find('body')
    links = (pkg for pkg in body.find_all('a'))
except:
    print('ERROR: Could not parse pypi HTML.')
    exit(1)


# set ny limit you want
install_limit = 100
some_of_the_links = random.sample(list(links), install_limit)

for link in some_of_the_links:
    pkg_name = link['href'].split('/')[-2]
    cmd = f'pip install {pkg_name}' 
    print("=" * 30)
    print(f'NOW installing "{pkg_name}"')
    try:
        subprocess.run(cmd.split(), check=True)
    except subprocess.CalledProcessError:
        print(f'ERROR: Failed to install {pkg_name}')
        continue
