from bs4 import BeautifulSoup
import requests
from data_inserts import insert_dicts

#set up the three required dicts
bill_dict = {}
senator_dict = {}
congress_dict = {}

# get the vote urls one by one
with open("vote_urls.txt") as vote_url_file:
    urls = [line.rstrip('\n') for line in vote_url_file]
vote_url_file.close()

# run the dictionary inserts
insert_dicts(urls, bill_dict, senator_dict, congress_dict)

# write the dictionaries into txt files
bill_txt = open("bill_dict.txt","w")
bill_txt.write(str(bill_dict))
bill_txt.close()

senator_txt = open("senator_dict.txt","w")
senator_txt.write(str(senator_dict))
senator_txt.close()

congress_txt = open("congress_dict.txt","w")
congress_txt.write(str(congress_dict))
congress_txt.close()
