import sys, pickle
from profile_scraper import *
import pprint as pp

if len(sys.argv) != 3:
    print('Invalid args!')
    exit(1)

_, email, password = sys.argv

with open('all_likers.txt', 'rb') as file:
    ids = pickle.load(file)

new_ids = []
scraper = Scraper()
scraper.login(email, password)
for fb_id in ids:
    if profile_exists(scraper, fb_id[1].split('.com/')[1]):
        new_ids.append(fb_id)

with open('all_likers_clean.txt', 'wb') as file:
    pickle.dump(new_ids, file)
