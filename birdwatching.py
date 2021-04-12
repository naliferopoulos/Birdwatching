#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import tweepy
import importlib
import os
import time
import threading
import sys
import re
from secrets import consumer_key, consumer_secret, access_token, access_token_secret

# Thread List
threads = []

# Tweet Fetcher
class Fetcher (threading.Thread):
    def __init__(self, accounts):
        threading.Thread.__init__(self)
        self.accounts=accounts

    def run(self):
        fetch(self.accounts)

def get_all_tweets(screen_name):
	alltweets = []
	new_tweets = api.user_timeline(screen_name = screen_name, count=200)
	alltweets.extend(new_tweets)
	oldest = alltweets[-1]['id'] - 1
	while len(new_tweets) > 0:
		new_tweets = api.user_timeline(screen_name = screen_name, count=200, max_id=oldest)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1]['id'] - 1
		print("%s tweets downloaded so far for %s..." % ((len(alltweets)), "@" + screen_name))
	return alltweets

def get_accounts():
	acc=[]
	with open('accounts.txt') as f:
		for l in f.readlines():
			account = l.replace('\n', '')
			if not l.startswith('#') and not l.startswith('\n'):
				acc.append(account)
				if not os.path.exists('results/' + account):
					os.makedirs('results/' + account)
		return acc

def run_modules(account, tweets):
	try:
		files = os.listdir("modules")
	except:
		print("[!] Could not list modules directory!")
		return

	
	for file in files:
		if file.endswith(".py"):
			try:
				module = importlib.import_module("modules" + "." + file[:-3])
			except:
				print("[!] Could not import '" + file + "'")
				continue
			try:
				analysis = getattr(module, 'analyze')
			except:
				print("[!] '" + file + "' is not an Analyzer!")
				continue
			
			try:
				analysis(account, tweets)
			except Exception as e:
				print("[!] Error while running '" + file + "'" + "(" + print(e) + ")")


def fetch(accounts):
	crawled_tweets = []

	lock.acquire()

	if len(accounts) == 0:
		done = True
		lock.release()
		return

	acc = accounts.pop(0)
	lock.release()
	tweets = get_all_tweets(acc)
	for tweet in tweets:
		if 'RT' not in tweet['text']:
			crawled_tweets.append(tweet)

	thread1 = Fetcher(accounts)
	threads.append(thread1)
	thread1.daemon = True
	thread1.start()

	run_modules(acc, crawled_tweets)

	try:
		f = open('results/' + acc + '/tweets.txt', 'w', encoding='utf8')
	except:
		print('[!] Could not open output file!')
	
	try:
		for t in crawled_tweets:
			try:
				f.write('\t' + t["text"])
			except:
				print('[!] Unknown encoding in tweet!')
				continue
	except:
		print('[!] Unknown error! Attempting to gracefully stop.')

	finally:
		f.close() 

	print("[" + acc + "] " + str(len(crawled_tweets)) + " tweets crawled.")	


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())

accounts = get_accounts()

print("Target List")
print("===========")
for acc in accounts:
	print("\t" + acc)

lock = threading.Lock()

for x in range(len(accounts)):
	thread1 = Fetcher(accounts)
	threads.append(thread1)
	thread1.daemon = True
	thread1.start()

while True:
	should_exit = True

	for i in threads:
		if i.is_alive():
			should_exit = False
			time.sleep(1)
	
	if should_exit:
		break

print("[+] Done!")