import operator, string

# get the bill_dict as a dict
bills_txt = open("bill_dict.txt", "r")
bill_string = bills_txt.read()
bill_dict = eval(bill_string)

#get the most frequent words in the vote titles
words = {}
for bill in bill_dict:
    vote_title = bill_dict[bill]['vote_title']
    word_list = vote_title.split(" ")
    
    #count word frequency
    for w in word_list:
        for c in string.punctuation:
            if c == '.':
                continue
            else:
                w = w.replace(c,"")
        if not w.isdigit() and len(w)>2 and w[:1] != 'S.':
            if w not in words:
                words[w] = 1
            else:
                words[w] += 1

#Elimate top 100 words and names
top_100_txt = open("100_common_words.txt", "r")
top_100 = [line.strip('\n') for line in top_100_txt.readlines()]
top_100 = [line.strip('\t') for line in top_100]

for key in top_100:     
    try:
        del words[key]
    except:
        continue

freq_dict = {}
for key in words:
    freq = words[key]
    if freq not in freq_dict:
        freq_dict[freq] = [key,]
    else:
        freq_dict[freq].append(key)

print(freq_dict)

# freqs = sorted(freq_dict.keys(),reverse=True)
