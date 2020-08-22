from bs4 import BeautifulSoup
import requests

def insert_dicts(urls, bill_dict, senator_dict, congress_dict):

    for url in urls:
        #request the page and get the html and information
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            document = soup.find('document_name').text
        except:
            print('ERROR', url)
            document = soup.find('congress').text + '/' + soup.find('session').text + '/' + soup.find('congress_year').text + '/' + soup.find('vote_number').text
            continue

        #dictionary inserts
        congress_insert(soup, document, congress_dict)
        votes = senator_votes(soup,document, senator_dict)
        bill_insert(soup, document, url, votes, bill_dict)
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
    votes = {'yea': set(), 'nay': set(), 'not_voting': set(), 'guilty': set(), 'not_guilty': set(), 'present': set(), 'present_giving_live_pair': set()}

    # build up senator entries
    for mem in members:
        #add senator entry if it does not already exist
        senator_id = mem.find('lis_member_id').text
        if senator_id not in senator_dict:
            senator = {'full_name': None, 'member_full': None,'first_name': None, 'last_name':  None, 
                       'party': None, 'state': None, 'Yea': set(), 'Nay': set(), 'Not Voting': set(), 'Guilty': set(),
                       'Not Guilty': set(), 'Present': set(), 'Present, Giving Live Pair': set()}
            full_name = mem.find('first_name').text + ' ' + mem.find('member_full').text
            senator['full_name'] = full_name
            for info in senator_info:
                senator[info] = mem.find(info).text
        
            # add all of the data
            senator_dict[senator_id] = senator

        #insert the vote information or output the unknown vote
        vote = mem.find('vote_cast').text
        try:
            senator_dict[senator_id][vote].add(document)
        except:
            print("UNKNOWN VOTE",vote)
            print(document)
            continue

        # gather the votes
        if vote == 'Yea':
            votes['yea'].add(senator_id)
        elif vote == 'Nay':
            votes['nay'].add(senator_id)
        elif vote == 'Not Voting':
            votes['not_voting'].add(senator_id)
        elif vote == 'Guilty':
            votes['guilty'].add(senator_id)
        elif vote == 'Not Guilty':
            votes['not_guilty'].add(senator_id)
        elif vote == 'Present':
            votes['present'].add(senator_id)
        else:
            votes['present_giving_live_pair'].add(senator_id)

    return votes

def bill_insert(soup, document, url, votes, bill_dict):
    bill = {'url': None, 'congress': None, 'session': None, 'congress_year': None, 'vote_date': None, 'vote_number': None,
            'question': None, 'vote_title': None, 'vote_result_text': None, 'majority_requirement': None, 'yeas': None,
            'nays': None, 'absent': None, 'Yea': set(), 'Nay': set(), 'Not Voting': set(), 'Guilty': set(), 'Not Guilty': set(),
            'Present': set(), 'Present, Giving Live Pair': set() }

    bill_info = ['congress', 'session', 'congress_year', 'vote_date', 'vote_number',
            'question', 'vote_title', 'vote_result_text', 'majority_requirement', 'yeas', 'nays', 'present', 'absent']

    # fill in the bill info
    bill['url'] = url
    for info in bill_info:
        bill[info] = soup.find(info).text

    # fill in the senators votes
    bill['Yea'] = votes['yea']
    bill['Nay'] = votes['nay']
    bill['Not Voting'] = votes['not_voting']
    bill['Guilty'] = votes['guilty']
    bill['Not Guilty'] = votes['not_guilty']
    bill['Present'] = votes['present']
    bill['Present, Giving Live Pair'] = votes['present_giving_live_pair']

    bill_dict[document] = bill

    return
