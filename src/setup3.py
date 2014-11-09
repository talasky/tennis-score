#!/usr/bin/python

"""
setup3.py
*****************************************************
* Copyright 2014, Ty A. Lasky                       *
* Released under the GNU General Public License 3.0 *
* See LICENSE.txt for license information.          *
*****************************************************

Third setup dialog. Gets all remaining setup information, including players.
Based on MVC architecture.

Exported classes:

Setup3 -- Third setup dialog, get player names.
"""
import util
py  = 2
try:
	import Tkinter as tk
except:
	import tkinter as tk
	py = 3
import player
import sys

baseUrl = 'http://tylasky.com/res/tennisScore/'
mensSinglesUrl = baseUrl + 'menSingles.txt'
womensSinglesUrl = baseUrl + 'womenSingles.txt'
mensDoublesUrl = baseUrl + 'menDoubles.txt'
womensDoublesUrl = baseUrl + 'womenDoubles.txt'

menuWidth = 29

class Setup3(tk.Toplevel):
	"""Third setup dialog, get player names."""
	def __init__(self, master, mens, doubles):
		"""
		@type master: Toplevel widget
		@param: master: Main application window.
		@type mens: integer
		@param mens: Flag, 0 - women's match, 1 = men's match, 2 = mixed match.
		@type doubles: boolean
		@param doubles: Flag, True if this is a doubles match.
		"""
		tk.Toplevel.__init__(self, master)
		self.overrideredirect(1) # No window decorations, no way to close window
		self.geometry('+100+100')
		self.numberOfSets = tk.IntVar()
		self.numberOfSets.set(3)
		self.doubles = doubles
		self.player1String = tk.StringVar(self) # First player, team 1, string including all object properties in parseable format
		self.player2String = tk.StringVar(self) # First player, team 2, string including all object properties in parseable format
		self.player1aString = tk.StringVar(self) # Second player, team 1, string including all object properties in parseable format
		self.player2aString = tk.StringVar(self) # Second player, team 2, string including all object properties in parseable format
		self.duplicateLastName = set([])

		if doubles: # Doubles match
			tk.Radiobutton(self, text="Two sets + tiebreak", padx = 20, variable = self.numberOfSets,
				value = 2, width = 20, anchor='w').pack()
			tk.Radiobutton(self, text="Three sets", padx = 20, variable = self.numberOfSets,
				value = 3, width = 20, anchor='w').pack()
		elif mens == 1: # Mens singles match
			tk.Radiobutton(self, text="Three sets", padx = 20, variable = self.numberOfSets,
				value = 3, width = 20, anchor='w').pack()
			tk.Radiobutton(self, text="Five sets", padx = 20, variable = self.numberOfSets,
				value = 5, width = 20, anchor='w').pack()

		if not doubles: # Singles match
			if (mens == 0): # Womens singles match
				# Get list of womens singles players
				plist = readPlayers(womensSinglesUrl)
			else: # Mens singles match
				# Get list of mens singles players
				plist = readPlayers(mensSinglesUrl)
			listToCheck = plist
			self.player1String.set(plist[0]) # default value
			self.player2String.set(plist[1]) # default value
			tk.Label(self,text='Player 1').pack()
			# Get a formatted dropdown menu for player 1
			w1 = myDropdown(self,self.player1String,plist)
			w1.pack()
			tk.Label(self,text='Player 2').pack()
			# Get a formatted dropdown menu for player 2
			w2 = myDropdown(self,self.player2String,plist)
			w2.pack()
		else: # Doubles match
			if(mens == 0):  # Womens doubles match
				# Get list of womens doubles players
				plist1 = plist2 = readPlayers(womensDoublesUrl)
				listToCheck = plist1[:]
			elif(mens == 1): # Mens doubles match
				# Get list of mens doubles players
				plist1 = plist2 = readPlayers(mensDoublesUrl)
				listToCheck = plist1[:]
			else: # Mixed doubles match
				# Get list of womens doubles players
				plist1 = readPlayers(womensDoublesUrl)
				# Get list of mens doubles players
				plist2 = readPlayers(mensDoublesUrl)
				listToCheck = plist1[:]
				listToCheck.extend(plist2)
			self.player1String.set(plist1[0]) # default value
			self.player2String.set(plist1[2]) # default value
			self.player1aString.set(plist2[1]) # default value
			self.player2aString.set(plist2[3]) # default value
			tk.Label(self, text='Team 1').pack()
			# Get a formatted dropdown menu for team 1, player 1
			w1 = myDropdown(self,self.player1String,plist1)
			w1.pack()
			# Get a formatted dropdown menu for team 1, player 2
			w1a = myDropdown(self,self.player1aString,plist2)
			w1a.pack()
			tk.Label(self, text='Team 2').pack()
			# Get a formatted dropdown menu for team 2, player 1
			w2 = myDropdown(self,self.player2String,plist1)
			w2.pack()
			# Get a formatted dropdown menu for team 2, player 2
			w2a = myDropdown(self,self.player2aString,plist2)
			w2a.pack()

		# Find duplicate last names (used to determine need for first initial)
		self.duplicateLastName = duplicates(listToCheck)

		self.startButton = tk.Button(self, text='Start', width=8)
		self.startButton.pack(side='left')
		self.title("Match Info #3") # Won't have any effect, given no decorations
		util.center(self)

	def getNumberOfSets(self):
		"""
		Returns number of sets.
		@rtype: integer
		@return: Number of sets.
		"""
		return self.numberOfSets.get()

	def getTeamStrings(self):
		"""
		Returns list of strings for the players on each team.
		@rtype: list of strings
		@return: List of strings for the players on each team. Each string includes all object properties in parseable format.
		"""
		if not self.doubles: # Singles match
			return [self.player1String.get(), self.player2String.get()]
		else: # Doubles match
			return [[self.player1String.get(), self.player1aString.get()],
					[self.player2String.get(), self.player2aString.get()]]

	def loadPlayerLists(self):
		"""
		Loads all four player lists.
		NOTE: Not used, loading player lists only when needed.
		"""
		self.menSinglesPlayers = readPlayers(mensSinglesUrl)
		self.womenSinglesPlayers = readPlayers(womensSinglesUrl)
		self.menDoublesPlayers = readPlayers(mensDoublesUrl)
		self.womenDoublesPlayers = readPlayers(womensDoublesUrl)

def myDropdown(master, var, optList):
	"""
	Provides a stylized option menu / dropdown list.
	@type master: Toplevel widget
	@param master: Window to host the menu.
	@type var: Tkinter variable
	@param var: The variable to be set by the option menu.
	@type optList: list of strings
	@param optList: List of strings for the option menu.
	@rtype: OptionMenu
	@return: The constructed option menu / dropdown list.
	"""
	w = tk.OptionMenu(master, var, *optList)
	w.config(bg='black',fg='white', width=menuWidth)
	w['menu'].config(bg='black',fg='white')
	return w

def readPlayers(url):
	"""
	Reads a player list from the given URL.
	@type url: strings
	@param url: The URL that holds the player list information.
	@rtype: list of strings
	@return: List of players in a special format that can be parsed into a player object.
	"""
	# Load the player list from URL into a string
	txt = util.getUrlAsString(url)
	if not txt is None:
		players = []
		for line in util.lineIter(txt): # Decode the player list from known format of tennischannel.com files
			line = util.decode(line)
			strings = line.split("\t")
			rank = int(strings[0])
			strings = strings[1].split(",")
			lastName = strings[0]
			strings = strings[1].split("(")
			firstName = strings[0].strip()
			country = strings[1][0:3]
			# Creating list of easily parsed strings representative of player objects.
			# These strings are "pretty" enough to use in dropdown list.
			players.append('{}. {}, {} ({})'.format(rank, lastName, firstName, country))
	else:
		print("readPlayers: Couldn't open {}, exiting.".format(url))
		# Maybe something better to do than exit. Consider in future version.
		sys.exit(1)
	return players

def duplicates(playerList):
	"""
	Checks player list to see if there are any duplicate last names.
	@type playerList: list of strings
	@param playerList: List of players, each as string formatted as returned by readPlayers.
	@rtype: set
	@return: Set of last names that appear more than once in playerList.
	"""
	lastNames = []
	dups = set([])
	for pString in playerList:
		s = pString.split('.') # strip off rank
		s = s[1].split(',')
		last = s[0].strip()
		if last in lastNames:
			dups.add(last)
		lastNames.append(last)
	return dups

if __name__ == '__main__':
	p = readPlayers(womensSinglesFile)
	print(p)
	p = readPlayers(mensSinglesFile)
	print(p)
	p = readPlayers(womensDoublesFile)
	print(p)
	p = readPlayers(mensDoublesFile)
	print(p)