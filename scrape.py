import requests
from bs4 import BeautifulSoup
from pprint import pprint

ADDITIONAL_PAGES = 3

res = requests.get("https://news.ycombinator.com/?p=1")
soup = BeautifulSoup(res.text, "html.parser")
links = soup.select(".titleline")
subtext = soup.select(".subtext")

for page_number in range(2, ADDITIONAL_PAGES + 1):
    page_res = requests.get("https://news.ycombinator.com/?p={page_number}")
    page_soup = BeautifulSoup(page_res.text, "html.parser")
    page_links = page_soup.select(".titleline")
    page_subtext = page_soup.select(".subtext")

    links = links + page_links
    subtext = subtext + page_subtext


def sort_stories_by_votes(hn_list):
    return sorted(hn_list, key=lambda k:k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn =[]
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.find('a').get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points >= 100:
                hn.append({'title': title, 'href': href, 'votes': points})
    return sort_stories_by_votes(hn)


pprint(create_custom_hn(links, subtext))