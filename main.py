from bs4 import BeautifulSoup


log = logging.getLogger('statistics') # Логер в контексте джанго, заменить на нативный


class Facebook_Stats:
    def __init__(self, fb_post_id, fb_token):
        self.fb_post_id = fb_post_id
        self.fb_token = fb_token

    def req_stats(self, url_method):
        req = requests.get(url_method)
        if req.status_code != 200:
            log.info('Facebook_Stats: %s' % req.json())
            return -1
        return req.json().get('summary').get('total_count')

    def fb_likes(self):
        url_method = fb_url + '%s/likes?summary=true&access_token=%s' % (self.fb_post_id, self.fb_token)
        return self.req_stats(url_method)

    def fb_reactions(self):
        url_method = fb_url + '%s/reactions?summary=total_count&access_token=%s' % (self.fb_post_id, self.fb_token)
        return self.req_stats(url_method)

    def fb_comments(self):
        url_method = fb_url + '%s/comments?summary=true&access_token=%s' % (self.fb_post_id, self.fb_token)
        return self.req_stats(url_method)

    def fb_sharedposts(self):
        url_method = fb_url + '%s/sharedposts?access_token=%s' % (self.fb_post_id, self.fb_token)
        req = requests.get(url_method)
        if req.status_code != 200:
            log.info('Facebook_Stats: %s' % req.json())
            return -1
        return len(req.json().get('data'))

    def fb_stats(self):
        fb_likes, fb_reactions, fb_comments, fb_sharedposts = self.fb_likes(), self.fb_reactions(), self.fb_comments(),\
        self.fb_sharedposts()
        return int(fb_likes), int(fb_reactions), int(fb_comments), int(fb_sharedposts)


class MediumStats:

    def stats(self, post_url):
        url = post_url
        html_doc = requests.get(url)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        lc = soup.find('div', class_='u-floatLeft buttonSet buttonSet--withLabels')
        r_list = []
        try:
            t = lc.find_all('button', class_='button button--chromeless u-baseColor--buttonNormal')
        except AttributeError as e:
            log.info('MediumStats: %s' % str(e))
            return -1, -1
        if len(t) == 2:
            for div in t:
                try:
                    if div['data-action'] == 'show-recommends':
                        r_list.append(int(div.text))
                    if div['data-action'] == 'scroll-to-responses':
                        r_list.append(int(div.text))
                    else:
                        r_list.append(0)
                except KeyError as e:
                    log.info('MediumStats: %s' % str(e))
                    return -1, -1
        elif len(t) == 1:
            if 'show-recommends' in str(t):
                for div in t:
                    r_list.append(int(div.text))
                    r_list.append(0)
            elif 'scroll-to-responses' in str(t):
                for div in t:
                    r_list.append(0)
                    r_list.append(int(div.text))
        elif len(t) == 0:
            r_list.append(0)
            r_list.append(0)
        return r_list