from bs4 import BeautifulSoup
import requests
from data_inserts import insert_dicts
from webscraper import get_vote_links

#set up the three required dicts
bill_dict = {}
senator_dict = {}
congress_dict = {}

urls = get_vote_links()
insert_dicts(urls, bill_dict, senator_dict, congress_dict)
