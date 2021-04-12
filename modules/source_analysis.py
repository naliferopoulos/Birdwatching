import operator

def analyze(account, tweets):
    sources = {}

    # Identify the main source
    for t in tweets:
        if t["source"] in sources:
            sources[t["source"]] = sources[t["source"]] + 1
        else:
            sources[t["source"]] = 1

    main = max(sources.items(), key=operator.itemgetter(1))[0]

    print("[" + account + "] Main source identified as '" + main + "'")

    for source in sources:
        print("[" + account + "] " + str(sources[source]) + " tweets from source '" + source + "'")

    try:
        f = open('results/' + account + '/unusual_sources.txt', 'w', encoding='utf8')
    except:
        print('[!] Could not open output file!')

    try:
        for t in tweets:
            try:
                if not t["source"] == main:
                    f.write(t["text"] + "\n")
            except:
                print('[!] Unknown encoding in tweet!')
                continue
    except:
        print('[!] Unknown error! Attempting to gracefully stop.')

    finally:
        f.close() 