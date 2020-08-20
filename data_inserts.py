from bs4 import BeautifulSoup
import requests

def insert_dicts(urls, bill_dict, senator_dict, congress_dict):

    for url in urls:
        #request the page and get the html and information
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        document = soup.find('document_name').text

        #dictionary inserts
        congress_insert(soup, document, congress_dict)
        print('congress_insert done')
        votes = senator_votes(soup, document, senator_dict)
        print('senator_insert done')
        bill_insert(soup, document, votes, bill_dict)
        print('bill_insert done')
    return


def congress_insert(soup, document, congress_dict):
    #insert into the congress dict
    congress = soup.find('congress').text

    if congress in congress_dict:
        congress_dict[congress].append(document)
    else:
        congress_dict[congress] = [document]
    return


def senator_votes(soup, document, senator_dict):

    # get all the senate members
    members = soup.find_all('member')

    # get the senator information
    senator_info = ['member_full','first_name', 'last_name', 'party', 'state', 'vote_cast']

    # create voting dict
    votes = {'yea': set(), 'nay': set(), 'not voting': set()}

    # build up senator entries
    for mem in members:
        #add senator entry if it does not already exist
        senator_id = mem.find('lis_member_id').text
        if senator_id not in senator_dict:
            senator = {'full_name': None, 'member_full': None,'first_name': None, 'last_name':  None, 
                       'party': None, 'state': None, 'Yea':set(), 'Nay':set(), 'Not Voting':set()}
            full_name = mem.find('first_name').text + ' ' + mem.find('member_full').text
            senator['full_name'] = full_name
            for info in senator_info:
                senator[info] = mem.find(info).text

        #insert the vote information
        vote = mem.find('vote_cast').text
        senator[vote].add(document)

        # gather the votes
        if vote == 'Yea':
            votes['yea'].add(senator_id)
        elif vote == 'Nay':
            votes['nay'].add(senator_id)
        else:
            votes['not voting'].add(senator_id)

        senator_dict[senator_id] = senator

    return votes

def bill_insert(soup, document, votes, bill_dict):
    bill = {'congress': None, 'session': None, 'congress_year': None, 'vote_date': None, 'vote_number': None,
            'question': None, 'vote_title': None, 'vote_result_text': None, 'majority_requirement': None, 'yeas': None,
            'nays': None, 'absent': None, 'Yea': set(), 'Nay': set(), 'Not Voting': set()}

    bill_info = ['congress', 'session', 'congress_year', 'vote_date', 'vote_number',
            'question', 'vote_title', 'vote_result_text', 'majority_requirement', 'yeas', 'nays', 'absent']

    # fill in the bill info
    for info in bill_info:
        bill[info] = soup.find(info).text

    # fill in the senators votes
    bill['Yea'] = votes['yea']
    bill['Nay'] = votes['nay']
    bill['Not Voting'] = votes['not voting']

    bill_dict[document] = bill

    return
