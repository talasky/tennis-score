#!/usr/bin/python

"""
tennisScore.py
*****************************************************
* Copyright 2014, Ty A. Lasky                       *
* Released under the GNU General Public License 3.0 *
* See LICENSE.txt for license information.          *
*****************************************************

Main program (controller) for tennis scoreboard based on model, view, controller architecture.

Exported classes:

Controller -- The conntroller for a tennis scoreboard program.
"""

py = 2
try:
	import Tkinter as tk
except:
	import tkinter as tk
	py = 3
from tennisModel import Model
from tennisView import View
from setup1 import Setup1
from setup2 import Setup2
from setup3 import Setup3
from playerError import PlayerError
from scoring import Scoring
from random import randrange
import player
import util

DEBUG = False

# Might want to determine special cases from the list of players, automatically. Later version.
specialCaseNames = [('Pliskova','K')] # Karolina and Kristyna

class Controller:
	"""The conntroller for a tennis scoreboard program."""
	def __init__(self, root):
		"""
		@type root: Toplevel widget
		@param root: Main application window.
		"""
		self.model = Model()
		# Add needed callbacks for observable fields in Model
		self.model.gameScore.addCallback(self.gameScoreChanged)
		self.model.setScore.addCallback(self.setScoreChanged)
		self.model.message.addCallback(self.messageChanged)
		self.model.server.addCallback(self.serverChanged)
		self.model.winner.addCallback(self.winnerNamed)
		self.model.tiebreak.addCallback(self.tiebreakChanged)
		self.model.currentSet.addCallback(self.setChanged)
		self.model.team.addCallback(self.teamChanged)
		# Presents first setup dialog (just whether singles or doubles match)
		self.viewSetup1 = Setup1(root)
		self.viewSetup1.nextButton.config(command=self.singles)

	def initTennisView(self):
		"""Initializes the scoreboard in the View class."""
		util.dbgprint(DEBUG,"initTennisView:")
		self.teamChanged(self.model.team)  # set the initial value of the tams in the view
		self.setChanged(self.model.currentSet.get())  # set the initial value of the set # in the view
		self.messageChanged(self.model.message.get())  # set the initial value of the message in the view
		self.serverChanged(self.model.server.get())  # set the initial value of the server in the view
		self.winnerNamed(self.model.winner.get())  # set the initial value of the winner in the view

	def gameScoreChanged(self,gameScore):
		"""
		Updates the game score in scoreboard.
		@type gameScore: list of integers
		@param gameScore: The current game score.
		"""
		self.scoreboard.setGameScore(gameScore)

	def setChanged(self,currentSet):
		"""
		Updates the set number for scoreboard.
		@type currentSet: integer
		@param currentSet: The current set (0 = first set).
		"""
		self.scoreboard.setSet(currentSet)
		
	def setScoreChanged(self, setScore):
		"""
		Updates the set score in scoreboard.
		@type setScore: list of integers
		@param setScore: The current set score.
		"""
		self.scoreboard.setSetScore(setScore)

	def messageChanged(self, message):
		"""
		Updates the message to be displayed on the scoreboard.
		@type message: string
		@param currentSet: The message to be displayed on the scoreboard.
		"""
		self.scoreboard.setMessage(message)

	def serverChanged(self, server):
		"""
		Updates which team / player is serving.
		@type server: integer
		@param server: The number of the team / player now serving.
		"""
		self.scoreboard.setServer(server)

	def teamChanged(self, team):
		"""
		Updates the Team objects and their scoreboard names.
		@type team: list of Team objects
		@param team: The Team objects for the current match.
		"""
		# Set the Team objects in the view
		self.scoreboard.setTeam(team)
		# Set the score names for the teams in the view
		self.scoreboard.setTeamMembers(
			self.model.team[0].scoreName(dups=self.model.duplicateLastName,	special=self.model.specialCaseNames),
			self.model.team[1].scoreName(dups=self.model.duplicateLastName, special=self.model.specialCaseNames))
		self.model.teamScoreNames = [
			self.model.team[0].scoreName(dups=self.model.duplicateLastName,	special=self.model.specialCaseNames),
			self.model.team[1].scoreName(dups=self.model.duplicateLastName, special=self.model.specialCaseNames)]

	def winnerNamed(self,winner):
		"""
		Sets the winning team for the current match. Shows message, and photo(s).
		@type winner: integer
		@param winner: The number of the winning team / player.
		"""
		if (winner >= 0): # winner < 0 means no winner yet
			util.dbgprint(DEBUG, "In controller, winnerNamed.")
			self.scoreboard.setMessage(self.model.teamScoreNames[winner]+" won!")
			# Show the winner photo(s) if available
			self.scoreboard.showWinnerPhotos(winner)
			self.scoreboard.setSetColorsSame()

	def tiebreakChanged(self,tiebreak):
		"""
		Updates whether currently in a tiebreak.
		@type tiebreak: boolean
		@param tiebreak: Flag, True if currently in a tiebreak.
		"""
		self.scoreboard.setTiebreak(tiebreak)

	def incrementGameScore(self, team):
		"""
		Increments the current game score by one for the scoring team.
		@type team: integer
		@param team: The scoring team.
		"""
		self.model.incrementGameScore(team)

	def singles(self): # Check for singles or doubles match
		"""Interprets first setup dialog. Determines whether the current match is singles or doubles. Also, presents next setup dialog."""
		self.model.doublesMatch.set(self.viewSetup1.getDoublesMatch())
		if DEBUG:
			if self.model.doublesMatch.get():
				print("Doubles")
			else:
				print("Singles")
		# Present next setup dialog, destroy current dialog
		self.viewSetup2 = Setup2(root, not self.model.doublesMatch.get())
		self.viewSetup2.nextButton.config(command=self.setup2)
		self.viewSetup1.destroy()

	def setup2(self):
		"""Interprets second setup dialog. Determines mens / womens / mixed match. Whether end on tiebreak. Also, presents next setup dialog."""
		self.model.mensMatch.set(self.viewSetup2.getMensMatch())
		if DEBUG:
			if self.model.mensMatch.get()==1:
				print("Men's")
			elif self.model.mensMatch.get() == 0:
				print("Women's")
			else:
				print("Mixed doubles")
		self.model.noEndingTiebreak.set(self.viewSetup2.getNoEndingTiebreak())
		util.dbgprint(DEBUG, "No ending tiebreak is "+str(self.model.noEndingTiebreak.get()))
		self.model.matchType.set(self.viewSetup2.matchType.get())
		util.dbgprint(DEBUG, "Match type is: "+self.model.matchType.get())
		# Present next setup dialog, destroy current dialog
		self.viewSetup3 = Setup3(root, self.model.mensMatch.get(), self.model.doublesMatch.get())
		self.viewSetup3.startButton.config(command = self.startMatch)
		self.viewSetup2.destroy()

	def reshowSetup3(self):
		"""Clears and reshows the third setup dialog."""
		# Not used. I just leave original dialog open until the user gets it right.
		self.viewSetup3.destroy()
		self.viewSetup3 = Setup3(root, self.model.mensMatch.get(), self.model.doublesMatch.get())
		self.viewSetup3.startButton.config(command = self.startMatch)

	def startMatch(self):
		"""Starts the match. Interprets third setup dialog. Player names, number of sets, ending tiebreak. Creates scoring buttons. Initializes scoreboard."""
		# Get the strings for the two team's player names. Each string includes all object properties in parseable format.
		teamStrings = self.viewSetup3.getTeamStrings()
		# Doing next earlier than I'd normally do, so capture change of teams.
		self.scoreboard = View(root)	# The main scoreboard
		if self.model.doublesMatch.get():
			props = parsePlayerString(teamStrings[0][0]) # Parse string for first team, player 1, extract properties
			player1 = player.Player(props[0],props[1],props[2],props[3])
			props = parsePlayerString(teamStrings[0][1]) # Parse string for first team, player 2, extract properties
			player1a = player.Player(props[0],props[1],props[2],props[3])
			props = parsePlayerString(teamStrings[1][0]) # Parse string for second team, player 1, extract properties
			player2 = player.Player(props[0],props[1],props[2],props[3])
			props = parsePlayerString(teamStrings[1][1]) # Parse string for second team, player 2, extract properties
			player2a = player.Player(props[0],props[1],props[2],props[3])
			playerList = [player1, player1a, player2, player2a] # List used to check for player uniqueness
			# Set teams in model
			self.model.team = [player.Team(player1, player1a), player.Team(player2, player2a)]
		else: # singles match
			props = parsePlayerString(teamStrings[0]) # Parse string for first player, extract properties
			player1 = player.Player(props[0],props[1],props[2],props[3])
			props = parsePlayerString(teamStrings[1]) # Parse string for second, extract properties
			player2 = player.Player(props[0],props[1],props[2],props[3])
			playerList = [player1, player2] # List used to check for player uniqueness
			# Set teams in model
			self.model.team = [player.Team(player1), player.Team(player2)]

		# Check for player uniqueness. If not, then re-show dialog.
		# Recall that when form a set from a list, any duplicate items will be discarded
		if not (len(playerList) == len(set(playerList))):
			# There are duplicates, so warn, and retry
			self.view4 = PlayerError(root)
			self.view4.okButton.config(command = self.view4.destroy)
			self.scoreboard.destroy()
			# Once drop out of view4 dialog, will be back at third setup dialog to allow user to correct error.
			return # Not sure this is necessary. Likely never gets here.

		self.model.duplicateLastName = self.viewSetup3.duplicateLastName # List of last names that appear mroe than once.
		self.model.specialCaseNames = specialCaseNames # List of special case names, same last name AND first initial.

		self.model.numberOfSets.set(self.viewSetup3.getNumberOfSets())
		# Following could be more general. It works for three and five set matches. Which is everthing, I think. Later version.
		if self.model.numberOfSets.get() == 3:
			self.model.winSets.set(2)
		else:
			self.model.winSets.set(3)
		if self.model.doublesMatch.get():
			self.model.winSets.set(2)

		if DEBUG:
			if self.model.noEndingTiebreak.get():
				print("This match cannot end set {} in a tiebreak.".format(self.model.numberOfSets.get()))
			else:
				print("This match can end set {} in a tiebreak.".format(self.model.numberOfSets.get()))

		util.dbgprint(DEBUG, str(self.model.winSets.get())+" sets to win match.")
		self.viewSetup3.destroy()
		# Establish the team scoring buttons.
		# Q: Should this be done in teamChanged? It works fine here, but may make more sense there.
		self.scoringView = Scoring(self.scoreboard,
				self.model.team[0].buttonName(self.model.duplicateLastName, self.model.specialCaseNames),
				self.model.team[1].buttonName(self.model.duplicateLastName, self.model.specialCaseNames),
				self.model.doublesMatch.get())   # The scoring buttons
		# Pick starting server at random
		self.model.server.set(randrange(2))
		self.scoringView.team1Button.config(command=lambda: self.incrementGameScore(0))   # Team 1 scores
		self.scoringView.team2Button.config(command=lambda: self.incrementGameScore(1))   # Team 2 scores
		if DEBUG:
			print("Before initTennisView(), self.model.team is {}".format(self.model.team))
		# Initialize scoreboard view, and we are off and running.
		self.initTennisView()

def parsePlayerString(s):
	"""
	Parses a string representing a player into elements of a Player object.
	@type s: string
	@param s: String representing a player.
	@rtype: tuple
	@return: Elements of a Player object.
	"""
	l1 = s.split('.')
	rank = l1[0]
	l2 = l1[1].split(',')
	lastName = l2[0].strip()
	l3 = l2[1].split('(')
	firstName = l3[0].strip()
	country = l3[1][0:3] # Three-letter IOC code for country.
	return (rank, firstName, lastName, country)

if __name__ == '__main__':
        root = tk.Tk()
        root.withdraw()   # removes widget from screen
        app = Controller(root)
        root.mainloop()