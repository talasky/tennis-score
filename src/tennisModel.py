#!/usr/bin/python
"""
tennisModel.py

Copyright 2014, Ty A. Lasky

Released under the GNU General Public License 3.0

See LICENSE.txt for license information.

---------------------------------------------------

The model for tennis scoreboard based on MVC architecture.

Exported classes:

Model -- Provides fields and logic for a tennnis match.
"""

import player

import sys
sys.path.append('../lib')
import util
from observable import Observable

DEBUG = False

class Model:
	"""Provides fields and logic for a tennnis match."""
	def __init__(self):
		self.noEndingTiebreak = Observable(False)
		self.doublesMatch = Observable(False)
		self.mensMatch = Observable(0)
		self.team = Observable(["",""])
		self.gameScore = Observable([0,0])
		self.setScore = Observable([[0,0],[0,0],[0,0],[0,0],[0,0]])
		self.currentSet = Observable(0)
		self.matchScore = Observable([0,0])
		self.tiebreak = Observable(False)
		self.message = Observable("")
		self.server = Observable(-1)
		self.winner = Observable(-1)
		self.numberOfSets = Observable(0)
		self.matchOver = False
		self.winSets = Observable(0)
		self.matchType = Observable("")
		self.tiebreakToWin = 7 # Default for normal tiebreak game. Will set to 10 for end tiebreak in doubles match.
		self.matchPointCount = [0,0]
		self.setPointCount = [0,0]
		self.breakPointCount = [0,0]
		self.deuceCount = 0
		self.duplicateLastName = set([])
		self.specialCaseNames = []
		self.teamScoreNames = ["",""]

	def setNoEndingTiebreak(self,bool):
		"""
		Establishes whether final set can end with a tiebreak.
		@type bool: boolean
		@param bool: Flag, True if final set can NOT end with a tiebreak.
		"""
		self.noEndingTiebreak.set(bool)

	def setDoublesMatch(self,bool):
		"""
		Establishes whether this is a doubles or singles match.
		@type bool: boolean
		@param bool: Flag, True if this is a doubles match.
		"""
		self.doublesMatch.set(bool)

	def setMensMatch(self,i):
		"""
		Establishes whether this is a men's match, women's, or some form of doubles. Sets that field, also the corresponding number of sets.
		@type i: integer
		@param i: Flag, 0 = women's match, 1 = men's match, 2 = mixed doubles match.
		"""
		self.mensMatch.set(i)
		if (self.mensMatch.get() == 1):
			self.numberOfSets.set(5) # I'm assuming 5 sets for men. This may not always be the case, in which case I'll include in dialog.
			self.winSets.set(3) # I'm assuming 5 sets for men. This may not always be the case, in which case I'll include in dialog.
		else: # either womens, or some form of doubles. All have three sets.
			self.numberOfSets.set(3)
			self.winSets.set(2)

	def changeServer(self):
		"""
		Swaps the serving team / player.
		"""
		# Simple toggle of server team
		if self.server.get() == 0:
			self.server.set(1)
		else:
			self.server.set(0)

	def gameDelta(self):
		"""
		Returns the absolute value of the difference in the current game score.
		@rtype: integer
		@return: The absolute value of the difference in the current game score.
		"""
		return scoreDelta(self.gameScore.get())

	def gamePoint(self, score):
		"""
		Returns whether the current score corresponds to game point.
		@type score: list of integers
		@param score: The current game score.
		@rtype: boolean
		@return: Whether the current score corresponds to game point.
		"""
		gameLeader = leader(score)
		if gameLeader == -1: # Game is tied
			return False
		# All below, game is not tied.
		# Tiebreak game
		if (self.tiebreak.get()) and (score[gameLeader] > self.tiebreakToWin - 2):
			return True
		# Regular game
		if (not self.tiebreak.get()) and (score[gameLeader] > 2):
			return True
		return False

	def breakPoint(self,score):
		"""
		Returns whether the current score corresponds to break point.
		@type score: list of integers
		@param score: The current game score.
		@rtype: boolean
		@return: Whether the current score corresponds to break point.
		"""
		if not self.gamePoint(score):
			return False
		# All below, it is game point
		util.dbgprint(DEBUG, "Break point: it is Game point")
		# No break point in tiebreak game
		if self.tiebreak.get():
			return False
		gameLeader = leader(score)
		if gameLeader == -1: # I think this cannot be true if get here. Maybe remove this.
			return False
		util.dbgprint(DEBUG, "breakPoint: Game leader is {}\tServer is: {}\tSet score is: {}\tGame score is: {}".format(
			self.team[gameLeader],self.server.get(),self.setScore.get(),score))
		if gameLeader != self.server.get(): # Game point, and receiver is ahead, so it's break point
			return True

	def setPoint(self,score):
		"""
		Returns whether the current score corresponds to set point.
		@type score: list of integers
		@param score: The current game score.
		@rtype: boolean
		@return: Whether the current score corresponds to set point.
		"""
		if not self.gamePoint(score):
			return False
		# All below, it is game point
		util.dbgprint(DEBUG, "Set point: it is Game point")
		setScore = self.setScore.get()[self.currentSet.get()]
		setLeader = leader(setScore)
		gameLeader = leader(score)
		util.dbgprint(DEBUG, "setPoint: Set leader is {}\tSet score is: {}\tGame score is: {}".format(
			self.team[setLeader],self.setScore.get(),score))
		# Tiebreak game
		if self.tiebreak.get():
			util.dbgprint(DEBUG, "Tiebreak set point")
			return True
		# Regular game, set not tied, set leader is winning game, and their set score is 5 or higher
		if setLeader != -1 and setLeader == gameLeader and setScore[setLeader] > 4:
			return True

	def matchPoint(self,score):
		"""
		Returns whether the current score corresponds to match point.
		@type score: list of integers
		@param score: The current game score.
		@rtype: boolean
		@return: Whether the current score corresponds to match point.
		"""
		if not self.setPoint(score):
			return False
		# All below, it is set point
		util.dbgprint(DEBUG, "Match point: it is Set point")
		setScore = self.setScore.get()[self.currentSet.get()]
		gameLeader = leader(score)
		setLeader = leader(setScore)
		# Doubles match
		if self.doublesMatch.get() and self.currentSet.get() + 1 == self.numberOfSets.get():
			util.dbgprint(DEBUG, "Doubles match, last set, so match point.")
			return True
		# Singles match
		util.dbgprint(DEBUG, "matchPoint: Set leader is {}\tMatch score is: {}\tSet score is: {}\tGame score is: {}".format(
			self.team[setLeader],self.matchScore.get(),self.setScore.get(),score))
		# Set point, and game leader match score (# of serts) is one less than tat needed to win
		if self.matchScore.get()[gameLeader] == self.winSets.get() - 1:
			return True

	def messageCheck(self, score):
		"""
		Determines what message should be displayed on scoreboard based on match conditions.
		@type score: list of integers
		@param score: The current game score.
		"""
		# Note: Prefix is way overdone vs. what you see on TV matches. But, it's accurate, and I like it.
		prefix = ("","","Double ","Triple ","Quadruple ","Quintuple ","Sextuple ")
		# Default message is just the match type (e.g. Semifinal)
		# Might want to revise this so default message is more random, e.g. nothing most of time, match type maybe 25% of time. Later version.
		msg = self.matchType.get()
		# Deuce
		if (not self.tiebreak.get()) and (score[0] == 3) and (score[1] == 3):
			self.deuceCount += 1
			if self.deuceCount <= 1: # First deuce
				self.message.set("Deuce")
			else:
				self.message.set("Deuce #{}".format(self.deuceCount)) # Subsequent deuces
			return
		if self.tiebreak.get():
			msg = "Tiebreak"
		delta = scoreDelta(score)
		matchScore = self.matchScore.get()
		matchLeader = leader(matchScore)
		gameLeader = leader(score)
		# Someone has won the match
		if matchLeader != -1 and matchScore[matchLeader] == self.winSets.get():
			self.message.set(str(self.team[matchLeader])+" won " + self.matchOrChampionship() +"!")
			return
		# Game point, check various possibilities
		if self.gamePoint(score): # if get to here, someone is ahead, so gameLeader in {0,1}
			if self.matchPoint(score): # It is match point
				self.matchPointCount[gameLeader] += 1
				if self.matchType.get() == "Championship": # It is match piont in a championship
					s = "Championship Point"
				else:
					s = "Match Point" # It is match point in a regular game, i.e. not championship
				# First match point, show prefix (e.g. Double) along with match point message
				if(self.matchPointCount[gameLeader] <= 1):
					self.message.set(prefix[delta]+s)
				else:
					# Subsequent match point, show match point message along with count for leading player
					self.message.set(s+" #{}".format(self.matchPointCount[gameLeader]))
				return
			if self.setPoint(score):
				self.setPointCount[gameLeader] += 1
				# First set point, show prefix (e.g. Double) along with set point message
				if(self.setPointCount[gameLeader] <= 1):
					self.message.set(prefix[delta]+"Set Point")
				else:
					# Subsequent set point, show set point message along with count for leading player
					self.message.set("Set Point #{}".format(self.setPointCount[gameLeader]))
				return
			if self.breakPoint(score):
				self.breakPointCount[gameLeader] += 1
				# First break point, show prefix (e.g. Double) along with break point message
				if(self.breakPointCount[gameLeader] <= 1):
					self.message.set(prefix[delta]+"Break Point")
				else:
					# Subsequent break point, show break point message along with count for leading player
					self.message.set("Break Point #{}".format(self.breakPointCount[gameLeader]))
				return
		self.message.set(msg)

	def matchOrChampionship(self):
		"""
		Returns whether this is a regular match or a championship.
		@rtype: string
		@return: Either 'championship' or 'match'
		"""
		if self.matchType.get().lower() == 'championship':
			return 'championship'
		else:
			return 'match'

	def incrementGameScore(self,team):
		"""
		Increments the current game score, and handles game logic (win, deuce, tiebreak, and message)
		@type team: integer
		@param team: The team that scored the point.
		"""
		if not self.matchOver:
			#self.message.set("")
			s = self.gameScore.get()
			# Increment score of the team that scored
			s[team] += 1
			util.dbgprint(DEBUG, str(self.team[team])+" " + self.singular('score') + ". Score = "+str(s)+". tiebreak is "+
				str(self.tiebreak.get()))
			if not self.tiebreak.get():
				# NOT a tiebreak
				# Point was Ad, and non-leading player scored, so back to Deuce
				if (s[0]==4) and (s[1]==4):
					s = [3,3]
				# Scoring player just won the game
				if (s[team] > 3) and (scoreDelta(s) > 1):
					util.dbgprint(DEBUG, str(self.team[team])+" "+self.singular('win')+" game.")
					# Reset for next game
					s = [0,0]
					self.breakPointCount = [0,0]
					self.deuceCount = 0
					# Increment the game winning team's set score
					self.incrementSetScore(team)
					if not self.matchOver:
						self.changeServer()
			else:
				# tiebreak
				if (s[0]+s[1]) % 2 == 1: # It's an odd game, so change server.
					self.changeServer()
				if (s[team] >=self.tiebreakToWin) and (scoreDelta(s) > 1):
					# Point winning team just won the tiebreak
					util.dbgprint(DEBUG, str(self.team[team])+" "+self.singular('win')+" tiebreak game.")
					# Increment the game winning team's set score
					self.incrementSetScore(team)
					# Increment the game winning team's match score, as they also won the set.
					self.incrementMatchScore(team)
					# Reset for next game
					s = [0,0]
					self.breakPointCount = [0,0]
					self.deuceCount = 0
					self.tiebreak.set(False)
			# Reset for next game
			self.gameScore.set(s)
			util.dbgprint(DEBUG, "Before message check. Score: {}\tSets:\t{}".format(s,self.setScore.get()))
			# Determine what message should be displayed
			self.messageCheck(s)

	def incrementSetScore(self,team):
		"""
		Increments the current set score (# of games), and handles set logic (win, update match score)
		@type team: integer
		@param team: The team that won the game.
		"""
		s = self.setScore.get()
		thisSet = self.currentSet.get()
		# Increment game winning team's set score
		s[thisSet][team] += 1
		self.setScore.set(s)
		util.dbgprint(DEBUG, "Set: " + str(self.currentSet.get()) + ". Current set score: "+str(s))
		if not self.tiebreak.get():
			# NOT a tiebreak
			if (s[thisSet][team] > 5) and (scoreDelta(s[thisSet]) > 1):
				# Game winners also won the current set
				util.dbgprint(DEBUG, str(self.team[team]) +" "+self.singular('win')+ " set "+str(thisSet))
				# Reset for next set
				self.setPointCount = [0,0]
				self.incrementMatchScore(team)
			if not self.doublesMatch.get() and self.noEndingTiebreak.get() and (thisSet == self.numberOfSets.get()-1):
				# Singles match, and no ending tiebreak, and we're in the final set, so just keep playing games until match winner.
				return
			if (s[thisSet][0]==6) and (s[thisSet][1]==6):
				# We now enter into a tiebreak
				self.tiebreak.set(True)
				self.gameScore.set([0,0])
				util.dbgprint(DEBUG, "Now entering tiebreak")

	def incrementMatchScore(self,team):
		"""
		Increments the match score (# of sets), and handles match logic (win)
		@type team: integer
		@param team: The team that won the set.
		"""
		currSet = self.currentSet.get() + 1
		s = self.matchScore.get()
		# Increment the set winning team's match score
		s[team] += 1
		self.matchScore.set(s)
		util.dbgprint(DEBUG, "Match score in set "+ str(currSet) + " is "+str(s))
		util.dbgprint(DEBUG, "team # is "+str(team)+", with "+str(s[team])+" sets.")
		if s[team] == self.winSets.get():
			# The set winning team has won the match
			self.winner.set(team)
			util.dbgprint(DEBUG, str(self.team[team])+" "+self.singular('win')+" " + self.matchOrChampionship() + "!")
			self.matchOver = True
			self.server.set(-1)
			currSet -= 1
			return
		if self.doublesMatch.get() and self.numberOfSets.get() == 2:
			# It is a doubles match, with two sets
			if s == [1,1]:
				# Each team has won a set, so now it is the final 10-point tiebreak
				self.tiebreak.set(True)
				self.tiebreakToWin = 10
		# Update the set number
		self.currentSet.set(currSet)

	def singular(self,word):
		"""
		Returns plural or singular form for word depending on singles or doubles match. Not an intelligent pluralization.
		@type word: string
		@param word: Word to be returned, singular or plural.
		@rtype: string
		@return: Plural or singular form for word depending on singles or doubles match. Not an intelligent pluralization.
		"""
		# This is crude. It works for the words that I am using. Probably could be more sophisticated. Later version.
		if self.doublesMatch.get():
			return word
		else:
			return word+'s'

def leader(score):
	"""
	Returns which team is winning.
	@type score: list of integers
	@param score: The current (game, set, or match) score as a list of two integers.
	@rtype: integer
	@return: Which team is winning. Returns -1 if score is tied.
	"""
	if score[0] > score[1]:
		# First team (0) is winning
		return 0
	elif score[1] > score[0]:
		# Second team (1) is winning
		return 1
	else:
		# Tied
		return -1

def scoreDelta(score):
	"""
	Returns the absolute value of the difference in the score.
	@type score: list of integers
	@param score: The score as a list of two integers.
	@rtype: integer
	@return: The absolute value of the difference in the score.
	"""
	return abs(score[0]-score[1])