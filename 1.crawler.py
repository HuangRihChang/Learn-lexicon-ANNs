import twitter #To install: open PowerShell, type `pip install twitter`
import requests, re, time, os
import matplotlib.pyplot as plts

CONSUMER_KEY = 'zC0l8hihN8yG0nyjAuJDuZYZL'
CONSUMER_SECRET ='ppVzdV30tEyuRn526jWt01NdZw8iSWCCdzkTxpH372dMZUi5wh'
OAUTH_TOKEN = '843983090884128768-b9rlzAi1QuBS1RT2TPaBQAa7efw3lOU'
OAUTH_TOKEN_SECRET = 'U29lYqtRxE6PVbTEbPW7dV0uvjgOvZzfXFdcqb3EqGc8Q'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


def getTweet(emo, sumPages):
    
    num_of_check_lines = 5000
    num_of_patience = 3
    
    if(re.findall('\)', emo)):
        matches = [':\)', ': \)', ':-\)', ':D', '=\)']
        anti_matches = [':\(', ': \(', ':-\(']
        sentive = 1
        
    else:
        matches = [':\(', ': \(', ':-\(']
        anti_matches = [':\)', ': \)', ':-\)', ':D', '=\)']
        sentive = 0
    
    search_results = twitter_api.search.tweets(q=emo, count=50)

    # Init variables
    statuses = search_results['statuses']
    page_idx = 0 # First page
    
    sumPages += 1
    if sumPages == 175:
        return 0

    # Print search info
    print 'Page %d, %d statuses' %(page_idx, len(search_results['statuses']))

    # Go to next page, then next page, then next page ...
    while True:
        # Go to next page
        try:
            next_search = search_results['search_metadata']['next_results']
            kwargs = dict([requests.utils.unquote(kv).split('=') for kv in next_search[1:].split('&')])
            search_results = twitter_api.search.tweets(**kwargs)
        except:
            break # No more page, or ...
    
        # Update variables
        statuses += search_results['statuses']
        page_idx += 1
        sumPages += 1
        
        for stat in statuses:
            
            if stat['lang'] == 'zh-cn' or stat['lang'] == 'zh-tw':

                if not os.path.exists("./train_data/zh-data/"): 
                    os.mkdir("./train_data/zh-data/")
                    os.mkdir("./train_data/zh-data/raw")
                
                fileTraining = open("./train_data/zh-data/raw/metatweets", "ab")
                
                status_pocess = str(stat['text'].encode('utf-8'))
                
                both_emoji = False
                
                for anti_match in anti_matches:
                        if re.findall(anti_match, status_pocess):
                            both_emoji = True
                            break
                
                if not (re.findall(':P', status_pocess) or re.findall(':p', status_pocess)
                        or re.findall('RT', status_pocess) or both_emoji):
                    status_pocess = re.sub('\n', ' ', status_pocess)                    
                    i = 0
                    is_not_existed = True
                    patiences = 0
                    status_pocess = str(sentive) + " " + status_pocess + "\n"
                    
                    for line in reversed(open("./train_data/zh-data/raw/metatweets").readlines()):
                        i += 1
                        if i == num_of_check_lines:
                            break
                        if status_pocess == line:
                            is_not_existed = False
                            patiences += 1
                            break
                    if(patiences == num_of_patience):
                        break
                    
                    if len(status_pocess.split(' ')) >= 7 and is_not_existed:
                        fileTraining.write(status_pocess)
                    fileTraining.close()
            
            if stat['lang'] == 'ar':

                if not os.path.exists("./train_data/ar-data/"): 
                    os.mkdir("./train_data/ar-data/")
                    os.mkdir("./train_data/ar-data/raw")
                
                
                fileTraining = open("./train_data/ar-data/raw/metatweets", "ab")
                
                status_pocess = str(stat['text'].encode('utf-8'))
                
                both_emoji = False
                
                for anti_match in anti_matches:
                        if re.findall(anti_match, status_pocess):
                            both_emoji = True
                            break
                
                if not (re.findall(':P', status_pocess) or re.findall(':p', status_pocess)
                        or re.findall('RT', status_pocess) or both_emoji):
                    status_pocess = re.sub('\n', ' ', status_pocess)                    
                    i = 0
                    is_not_existed = True
                    patiences = 0
                    status_pocess = str(sentive) + " " + status_pocess + "\n"
                    
                    for line in reversed(open("./train_data/ar-data/raw/metatweets").readlines()):
                        i += 1
                        if i == num_of_check_lines:
                            break
                        if status_pocess == line:
                            is_not_existed = False
                            patiences += 1
                            break
                    if(patiences == num_of_patience):
                        break
                    
                    if len(status_pocess.split(' ')) >= 7 and is_not_existed:
                        fileTraining.write(status_pocess)
                    fileTraining.close()
            
            if stat['lang'] == 'vi':

                if not os.path.exists("./train_data/vi-data/"): 
                    os.mkdir("./train_data/vi-data/")
                    os.mkdir("./train_data/vi-data/raw")

                fileTraining = open("./train_data/vi-data/raw/metatweets", "ab")
                
                status_pocess = str(stat['text'].encode('utf-8'))
                
                both_emoji = False
                
                for anti_match in anti_matches:
                        if re.findall(anti_match, status_pocess):
                            both_emoji = True
                            break
                
                if not (re.findall(':P', status_pocess) or re.findall(':p', status_pocess)
                        or re.findall('RT', status_pocess) or both_emoji):
                    status_pocess = re.sub('\n', ' ', status_pocess)                    
                    i = 0
                    is_not_existed = True
                    patiences = 0
                    status_pocess = str(sentive) + " " + status_pocess + "\n"
                    
                    for line in reversed(open("./train_data/vi-data/raw/metatweets").readlines()):
                        i += 1
                        if i == num_of_check_lines:
                            break
                        if status_pocess == line:
                            is_not_existed = False
                            patiences += 1
                            break
                    if(patiences == num_of_patience):
                        break
                    
                    if len(status_pocess.split(' ')) >= 7 and is_not_existed:
                        fileTraining.write(status_pocess)
                    fileTraining.close()
                        
            if stat['lang'] == 'en':
                
                if not os.path.exists("./train_data/en-data/"): 
                    os.mkdir("./train_data/en-data/")
                    os.mkdir("./train_data/en-data/raw")

                fileTraining = open("./train_data/en-data/raw/metatweets", "ab")
                
                status_pocess = str(stat['text'].encode('utf-8'))
                
                both_emoji = False
                
                for anti_match in anti_matches:
                        if re.findall(anti_match, status_pocess):
                            both_emoji = True
                            break
                
                if not (re.findall(':P', status_pocess) or re.findall(':p', status_pocess)
                        or re.findall('RT', status_pocess) or both_emoji):
                    status_pocess = re.sub('\n', ' ', status_pocess)                    
                    i = 0
                    is_not_existed = True
                    patiences = 0
                    status_pocess = str(sentive) + " " + status_pocess + "\n"
                    
                    for line in reversed(open("./train_data/en-data/raw/metatweets").readlines()):
                        i += 1
                        if i == num_of_check_lines:
                            break
                        if status_pocess == line:
                            is_not_existed = False
                            patiences += 1
                            break
                    if(patiences == num_of_patience):
                        break
                    
                    if len(status_pocess.split(' ')) >= 7 and is_not_existed:
                        fileTraining.write(status_pocess)
                    fileTraining.close()
                        
        if sumPages == 175:
            return 0
        
    
        # Print search info
        print 'Page %d, %d statuses' %(page_idx, len(search_results['statuses']))
    return sumPages



os.mkdir('./train_data')
sumPages = 0
while (True):
    sumPages = getTweet(':)', sumPages)
    print "Done with happy emoticon"
    if sumPages == 0:
        time.sleep(900)
        sumPages = 0
    sumPages = getTweet(':(', sumPages)
    print "Done with sad emoticon"
    if sumPages == 0:
        time.sleep(900)
        sumPages = 0