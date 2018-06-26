import sys, json
from profile_scraper import *
import pprint as pp

if len(sys.argv) != 5:
    print('Invalid args!')
    exit(1)

_, fp, output, email, password = sys.argv

with open(fp, 'r') as file:
    ids = json.load(file)

profiles = []
scraper = Scraper()
scraper.login(email, password)
for fb_id in ids:
    profiles.append(scrape_profile(scraper, fb_id))

with open(output, 'w') as file:
    json.dump(profiles, file)

pp.pprint(profiles)