import sys, subprocess, json, requests, random
import datetime as dt
import pprint as pp
from bs4 import BeautifulSoup as BS
from profile_parser import *


class Scraper:
    def __init__(self):
        self.last = dt.datetime.now()
        self.session = None

    def add_time(self):
        self.last += dt.timedelta(seconds=random.uniform(2, 5))

    def safe(self):
        return dt.datetime.now() >= self.last

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
            pass
        self.add_time()
        return self.session.get(url)


def scrape_profile(scraper, fb_id):
    print('Scraping and parsing ' + fb_id)
    
    profile = {'id': fb_id}
    params = (scraper, fb_id, profile)
    print('\tAbout...')
    parse_about(*params)
    print('\tLikes...')
    parse_likes(*params)
    print('\tTimeline...')
    parse_timeline(*params)

    return profile
