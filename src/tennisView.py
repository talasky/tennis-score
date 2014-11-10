#!/usr/bin/python

"""
tennisView.py

Copyright 2014, Ty A. Lasky

Released under the GNU General Public License 3.0

See LICENSE.txt for license information.

---------------------------------------------------

Provides the scoreboard view for tennis scoreboard based on MVC architecture.

Exported classes:

View -- The scoreboard for a tennis match.
"""

py = 2
try:
	import Tkinter as tk
except:
	import tkinter as tk
	py = 3

try:
	import ImageTk, Image
	pilAvailable = True
except:
	print("""\n\nNeed to install python-imaging and python-imaging-tk
to support JPEG player images.

Note that as of October 2014, PIL (Python Imaging Library) is not available
for Python 3.\n""")
	pilAvailable = False

# For downloading and displaying flags and pictures:
import urllib
if py == 3:
	import urllib.request
import base64
if py == 2:
	from StringIO import StringIO

import sys
sys.path.append('../lib')
import util

DEBUG = False

# Start of URL address for player photos
baseImageName = "http://tylasky.com/res/tennisScore/pics/"
imageSuffix = ".jpg"

# Used to convert integer (0, 1, 2, 3, 4) into normal tennis score representation
scoreRep = ("0", "15", "30", "40", "AD")

# See http://www.tutorialspoint.com/python/tk_fonts.htm for info on tkInter fonts
fontFace = "Helvetica"
fontSize = "24"
fontMod = "bold"
smallFontSize = "20"
msgFontSize = '16'
myFont = (fontFace, fontSize, fontMod)

# Define columns, widths, and spans for layout:
firstFlagCol = 0
rankCol = 2
nameCol = 3
serverCol = 4
firstSetCol = 5
messageCol = 0
messageSpan = 5
# Longest case is championship game, with Zahlavova Strycova, Barbora and Pavlyuchenkova, Anastasia, as of 10/2014.
messageWidth = 83
nameWidth = 33
rankWidth = 5
serverWidth = 5
setWidth = 5
gameWidth = 5
rankCol = 2
rankwidth = 5
buttonCol = 5
xLoc = '10'
yLoc = '175'

# Colors:
normalMsgForeground = 'black'
normalMsgBackground = 'white'
gameTypeMsgForeground = 'white'
gameTypeMsgBackground = 'blue'
tiebreakMsgForeground = 'white'
tieBreakMsgBackground = 'red'
championshipMsgForeground = 'black'
championshipMsgBackground = 'white'
mainForeground = 'white'
mainBackground = 'black'
currentSetForeground = 'white'
currentSetBackground = 'blue'
normalGameScoreForeground = 'black'
normalGameScoreBackground = 'white'
tiebreakScoreForeground = 'white'
tiebreakScoreBackground = 'red'

# Start of URL for flag images
flagPrefix = "http://www.33ff.com/flags/S_flags/flags_of_"
flagSuffix = ".gif"
flagWidth = 4

# File with three-letter IOC code, country name, and country flag string
countryUrl = 'http://tylasky.com/res/tennisScore/countries.txt'

class View(tk.Toplevel):
	"""The scoreboard for a tennis match."""
	def __init__(self, master):
		"""
		@type master: Toplevel widget
		@param master: Main application window.
		"""
		tk.Toplevel.__init__(self, master, bg=mainBackground)
		self.protocol('WM_DELETE_WINDOW', self.master.destroy) # should probably be self.exit
		self.overrideredirect(1) # No window decorations, no normal way to close window (added below)
		self.geometry('+'+xLoc+'+'+yLoc)
		# Messages
		self.messageCtrl = tk.Label(self, width = messageWidth,
			bg=normalMsgBackground, fg=normalMsgForeground, justify='center')
		self.messageCtrl.config(font=(fontFace, msgFontSize, fontMod))
		self.messageCtrl.grid(row=0,column=messageCol,columnspan=messageSpan)
		# Player / Team names
		# First team / player
		self.team1Ctrl = tk.Label(self, width = nameWidth, bg=mainBackground, fg=mainForeground, anchor='w')
		self.team1Ctrl.config(font=myFont)
		self.team1Ctrl.grid(row=1, column=nameCol, sticky='W')
		# Second team / player
		self.team2Ctrl = tk.Label(self, width = nameWidth, bg=mainBackground, fg=mainForeground, anchor='w')
		self.team2Ctrl.config(font=myFont)
		self.team2Ctrl.grid(row=2, column=nameCol, sticky='W')
		# Who is serving
		self.team1Serve = tk.Label(self, width = serverWidth, bg=mainBackground, fg=mainForeground, justify='center')
		self.team1Serve.config(font=myFont)
		self.team1Serve.grid(row=1, column=serverCol)
		self.team2Serve = tk.Label(self, width = serverWidth, bg=mainBackground, fg=mainForeground, justify='center')
		self.team2Serve.config(font=myFont)
		self.team2Serve.grid(row=2, column=serverCol)
		# Game score
		self.gameScoreTeam1 = tk.Label(self, width=gameWidth,
			bg=normalGameScoreBackground, fg=normalGameScoreForeground, justify='center')
		self.gameScoreTeam1.config(font=myFont)
		self.gameScoreTeam1.grid(row=1, column=firstSetCol+1)
		self.gameScoreTeam2 = tk.Label(self, width=gameWidth,
			bg=normalGameScoreBackground, fg=normalGameScoreForeground, justify='center')
		self.gameScoreTeam2.config(font=myFont)
		self.gameScoreTeam2.grid(row=2, column=firstSetCol+1)
		# Are we currently in a tiebreak?
		self.tiebreak = False
		self.currentSet = 0
		# Set scores
		self.team1SetCtrl = []
		self.team2SetCtrl = []
		# Flag labels for flags based on player countries:
		self.flag1 = tk.Label(self) # First team, player 1
		self.flag1a = tk.Label(self) # First team, player 2
		self.flag2 = tk.Label(self) # Second team, player 1
		self.flag2a = tk.Label(self) # Second team, player 2
		self.flagImages = []	# Will just be used to keep a reference to flag images (so not garbage collected)
		self.playerImages = []	# Will just be used to keep a reference to player images (so not garbage collected)
		# Team ranking labels
		self.rank1 = tk.Label(self, width=rankWidth,
			bg=mainBackground, fg=mainForeground, justify='center', font=myFont)
		self.rank2 = tk.Label(self, width=rankWidth,
			bg=mainBackground, fg=mainForeground, justify='center', font=myFont)
		self.rank1.grid(row=1, column=rankCol)
		self.rank2.grid(row=2, column=rankCol)
		# Button for exiting the program
		btnGroup = tk.LabelFrame(self, bg=mainBackground, fg=mainForeground)
		# may want to move this around for different sets. Or, put it before message control
		# As of right now, I like it showing above first set score, and staying there.
		btnGroup.grid(row=0, column=buttonCol, padx=10, pady=10)
		self.exitButton = tk.Button(btnGroup, text=u'\u2716', bg=mainBackground, fg=mainForeground)
		# Not 100% happy with this symbol. Seems it should be wider.
		# For now, removing minimize button. It doesn't work in combination with overrideredirect
		#self.minimizeButton = tk.Button(btnGroup, text=u'\u02cd', bg=mainBackground, fg=mainForeground)
		self.exitButton.config(command=lambda: self.exit()) # quit application
		#self.minimizeButton.config(command=lambda: self.wm_state('iconic')) # minimize scoreboard
		#self.minimizeButton.grid(row=0, column=0, sticky='E')
		self.exitButton.grid(row=0, column=1, sticky='E')
		self.title("Scoreboard") #no effect with overrideredirect
		util.center(self)
		self.readCountries()

	def exit(self):
		"""Do any image window close, file close, image close, etc., and exit."""
		# So far, seems nothing to close / clean up.
		sys.exit(0)

	def readCountries(self):
		"""Read in IOC country codes (key) from URL, and set corresponding country and flag name (values)."""
		# Read in the country information as a string fro the URL
		txt = util.getUrlAsString(countryUrl)
		if not txt is None: # String read from URL
			self.countries = {}
			for line in util.lineIter(txt): # Parse each line, key = IOC code, value = tuple of country name, flag file name prefix.
				line = util.decode(line) # Handle unicode
				strings = line.split(",")
				key = strings[0]
				val = (strings[1], strings[2].strip())
				self.countries[key] = val
		else: # Error in reading string from URL
			# Is there something better to do than exit? Later version.
			print("readCountries: Couldn't open {}, exiting.".format(countryUrl))
			sys.exit(1)

	def setTeamMembers(self, team1String, team2String):
		"""
		Sets the team member strings for the match.
		@type team1String: string
		@param team1String: Name(s) for first team.
		@type team2String: string
		@param team2String: Name(s) for second team.
		"""
		self.team1Ctrl.config(text = team1String)
		self.team2Ctrl.config(text = team2String)

	def setTeam(self,team):
		"""
		Sets the two team objects for the match. Also sets ranks and flags for teams.
		@type team: list of Teams
		@param team: The list of Team objects for the match.
		"""
		self.team = team
		self.setFlags() # Set the flags based on the current team players' countries
		self.setRank() # Set rank strings based on current team players

	def setRank(self):
		"""Sets the rank text for each team."""
		self.rank1.config(text=self.team[0].getRank())
		self.rank2.config(text=self.team[1].getRank())
		self.rank1.grid(row=1, column=rankCol)
		self.rank2.grid(row=2, column=rankCol)

	def setFlags(self):
		"""Sets the flags for each team member's country."""
		util.dbgprint(DEBUG, "For team 1, flags will be for: {}".format(self.team[0].getCountryCode()))
		util.dbgprint(DEBUG, "For team 2, flags will be for: {}".format(self.team[1].getCountryCode()))
		# Set flag for first team, player 1
		self.setOneFlag(self.flag1, self.team[0].getCountryCode()[0], 1, firstFlagCol)
		#
		# following is test code to see how handle non-exstent country code (comment out prior line):
		# self.setOneFlag(self.flag1, 'XYZ', 1, firstFlagCol)
		#
		if len(self.team[0].getCountryCode()) == 2: # Two players on first team
			# Set flag for first team, player 2
			self.setOneFlag(self.flag1a, self.team[0].getCountryCode()[1], 1, firstFlagCol+1)
		# Set flag for second team, player 1
		self.setOneFlag(self.flag2, self.team[1].getCountryCode()[0], 2, firstFlagCol)
		if len(self.team[1].getCountryCode()) == 2: # Two players on second team
			# Set flag for second team, player 2
			self.setOneFlag(self.flag2a, self.team[1].getCountryCode()[1], 2, firstFlagCol+1)

	def setOneFlag(self, label, countryCode, row, column):
		"""
		Obtains a flag image and configures a label with it. Grids the label.
		@type label: tkl.Label
		@param label: Label to configure with flag image.
		@type countryCode: string
		@param countryCode: Three-letter IOC code for country.
		@type row: integer
		@param row: Row for label placement
		@type column: integer
		@param column: Column for label placement
		"""
		# configures label with flag image from URL indicated by three-letter IOC country code
		try:
			img = self.getFlagImage(countryCode)
		except tk.TclError: # Error in getting the flag image
			print("Tcl image error, defaulting to country code.")
			img = None
		if img != None:
			# Next line is essential, have to keep a ref to image, or it will be garbage-collected.
			self.flagImages.append(img)
			label.config(image=img) # Set the label's image to the flag image
		else:
			# Problem getting flag image, just use three-letter IOC code text
			label.config(text=countryCode, font = myFont, bg=mainBackground, fg=mainForeground)
		label.grid(row=row, column=column)

	def getFlagImage(self, countryCode):
		"""
		Returns a base 64 encoded image of a flag from URL indicated by countryCode.
		@type countryCode: string
		@param countryCode: Three-letter IOC code for country.
		@rtype: tk.PhotoImage (unless some error, then None)
		@return: A base 64 encoded image of a flag from URL indicated by countryCode. If error, None.
		"""
		# returns a base 64 encoded image of a flag from URL indicated by countryCode
# http://stackoverflow.com/questions/6086262/python-3-how-to-retrieve-an-image-from-the-web-and-display-in-a-gui-using-tkint
		if countryCode in self.countries:
			flagString = flagPrefix + self.countries[countryCode][1] + flagSuffix
		else: # No such country code
			print("Error: Could not find country code: %s" % countryCode)
			return None
		if countryCode == 'TPE': # This flag is not available on http://www.33ff.com. Found it elsewhere, scaled, placed in my resources
			# Flag for Chinese Taipei / Taiwan:
			flagString = 'http://tylasky.com/res/tennisScore/Chinese-Taipei.gif'
		util.dbgprint(DEBUG, "getFlagImage: "+flagString)
		# following is test code to see how handle no resource on server:
		#
		# flagString = flagPrefix
		#
		# following is test code to see how handle bad server:
		#
		# flagString = 'http://xyz.badsite.dbg'
		#
		try:
			if py == 2:
				u = urllib.urlopen(flagString)
			else: # Python 3
				u = urllib.request.urlopen(flagString)
		except IOError:
			print("getFlagImage: Could not locate server {}".format(flagString))
			u.close()
			return None
		if u.getcode() != 200:
			print("getFlagImage: Resource not found on server {} : code = {}".format(flagString,u.getcode()))
			u.close()
			return None
		# Successful, finish up
		rawData = u.read() # Any error to check here?
		u.close()
		return tk.PhotoImage(data=base64.encodestring(rawData))

	def showWinnerPhotos(self, winner):
		"""
		Shows photo(s) of the match winner(s).
		@type winner: integer
		@param winner: Number of the winning team.
		"""
		if not pilAvailable: # Can't show JPEG images
			return
		img1 = getPlayerPhoto(self.team[winner].playerA) # Get photo for winning team, first player
		img2 = getPlayerPhoto(self.team[winner].playerB) # Get photo for winning team, second player
		if (img1 is None) and (img2 is None): # No photos for some reason
			return
		photoWin = tk.Toplevel() # Create a window for photo(s)
		if img1 != None: # Show first player's photo
			# Next line is essential, have to keep a ref to image, or it will be garbage-collected.
			self.playerImages.append(img1)
			label1 = tk.Label(photoWin, image = img1, bg='black')
			label1.grid(row=0, column=0, padx=10, pady=10)
		if img2 != None: # Show second player's photo
			# Next line is essential, have to keep a ref to image, or it will be garbage-collected.
			self.playerImages.append(img2)
			label2 = tk.Label(photoWin, image = img2, bg='black')
			label2.grid(row=0, column=1, padx=10, pady=10)
		photoWin.overrideredirect(1) # No window decorations, no normal way to close window (added below)
		(x,y) = util.centerCoords(photoWin)
		util.positionWindow(photoWin, x, y-300)		

	def setServer(self,server):
		"""
		Updates the scoreboard indicator for the current server.
		@type server: integer
		@param server: Number of the current server.
		"""
		# Set the server indicator. Here, using unicode for a left-facing elongated triangle
		if (server==0):
			self.team1Serve.config(text=u'\u25c5')
			self.team2Serve.config(text = '')
		elif (server==1):
			self.team1Serve.config(text = '')
			self.team2Serve.config(text=u'\u25c5')

	def setMessage(self,message):
		"""
		Sets the scoreboard message.
		@type message: string
		@param message: Message to be displayed by the scoreboard.
		"""
		(foreground,background) = getMessageColor(message)
		self.messageCtrl.config(bg=background,fg=foreground, text=message.upper())

	def setGameScore(self,score):
		"""
		Sets the current game score. Handles deuce and ad situations. Converts score (0,1,2,3,..) into (0, 15, 30, 40,...)
		@type score: list of integers
		@param score: Current game score.
		"""
		(foreground,background) = self.getScoreColor()
		self.gameScoreTeam1.config(fg=foreground,bg=background)
		self.gameScoreTeam2.config(fg=foreground,bg=background)
		if (self.tiebreak):
			# Here, no representation conversion. Displayed score same as numerical score.
			self.gameScoreTeam1.config(text = str(score[0]))
			self.gameScoreTeam2.config(text = str(score[1]))
		else:
			# Here, there is representation conversion.
			if((score[0] < len(scoreRep)) and (score[1] < len(scoreRep))): #Make sure we don't index outside of scoreRep tuple
				self.gameScoreTeam1.config(text = scoreRep[score[0]])
				self.gameScoreTeam2.config(text = scoreRep[score[1]])
				if score[0] == 4:
					self.gameScoreTeam2.config(text = "-") # It is an AD game, first team is ahead
				if score[1] == 4:
					self.gameScoreTeam1.config(text = "-") # It is an AD game, second team is ahead
			else: # One of the scores is greater than the length of scoreRep. This should NEVER happen.
				print("Serious error condition. Score of %d, %d is too big for score representation."%(score[0], score[1]))
				self.gameScoreTeam1.config(text = "Err")
				self.gameScoreTeam2.config(text = "Err")
		if (score[0]+score[1]) == 0: # At start of a game, don't show the score boxes.
			self.gameScoreTeam1.grid_remove()
			self.gameScoreTeam2.grid_remove()
		else:
			self.gameScoreTeam1.grid() # In middle of game, show score boxes.
			self.gameScoreTeam2.grid()
			# Note, following really only needed once, but doesn't hurt to do every time:
			self.team1SetCtrl[self.currentSet].grid()
			self.team2SetCtrl[self.currentSet].grid()

	def setTiebreak(self,tiebreak):
		"""
		Sets whether  currently in a tiebreak.
		@type tiebreak: boolean
		@param tiebreak: Flag, True if in a tiebreak.
		"""
		self.tiebreak = tiebreak

	def addSetCtrl(self, set):
		"""
		Adds scoreboard controls for new set. Hides them at beginning of set.
		@type set: integer
		@param set: Number of set (0 = first set)
		"""
		t1set = tk.Label(self, width=setWidth, bg=mainBackground, fg=mainForeground, justify='center')
		t1set.config(font=myFont,text="0")
		t1set.grid(row=1, column = set + firstSetCol)
		# Add to the list of set controls
		self.team1SetCtrl.append(t1set)
		t2set = tk.Label(self, width=setWidth, bg=mainBackground, fg=mainForeground, justify='center')
		t2set.config(font=myFont,text="0")
		t2set.grid(row=2, column = set + firstSetCol)
		# Add to the list of set controls
		self.team2SetCtrl.append(t2set)
		# Hide control for now:
		t1set.grid_remove()
		t2set.grid_remove()

	def setSet(self,currentSet):
		"""
		Starts a new set. Hides game score at beginning of set.
		@type currentSet: integer.
		@param currentSet: Number of the current set (0 = first set)
		"""
		self.currentSet = currentSet
		# Create controls and add them to the list of set controls.
		self.addSetCtrl(currentSet)
		for i in range(currentSet+1):
			(foreground,background) = self.getSetColor(i)
			self.team1SetCtrl[i].config(fg=foreground,bg=background)
			self.team2SetCtrl[i].config(fg=foreground,bg=background)
		# Move the game score one spot to the right to accomodate the new set score boxes.
		self.gameScoreTeam1.grid(row=1, column=currentSet+firstSetCol+1)
		self.gameScoreTeam2.grid(row=2, column=currentSet+firstSetCol+1)
		# Hide score for now
		self.gameScoreTeam1.grid_remove()
		self.gameScoreTeam2.grid_remove()

	def setSetScore(self,score):
		"""
		Updates the set scores.
		@type score: list of lists of integers
		@param score: List of set scores up to and including current set.
		"""
		for i in range(self.currentSet + 1):
			self.team1SetCtrl[i].config(text = str(score[i][0]))
			self.team2SetCtrl[i].config(text = str(score[i][1]))

	def setSetColorsSame(self):
		"""Sets the set control foreground and background colors the same as the main colors."""
		for i in range(self.currentSet + 1):
			self.team1SetCtrl[i].config(bg = mainBackground, fg = mainForeground)
			self.team2SetCtrl[i].config(bg = mainBackground, fg = mainForeground)

	def getScoreColor(self):
		"""
		Gets the game score colors depending on whether a normal game or a tiebreak.
		@rtype: tuple of colors
		@return: Foreground and background color as a tuple.
		"""
		if self.tiebreak:
			fg = tiebreakScoreForeground
			bg = tiebreakScoreBackground
		else:
			fg = normalGameScoreForeground
			bg = normalGameScoreBackground
		return fg,bg

	def getSetColor(self,set):
		"""
		Gets the set score color depending on whether it is the current or a previous set.
		@rtype: tuple of colors
		@return: Foreground and background color as a tuple.
		"""
		if self.currentSet == set:
			fg = currentSetForeground
			bg = currentSetBackground
		else:
			fg = mainForeground
			bg = mainBackground
		return fg,bg

def getMessageColor(message):
	"""Gets the message color scheme depending on the type of message."""
	if message.lower() == "tiebreak":
		# Tiebreak
		fg = tiebreakMsgForeground
		bg = tieBreakMsgBackground
	elif message.lower() in {"round 1", "round 2", "round 3", "round 4",
							"round of 16", "quarterfinal", "semifinal", "championship"}:
		# Message is the match type
		fg = gameTypeMsgForeground
		bg = gameTypeMsgBackground
	elif "championship point" in message.lower():
		# Championship point
		fg = championshipMsgForeground
		bg = championshipMsgBackground
	else:
		# Regular message
		fg = normalMsgForeground
		bg = normalMsgBackground
	return fg,bg

def getPlayerPhoto(player):
	"""
	Returns the photo for a Player.
	@type player: Player
	@param player: The Player to get the photo for.
	@rtype: tk.PhotoImage (unless some error, then None)
	@return: Photo of Player.
	"""
	# returns photo for player
	if player is None:
		return None
	# Form JPEG file name. Substitute spaces in last name with "_":
	jpgFileName = (player.firstName[0:2]+"_"+player.lastName.replace(" ", "_")+imageSuffix).lower()
	img = getUrlPhoto(baseImageName + jpgFileName)
	return img

def getUrlPhoto(jpgUrl):
	"""
	Gets a photo for the given JPEG URL.
	@type jpgUrl: string
	@param jpgUrl: URL for a desired JPEG.
	@rtype: ImageTk.PhotoImage (unless some error, then None)
	@return: Photo corresponding to JPEG URL (unless some error, then None)
	"""
	# returns a PhotoImage for the JPEG file at jpgUrl
	#
	# following is test code to see how handle no resource on server:
	#
	# jpgUrl = jpgUrl+"xjlxkldx"
	#
	# following is test code to see how handle bad server:
	#
	# jpgUrl = 'http://xyz.badsite.dbg'
	#
	if pilAvailable:
		try:
			if py == 2:
				u = urllib.urlopen(jpgUrl)
			else:
				u = urllib.request.urlopen(jpgUrl)
		except IOError:
			print("getPhoto: Could not locate server {}".format(jpgUrl))
			u.close()
			return None
		if u.getcode() != 200:
			print("getPhoto: Resource not found on server {} : code = {}".format(jpgUrl,u.getcode()))
			u.close()
			return None
		rawData = u.read() # Any error check here?
		u.close()
		if py == 3:
			img = Image.open(io.StringIO(rawData))
		else: # Python 2
			img = Image.open(StringIO(rawData))
		return ImageTk.PhotoImage(img)
	else:
		# Can't show JPEG images without PIL
		return None

if __name__ == '__main__':
	# Test flag routine.
	master = tk.Tk()
	myView = View(master)
	country = 'Australia'
	url = flagPrefix + country + flagSuffix
	if py == 2:
		u = urllib.urlopen(url)
	else:
		u = urllib.request.urlopen(url)
	rawData = u.read()
	u.close()

	b64Data = base64.encodestring(rawData)
	image = tk.PhotoImage(data=b64Data)

	label = tk.Label()
	label.config(image=image)
	label.pack()
	img = myView.getFlagImage('CHN')
	myView.flag1.config(image=img)
	myView.flag1.grid(row=1, column=firstFlagCol)
	master.mainloop()