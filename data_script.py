from bs4 import BeautifulSoup
import requests
from data_inserts import insert_dicts

#set up the three required dicts
bill_dict = {}
senator_dict = {}
congress_dict = {}

url = 'https://www.senate.gov/legislative/LIS/roll_call_votes/vote1162/vote_116_2_00157.xml'

insert_dicts(url, bill_dict, senator_dict, congress_dict)
