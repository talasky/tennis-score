#!/usr/bin/python
"""
player.py

Copyright 2014, Ty A. Lasky

Released under the GNU General Public License 3.0

See LICENSE.txt for license information.

---------------------------------------------------

The player and team classes for tennis scoreboard based on MVC architecture.

Exported classes:

Player -- Represents an indivudiual tennis player.

Team -- Represents a group of players (1 or 2).
"""

class Player():
	"""Represents an indivudiual tennis player."""
	def __init__(self, rank, first, last, country):
		"""
		@type rank: string
		@param rank: Player's current rank.
		@type first: string
		@param first: Player's first name.
		@type last: string
		@param last: Player's last name.
		@type country: string
		@param rank: Player's country (IOC three letter country code)
		"""
		self.rank = int(rank)
		self.firstName = first
		self.lastName = last
		self.countryCode = country # IOC three letter country code

	def __repr__(self):
		"""
		Provides detailed representation of a Player object.
		@rtype: string
		@return: Detailed representation of a Player object.
		"""
		return "rank: {}, firstName: {}, lastName: {}, countryCode: {}".format(repr(self.rank),
			repr(self.firstName), repr(self.lastName), repr(self.countryCode))

	def __str__(self):
		"""
		Provides a pretty string for the Player object.
		@rtype: string
		@return: Pretty string for the Player object.
		"""
		# May be other Asian countries where this is appropriate. Perhaps South Korea.
		if self.countryCode in ("CHN","TPE"): # Reverse family and given names for China / Taipei / Taiwan players
			name = "{} {}".format(self.lastName,self.firstName)
		else:
			name = "{} {}".format(self.firstName,self.lastName)
		return name

	def __hash__(self):
		"""
		Hash function for Player object. Used in generating sets.
		@rtype: integer
		@return: The hash value of the object.
		"""
		return hash((self.rank,self.lastName))
		# Note: rank should be sufficient. I'm including last name for a little extra assurance of uniqueness.
		# hash only takes one argument. So, using a tuple of values to hash.

	def __eq__(self, other):
		"""
		Tests equality of Player object vs. other Player object.
		@type other: Player
		@param other: The other Player object.
		@rtype: boolean
		@return: True if current Player = other Player.
		"""
		return self.__dict__ == other.__dict__

	def __ne__(self,other):
		"""
		Tests inequality of Player object vs. other Player object.
		@type other: Player
		@param other: The other Player object.
		@rtype: boolean
		@return: True if current Player is not equal to other Player.
		"""
		return not self.__eq__(other)

	""" Here, '__lt__' and '__gt__ are defined so that a list of players will sort in 
	ascending order by their rank. I.e. highest rank player will be first in a sorted
	list. This means tha in a direct comparison of two players, i.e. for e.g.,
	player1 > player2, this will be true of player1 rank is a bigger number than
	player2 rank. Which may be a bit countierintuitive. """

	def __lt__(self,other):
		"""
		Tests whether Player rank is less than other Player object rank.
		@type other: Player, or integer
		@param other: The other Player object, or a rank number.
		@rtype: boolean
		@return: True if current Player rank is less than other Player rank, or provided rank. (rank = 1) is less than (rank = 2).
		"""
		if hasattr(other,'rank'):
			return self.rank < other.rank
		else:
			return self.rank < other

	def __gt__(self,other):
		"""
		Tests whether Player rank is greater than other Player object rank.
		@type other: Player, or integer
		@param other: The other Player object, or a rank number.
		@rtype: boolean
		@return: True if current Player rank is greater than other Player rank, or provided rank. (rank = 2) is greater than (rank = 2).
		"""
		if hasattr(other,'rank'):
			return self.rank > other.rank
		else:
			return self.rank > other

	def __le__(self,other):
		"""
		Tests whether Player rank is less than or equal to other Player object rank.
		@type other: Player, or integer
		@param other: The other Player object, or a rank number.
		@rtype: boolean
		@return: True if current Player rank is less than or equal to other Player rank, or provided rank. (rank = 1) is less than or equal to (rank = 2)
		"""
		return self.__eq__(other) or self.__lt__(other)

	def __ge__(self,other):
		"""
		Tests whether Player rank is greater than or equal to other Player object rank.
		@type other: Player, or integer
		@param other: The other Player object, or a rank number.
		@rtype: boolean
		@return: True if current Player rank is greater than or equal to other Player rank, or provided rank.  (rank = 2) is greater than or equal to (rank = 2).
		"""
		return self.__eq__(other) or self.__gt__(other)
		
	def scoreName(self, dups=set([]), special = []):
		"""
		Provides the scoreboard name for a Player.
		@type dups: list of strings
		@param dups: List of last names that appear for multiple players.
		@type special: list of strings
		@param special: List of last names that appear for multiple players, and have same first initial.
		@rtype: string
		@return: The scoreboard name for the Player.
		"""
		if self.lastName not in dups:
			return self.lastName
		else:
			inits = self.getFirstInits(special)
			return inits + " " + self.lastName

	def buttonName(self, dups=set([]), special = []):
		"""
		Provides the scoring button name for a Player.
		@type dups: list of strings
		@param dups: List of last names that appear for multiple players.
		@type special: list of strings
		@param special: List of last names that appear for multiple players, and have same first initial.
		@rtype: string
		@return: The scoring button name for the Player.
		"""
		return self.scoreName(dups, special)
		
	def getRank(self):
		"""
		Returns the Player's rank.
		@rtype: integer
		@return: The Player's rank.
		"""
		return self.rank

	def getFirstName(self):
		"""
		Returns the Player's first name.
		@rtype: string
		@return: The Player's first name.
		"""
		return self.firstName

	def getLastName(self):
		"""
		Returns the Player's last name.
		@rtype: string
		@return: The Player's last name.
		"""
		return self.lastName

	def getFirstInits(self, special = []):
		"""
		Returns the Player's first initial(s). One for most players, two inits for special cases.
		@rtype: string
		@return: The Player's first initial(s).
		"""
		for case in special: # Special names have same last name and first initial, e.g. Karolina and Kristyna Pliskova
			if self.lastName == case[0]:
				if self.firstName[0] == case[1]:
					return self.firstName[0:2]+"."
		return fancyFirstInits(self.firstName) # Not a special case, just use normal initial(s).

	def getCountryCode(self):
		"""
		Returns the Player's IOC three letter country code.
		@rtype: string
		@return: The Player's IOC three letter country code.
		"""
		return self.countryCode

	def getPhotoName(self):
		"""
		Returns the photo file name for the Player.
		@rtype: string
		@return: The photo file name for the Player.
		"""
		# Sample photo name: "an_ivanovic.jpg" for Ana Ivanovic
		return self.firstName[0:2] + "_" + self.lastName + ".jpg"

class Team():
	"""Represents a group of players (1 or 2)."""
	def __init__(self, playerA, playerB=None):
		"""
		@type playerA: Player
		@param playerA: The first player on the team.
		@type playerB: Player
		@param playerB: The second player on the team. Will be None for singles.
		"""
		self.playerA = playerA
		self.playerB = playerB # None if singles match

	def __repr__(self):
		"""
		Provides detailed representation of a Team object.
		@rtype: string
		@return: Detailed representation of a Team object.
		"""
		return "playerA: {}, playerB: {}".format(repr(self.playerA), repr(self.playerB))

	def __str__(self):
		"""
		Provides a pretty string for the Team object.
		@rtype: string
		@return: Pretty string for the Team object.
		"""
		if self.playerB is None: # Singles match
			return str(self.playerA)
		else: # Doubles match
			return str(self.playerA) + " and " + str(self.playerB)

	def scoreName(self, dups=set([]), special = []):
		"""
		Provides the scoreboard name for a Team.
		@type dups: list of strings
		@param dups: List of last names that appear for multiple players.
		@type special: list of strings
		@param special: List of last names that appear for multiple players, and have same first initial.
		@rtype: string
		@return: The scoreboard name for the Team.
		"""
		if self.playerB is None: # Singles match
			return self.playerA.scoreName(dups, special)
		else: # Doubles match
			return self.playerA.scoreName(dups, special) + " / " + self.playerB.scoreName(dups, special)

	def buttonName(self, dups=set([]), special = []):
		"""
		Provides the scoring button name for a Team.
		@type dups: list of strings
		@param dups: List of last names that appear for multiple players.
		@type special: list of strings
		@param special: List of last names that appear for multiple players, and have same first initial.
		@rtype: string
		@return: The scoring button name for the Team.
		"""
		if self.playerB is None: # Singles match
			return self.playerA.buttonName(dups, special)
		else: # Doubles match
			return self.playerA.buttonName(dups, special) + " /\n" + self.playerB.buttonName(dups, special)

	def getRank(self):
		"""
		Returns the Team's rank(s).
		@rtype: integer
		@return: The Team's rank(s).
		"""
		if self.playerB is None: # Singles match
			return str(self.playerA.getRank())
		else: # Doubles match
			return str(self.playerA.getRank()) + "/" + str(self.playerB.getRank())

	def getFirstName(self):
		"""
		Returns the Team's first name(s).
		@rtype: string
		@return: The Team's first name(s).
		"""
		if self.playerB is None: # Singles match
			return self.playerA.getFirstName()
		else: # Doubles match
			return self.playerA.getFirstName() + " and " + self.playerB.getFirstName()

	def getLastName(self):
		"""
		Returns the Team's last name(s).
		@rtype: string
		@return: The Team's last name(s).
		"""
		if self.playerB is None: # Singles match
			return self.playerA.getLastName()
		else: # Doubles match
			return self.playerA.getLastName() + " and " + self.playerB.getLastName()

	def getCountryCode(self):
		"""
		Returns the Team's IOC three letter country code(s).
		@rtype: tuple of strings
		@return: The Team's IOC three letter country code.
		"""
		if self.playerB is None: # Singles  match
			return (self.playerA.getCountryCode(),)
		else: # Doubles match
			return (self.playerA.getCountryCode(), self.playerB.getCountryCode())

def fancyFirstInits(firstName):
	"""
	Breaks a first name into initials. Handles hyphenated names.
	@type firstName: string
	@param firstName: Person's first name.
	@rtype: string
	@return: Initials corresponding to first name. Includes hyphens as needed.
	"""
	# May be other special case first names. Handle those when run into them, later version.
	inits = ''
	strings = firstName.split() # first, break into chunks by spaces
	for word in strings:
		if '-' in word: 		# handle hyphens
			sub = word.split('-')
			for s in sub[:-1]:
				inits += s[0]+".-"
			inits+= sub[-1][0]+"."
		else:
			inits += word[0]+"."
	return inits

if __name__ == '__main__':
	dups = set(['Williams', 'Pliskova', 'Bryan']) # There may be others, or less, depending on retirements.
	special = [('Pliskova', 'K')]
	serena = Player("1","Serena","Williams","USA")
	li = Player("2","Na","Li","CHN")
	halep = Player("3","Simona","Halep","ROU")
	kvitova = Player("4","Petra","Kvitova","CZE")
	radwanska = Player("5","Agnieszka", "Radwanska","POL")
	scrambled = [radwanska, li, serena, kvitova, halep]
	unscrambled = scrambled[:]
	unscrambled.sort()
	print("Scrambled players are {}".format(scrambled))
	print("Unscrambled players are {}".format(unscrambled))
	print(serena)
	print("Scorename: " + serena.scoreName(dups=dups,special=special))
	print(radwanska)
	print("Scorename: " + radwanska.scoreName())
	print(li)
	print("Scorename: " + li.scoreName())
	print("Serena = Serena is {}".format(serena==serena))
	print("Aga = Halep is {}".format(radwanska==halep))
	print("Halep < Serena is {}".format(halep < serena))
	print("Li > Aga is {}".format(li > radwanska))
	print("Kvitova >= Aga is {}".format(kvitova >= radwanska))
	print("Halep >= Halep is {}".format(halep >= halep))
	print("Aga > 6 is {}".format(radwanska > 6))
	print("Serena < 1 is {}".format(serena < 1))
	print("Kvitova > 5 is {}".format(kvitova > 5))
	print("Kvitova < 1 is {}".format(kvitova < 1))
	team1 = Team(radwanska, halep)
	team2 = Team(li, kvitova)
	print("repr(team1): " + repr(team1))
	print("repr(team2): " + repr(team2))
	print("Team 1: {}".format(team1))
	print("Team 2: {}".format(team2))
	print("Team 1 score name: {}".format(team1.scoreName()))
	myList = [radwanska, li, serena, kvitova, halep, li]
	print("Type of myList is: {}".format(type(myList)))
	print("Dict of halep is:")
	print(halep.__dict__)
	mySet = set(myList)
	print("Type of mySet is: {}".format(type(mySet)))
	if len(set(myList)) == len(myList):
		print("No duplicates in {}".format(myList))
	else:
		print("Duplicates found in {}".format(myList))

	team1 = Team(li, halep)
	team2 = Team(radwanska) #, kvitova)
	print("Team1: {}".format(team1))
	print("Team2: {}".format(team2))
	print("Team1 countries: {}".format(team1.getCountryCode()))
	print("Team2 countries: {}".format(team2.getCountryCode()))
	teams = [team1, team2]
	print("Teams are: {}".format(teams))
	kapliskova = Player("48", "Karolina", "Pliskova", "CZE")
	krpliskova = Player("94", "Kristyna", "Pliskova", "CZE")
	print(kapliskova)
	print("Scorename: " + kapliskova.scoreName(dups=dups,special=special))
	print(krpliskova)
	print("Scorename: " + krpliskova.scoreName(dups=dups,special=special))
	tf = Player("60", "Maria-Teresa", "Torro-Flor", "ESP")
	js = Player("24", "Juan Sebastian", "Cabal", "COL")
	dups = set(['Cabal', 'Torro-Flor'])
	print(tf)
	print("Scorename: " + tf.scoreName(dups=dups,special=special))
	print(js)
	print("Scorename: " + js.scoreName(dups=dups,special=special))
	jhyphenboy = Player("24", "Juan-Thomas-Yglesias Sebastian-Joeseph Joe-Bob-At-The-Drivein", "Cabal", "COL")
	print(jhyphenboy)
	print("Scorename: " + jhyphenboy.scoreName(dups=dups,special=special))