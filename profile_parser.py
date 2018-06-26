import re, json
from lxml import html


def get(lst, obj):
    return lst[lst.index(obj)]

def getall(lst, obj):
    result = []
    for item in lst:
        if item == obj:
            result.append(item)
    return result

def getre(lst, prog):
    for item in lst:
        if prog.match(item):
            return item

def getallre(lst, prog):
    result = []
    for item in lst:
        if prog.match(item):
            result.append(item)
    return result

friend_prog = re.compile(r'See All Friends \([0-9]+\)')
comments_prog = re.compile(r'[0-9]+ Comments?')
likes_prog = re.compile(r'[0-9]+')


def parse_about(scraper, fb_id, profile):
    url = 'https://m.facebook.com/' + fb_id + '?v=info'
    r = scraper.get(url)
    root = html.document_fromstring(r.content)

    text_list = root.xpath('//text()')

    profile['#friends'] = 0
    profile['*friends'] = False
    if 'Friends' in text_list:
        try:
            text = getre(text_list, friend_prog)
            profile['#friends'] = text[17:-1]
            profile['*friends'] = True
        except:
            pass

    try:
        education = root.get_element_by_id('education')
        entries = education[0][1].getchildren()
        profile['education'] = len(entries)
    except:
        profile['education'] = 0

    try:
        living = root.get_element_by_id('living')
        entries = education[0][1].getchildren()
        profile['living'] = len(entries)
    except:
        profile['living'] = 0

    try:
        work = root.get_element_by_id('work')
        entries = education[0][1].getchildren()
        profile['work'] = len(entries)
    except:
        profile['work'] = 0

    try:
        skills = root.get_element_by_id('skills')
        string = skills[0][1][0][0].text
        profile['skills'] = len(re.split(', | and ', string))
    except:
        profile['skills'] = 0

    profile['address'] = 'Address' in text_list
    profile['birthday'] = 'Birthday' in text_list
    profile['gender'] = 'Gender' in text_list
    profile['interested_in'] = 'Interested In' in text_list
    profile['phone'] = 'Mobile' in text_list


def parse_likes(scraper, fb_id, profile):
    likes = set()
    urls = ['https://m.facebook.com/' + fb_id + '?v=likes']

    while urls:
        url = urls[0]
        del urls[0]

        r = scraper.get(url)
        root = html.document_fromstring(r.content)
        text_list = root.xpath('//text()')

        for like in getall(text_list, 'Like'):
            try:
                name = like.getparent().getprevious().getprevious()[0].text
                likes.add(name)
            except:
                print('LIKE ERROR')

        for more in getall(text_list, 'See More'):
            try:
                if more.getparent().tag == 'a':
                    urls.append('https://m.facebook.com' + more.getparent().get('href'))
                else:
                    urls.append('https://m.facebook.com' + more.getparent().getparent().get('href'))
            except:
                print('LIKE MORE ERROR')

        if (len(likes) >= 200):
            break
        
    profile['likes'] = min(len(likes), 200)


def parse_story(scraper, entry):
    data = json.loads(entry.get('data-ft'))
    story = {'id': data.get('tl_objid', ''), 'likes': 0, 'comments': 0}
    entry_text_list = entry.xpath('.//text()')

    try:
        comments = getallre(entry_text_list, comments_prog)[-1]
        story['comments'] = int(comments.split(' ')[0])
    except:
        pass

    try:
        url = 'https://m.facebook.com' + getall(entry_text_list, 'Full Story')[-1].getparent().get('href')
        r = scraper.get(url)
        root = html.document_fromstring(r.content)
        text_list = root.xpath('//text()')

        for number in getallre(text_list, likes_prog):
            try:
                sentence = number.getparent().getparent().getparent().getparent()
                if sentence.get('id')[:8] == 'sentence':
                    story['likes'] = int(number)
                    break
            except:
                continue
    except:
        pass

    return story


def parse_timeline(scraper, fb_id, profile):
    timeline = []
    last = ''
    url = 'https://m.facebook.com/' + fb_id + '?v=timeline'

    while url:
        r = scraper.get(url)
        root = html.document_fromstring(r.content)
        container = root.get_element_by_id('structured_composer_async_container')

        try:
            entries = container[0].getchildren()
            for entry in entries:
                story = parse_story(scraper, entry)
                if not last:
                    last = story['id']
                timeline.append(story)
        except:
            pass

        try:
            more = container[1][0]
            if more[0].text == 'See More Stories':
                url = 'https://m.facebook.com' + more.get('href')
            else:
                url = None
        except:
            url = None

    profile['timeline'] = timeline
    profile['timeline_last'] = last
    comments = [story['comments'] for story in profile['timeline']]
    profile['comments_total'] = sum(comments)
    profile['comments_max'] = max(comments)
    profile['comments_avg'] = profile['comments_total'] / len(comments) if len(comments) else 0
    likes = [story['likes'] for story in profile['timeline']]
    profile['likes_total'] = sum(likes)
    profile['likes_max'] = max(likes)
    profile['likes_avg'] = profile['likes_total'] / len(likes) if len(likes) else 0

                


'''
def stringify(d, empty=True, f=lambda x: x if type(x) == str else x[0].text.strip()):
    r = {}
    for k, v in d.items():
        if not v:
            if not empty:
                continue
            else:
                r[k] = ''
        else:
            r[k] = v[1](v[0]) if type(v[0]) == list else f(v)
    return r


def parse_about(root, profile):
    profile['education'] = []
    try:
        education = root.get_element_by_id('education')
        for entry in education.xpath('./div/div[2]')[0].getchildren():
            data = {
                'name': entry.xpath('./div/div[1]/div[1]/div/span/a'),
                'type': entry.xpath('./div/div[1]/div[2]/span'),
            }
            profile['education'].append(stringify(data))
    except:
        pass


    profile['work'] = []
    try:
        work = root.get_element_by_id('work')
        for entry in work.xpath('./div/div[2]')[0].getchildren():
            data = {
                'name': entry.xpath('./div/div[1]/div[1]/span/a'),
            }
            profile['work'].append(stringify(data))
    except:
        pass


    profile['skills'] = []
    try:
        skills = root.get_element_by_id('skills')
        string = skills.xpath('./div/div[2]/div/span')[0].text
        profile['skills'] = re.split(', | and ', string)
    except:
        pass


    profile['living'] = []
    try:
        living = root.get_element_by_id('living')
        for entry in living.xpath('./div/div[2]')[0].getchildren():
            data = {
                'name': entry.xpath('./div/table/tr/td[2]/div/a'),
                'type': entry.xpath('./div/table/tr/td[1]/div/span'),
            }
            profile['living'].append(stringify(data))
    except:
        pass


    profile['info'] = {}
    try:
        contact = root.get_element_by_id('contact-info')
        entries = contact.xpath('./div/div[2]')[0]
        data = {
            'email': entries.xpath('./div[@title=\'Email\']/table/tr/td[2]/div/a'),
            'phone': entries.xpath('./div[@title=\'Mobile\']/table/tr/td[2]/div/span/span')
        }
        profile['info'].update(stringify(data))
    except:
        pass

    try:
        basic = root.get_element_by_id('basic-info')
        entries = basic.xpath('./div/div[2]')[0]
        data = {
            'birthday': entries.xpath('./div[@title=\'Birthday\']/table/tr/td[2]/div'),
            'gender': entries.xpath('./div[@title=\'Gender\']/table/tr/td[2]/div'),
            'interest': entries.xpath('./div[@title=\'Interested In\']/table/tr/td[2]/div'),
        }
        profile['info'].update(stringify(data))
    except:
        pass

    try:
        relationship = root.get_element_by_id('relationship')
        data = {
            'relationship': relationship.xpath('./div/div[2]/div/div/div')
        }
        profile['relationship'].update(stringify(data))
    except:
        pass



def parse_friends(root, profile):
    profile['friends'] = []
    try:
        entries = root.get_element_by_id('objects_container').xpath('./div/div[1]/div[2]')[0].getchildren()
        for entry in entries:
            data = {
                'name': entry.xpath('./table/tbody/tr/td[2]/a'),
                #'id': [entry.xpath('./table/tbody/tr/td[2]/div[2]/a'), friend_href],
            }
            profile['friends'].append(stringify(data))
    except:
        pass
    try:
        more = root.get_element_by_id('m_more_friends')
        return 'https://m.facebook.com' + more.xpath('./a')[0].get('href')
    except:
        pass


def parse_friends_more(root, profile):
    try:
        entries = root.get_element_by_id('root').xpath('./div[1]/div[1]')[0].getchildren()
        for entry in entries:
            data = {
                'name': entry.xpath('./table/tbody/tr/td[2]/a'),
                #'id': [entry.xpath('./table/tbody/tr/td[2]/div[2]/a'), friend_href],
            }
            profile['friends'].append(stringify(data))
    except:
        pass
    try:
        more = root.get_element_by_id('m_more_friends')
        return 'https://m.facebook.com' + more.xpath('./a')[0].get('href')
    except:
        pass



def parse_likes(root, profile):
    profile['likes'] = []
    more_urls = []
    try:
        sections = root.get_element_by_id('root').xpath('./div[1]')[0].getchildren()[1:]
        for section in sections:
            if section.xpath('./h4'):
                sec_data = stringify({'type': section.xpath('./h4')})
                sec_data['likes'] = []
                entries = section.getchildren()[1:]
                for entry in entries:
                    ent_data = {
                        'name': entry.xpath('./div/div[1]/a[1]/span'),
                    }
                    sec_data['likes'].append(stringify(ent_data, empty=False))
                profile['likes'].append(sec_data)
            elif section.xpath('./div/div'):
                sec_data = stringify({'type': section.xpath('./div/div/div/div/div[1]/h3')})
                sec_data['likes'] = []
                entries = section.xpath('./div/div/div/div/div[2]/div')[0].getchildren()
                for entry in entries:
                    ent_data = {
                        'name': entry.xpath('./div/div[1]/a/span'),
                    }
                    sec_data['likes'].append(stringify(ent_data, empty=False))
                profile['likes'].append(sec_data)
    except:
        pass


def parse_likes_more(root, profile):
    pass


def parse_timeline(root, profile):
    pass
'''
