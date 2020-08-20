from bs4 import BeautifulSoup
import requests

def get_roll_call_list_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        next_page = link.get('href')
        if type(next_page) is str and 'roll_call_lists' in next_page:
            links.append(next_page)

    # clean the links
    clean_links = set()
    for l in links:
        if 'senate.gov' not in l:
            clean_links.add('https://www.senate.gov' + l)
        else:
            clean_links.add(l)
    return clean_links

def get_vote_links():
    og_url = 'https://www.senate.gov/reference/Index/Votes.htm'
    congresses = get_roll_call_list_links(og_url)
    documents = []
    for link in congresses:
        documents.extend(get_roll_call_list_links(link))
    votes = []
    for link in documents:
        votes.extend(get_roll_call_list_links(link))
    return votes


print(get_vote_links)