from bs4 import BeautifulSoup
import requests

def get_roll_call_list_links(url, url_segment):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        next_page = link.get('href')
        if type(next_page) is str and url_segment in next_page:
            links.append(next_page)

    # clean the links to include the https etc
    clean_links = []
    for l in links:
        if 'senate.gov' not in l:
            clean_links.append('https://www.senate.gov' + l)
        else:
            clean_links.append(l)

    return clean_links

def get_vote_links():
    og_url = 'https://www.senate.gov/reference/Index/Votes.htm'
    # get each document from a specific congress and session
    congresses = get_roll_call_list_links(og_url, 'roll_call_lists/vote_menu')
    print('got congresses')

    # get each vote record
    documents = []
    for link in congresses:
        documents.extend(get_roll_call_list_links(link, 'roll_call_lists/roll_call_vote_cfm'))

    print('got votes')

    # get the xml
    votes = []
    for link in documents:
        votes.extend(get_roll_call_list_links(link, 'xml'))
    
    print('got xmls')

    return votes


#get all the vote urls
votes = get_vote_links()

# get the vote urls stored in a txt file
vote_urls_txt = open("vote_urls.txt","w")
for elem in votes:
    vote_urls_txt.write(elem+'\n')
vote_urls_txt.close()