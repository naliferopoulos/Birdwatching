import socket
import dns.resolver

whitelist = ['twitter.com','facebook.com','fb.me','apple.com','apple.co','snapchat.com','billboard.com','youtube.com','youtu.be','spotify.com','github.com','yahoo.com','fbi.gov','goo.gl','instagram.com','buzzfeed.com','amazon.com','vine.co','twimg.com','persiscope.tv','microsoft.com','fb.on','bit.ly','nike.com']

def is_not_registered(url):
	# First verify that we did not split at a TLD.
	try:
		dns.resolver.query(url + '.', 'SOA')
		return False
	except:
		pass

	try:
		socket.gethostbyname(url)
		return False

	except Exception:
		return True

def analyze(account, tweets):
    checked = []
    takeovers = []

    for tweet in tweets:
        urls = tweet['entities']['urls']
        for url in urls:
            expanded_url = url["expanded_url"]
            expanded_url = expanded_url.replace("http://","").replace("https://","").replace("www.", "").split("/")[0].split(".")
            expanded_url = expanded_url[len(expanded_url)-2:len(expanded_url)]
            expanded_url = '.'.join(x for x in expanded_url)
            
            if expanded_url not in whitelist and expanded_url not in checked:
                if is_not_registered(expanded_url):
                    print("[" + account + "] Takeover found: " + url["expanded_url"])
                    takeovers.append(url["expanded_url"])
                else:
                    checked.append(expanded_url)

    try:
        f = open('results/' + account + '/takeovers.txt', 'w', encoding='utf8')
    except:
        print('[!] Could not open output file!')

    try:
        for takeover in takeovers:
            try:
                    f.write(url["expanded_url"] + "\n")
            except:
                print('[!] Unknown encoding in URL!')
                continue
    except:
        print('[!] Unknown error! Attempting to gracefully stop.')

    finally:
        f.close()
