from pprint import pprint
import json
import requests
import bs4
import tweepy
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import twitter
sys.path.insert(0, '../../../')

from sven.src.credentials import twitter_credentials
from sven.src.data.cbpro_cryptocurrencies import currencies


class TwitterDataHandler:

	def __init__(self):
		self.api_key = twitter_credentials.get('api_key')
		self.api_secret = twitter_credentials.get('api_secret')
		self.access_token = twitter_credentials.get('access_token')
		self.access_token_secret = twitter_credentials.get('access_token_secret')
		self.auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
		self.auth.set_access_token(self.access_token_key, self.access_token_secret)
		self.api = tweepy.API(self.auth)

	def get_tweets(self, symbol):
		pass

	def udpate_twitter_database(self, symbol):

		#
		pass
