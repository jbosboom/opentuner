#!/usr/bin/python

import adddeps #fix sys.path
from squarecover import SquareCover

import json
import requests
import argparse
import opentuner
from opentuner.tuningrunmain import TuningRunMain

with open('key.txt', 'r') as keyfile:
  API_KEY = keyfile.read()[:-1]
ENV = 'trial'
BASE_URL = 'http://techchallenge.cimpress.com'
get_url = '{0}/{1}/{2}/puzzle'.format(BASE_URL, API_KEY, ENV)
post_url = '{0}/{1}/{2}/solution'.format(BASE_URL, API_KEY, ENV)

args = argparse.ArgumentParser(parents=opentuner.argparsers()).parse_args()

puzzle = json.loads(requests.get(get_url).text)
print puzzle

tuner = SquareCover(args, puzzle['puzzle'])
TuningRunMain(tuner, args).main()
cover = tuner.cover

solution = {'id': puzzle['id'], 'squares': cover}
response = requests.post(post_url, data=json.dumps(solution)).text
print response
