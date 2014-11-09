#!/usr/bin/python

"""
tennisScore.py
*****************************************************
* Copyright 2014, Ty A. Lasky                       *
* Released under the GNU General Public License 3.0 *
* See LICENSE.txt for license information.          *
*****************************************************

Simple test of reading players from URL
"""

import sys
sys.path.append("../src") # so can find util module
import util
import time

baseUrl = 'http://tylasky.com/res/tennisScore/'
mensSinglesUrl = baseUrl + 'menSingles.txt'
womensSinglesUrl = baseUrl + 'womenSingles.txt'
mensDoublesUrl = baseUrl + 'menDoubles.txt'
womensDoublesUrl = baseUrl + 'womenDoubles.txt'

urlChoices = (mensSinglesUrl, mensDoublesUrl, womensSinglesUrl, womensDoublesUrl)

if len(sys.argv) != 2: # No commandline URL, will default to women's singles
	print("\nUsage: python playerReader.py url")
	print("where url is in:\n")
	for u in urlChoices:
		print(u)
	print("\nDefaulting to women's singles\n")
	time.sleep(5) # pause 5 seconds
	url = womensSinglesUrl
else: # use the commandline URL
	url = sys.argv[1]

txt = util.getUrlAsString(url)
if not txt is None:
	players = []
else:
	print("playerReader: Couldn't open {}, exiting.".format(url))
	sys.exit(1)

for line in util.lineIter(txt):
	line = util.decode(line)
	strings = line.split("\t")
	rank = int(strings[0])
	strings = strings[1].split(",")
	lastName = strings[0]
	strings = strings[1].split(" ")
	firstName = strings[1]
	country = strings[2][1:4]
	print("Rank: {}\tFirst: {}\tLast: {}\tCountry: {}".format(rank, firstName, lastName, country))
	# If imported ../src/player could now create player object.