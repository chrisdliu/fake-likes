import requests, random, time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as BS
from profile_parser import *


class Scraper:
    def __init__(self):
        self.last = datetime.now()
        self.session = None
        self.response = None

    def add_time(self):
        if random.uniform(0, 1) >= 0.01:
            self.last += timedelta(seconds=random.uniform(2, 4))
        else:
            print('PAUSING...')
            self.last += timedelta(seconds=20)

    def safe(self):
        return datetime.now() >= self.last

    def login(self, email, password):
        self.session = requests.Session()
        r = self.get('https://facebook.com/')
        soup = BS(r.text, 'lxml')
        form = soup.find('form', id='login_form')
        login_url = form['action']
        inputs = form.findAll('input', {'type': ['hidden', 'submit']})
        payload = {input.get('name'): input.get('value') for input in inputs}
        payload['email'] = email
        payload['pass'] = password
        r = self.session.post(login_url, data=payload)
        if r.ok:
            print('Login success!')
            return True
        else:
            print('Login failed!')
            return False

    def get(self, url):
        #print('\t\tGetting ' + url)
        while not self.safe():
            time.sleep(0.1)
        self.add_time()
        self.response = self.session.get(url)
        return self.response


def scrape_profile(scraper, fb_id):
    print('Scraping and parsing ' + fb_id)
    
    profile = {
        'parsed': {},
        'raw': {},
        'id': fb_id,
    }

    try:
        if not validate(scraper, scrape_urls['about'].format(fb_id), profile):
            return profile

        params = (scraper, fb_id, profile)
        print('\tAbout...')
        parse_about(*params, True)
        print('\tLikes...')
        parse_likes(*params)
        print('\tTimeline...')
        parse_timeline(*params)

        return profile
    except:
        print('PARSE ERROR')
        profile['error'] = True
        return profile
