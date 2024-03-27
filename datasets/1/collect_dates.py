import requests
import json
import csv
import time
import logging

from datetime import datetime
from tqdm import tqdm

# set up logging to file
logger = logging.getLogger(name='collect_dates')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('collect_dates.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

URL = "https://mb-api.abuse.ch/api/v1/"

def get_first_and_last_seen(hash_value):
    payload = {
        'query': 'get_info',
        'hash': hash_value
    }
    files = []
    headers = {}
    response = requests.request("POST", URL, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        response_json = response.json()
        if response_json['query_status'] == 'ok':
            first_seen, last_seen = response_json['data'][0]['first_seen'], response_json['data'][0]['last_seen']
            first_seen = datetime.strptime(first_seen, '%Y-%m-%d %H:%M:%S')
            last_seen = datetime.strptime(last_seen, '%Y-%m-%d %H:%M:%S') if last_seen else None
            return first_seen, last_seen, False
        else:
            logger.error(f"Query Status: {response_json['query_status']}")
            return None, None, True
    else:
        logger.error(f"Status: {response.status_code}")
        return None, None, False

# load hashes
with open('hashes.json', 'r') as file:
    hashes = json.load(file)
logger.info(f"Length of hashes: {len(hashes)}")

# hash_dates.csv: SHA256, DateTime, Date
with open('hash_dates.csv', 'w') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['SHA256', 'DateTime', 'Date'])
    for hash_value in tqdm(hashes):
        first_seen, last_seen, skip = get_first_and_last_seen(hash_value)
        time_counter = 1
        while not first_seen and not skip:
            logger.info(f"Sleeping for {time_counter}s...")
            time.sleep(time_counter)
            time_counter *= 2
            first_seen, last_seen, skip = get_first_and_last_seen(hash_value)
        if skip:
            logger.info(f"Skipping hash: {hash_value}")
        date = first_seen
        if last_seen:
            date = last_seen
        csv_writer.writerow([hash_value, date, date.date() if date else None])
