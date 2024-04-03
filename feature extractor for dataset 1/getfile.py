import requests, sys

session = requests.Session()
session.headers = {'X-Apikey': 'e574dfcbc009def4c0456297e623369fe71c5a21d3b72c64d3640f96cacf66d2'}

sha256 = sys.argv[1]

url = f"https://www.virustotal.com/api/v3/monitor_partner/files/{sha256}/download"
response = session.get(url)
print(response.text)