#!/usr/bin/python

"""
scoring.py
*****************************************************
* Copyright 2014, Ty A. Lasky                       *
* Released under the GNU General Public License 3.0 *
* See LICENSE.txt for license information.          *
*****************************************************

The scoring controls for tennis scoreboard based on MVC architecture.

Exported classes:

Scoring -- A simple window providing scoring buttons for two tennis teams (players)
"""
import util
py = 2
try:
	import Tkinter as tk
except:
	import tkinter as tk
	py = 3

score1Color = 'blue'
score2Color = 'red'
# These are just hand-tuned. Better if could base off of the final scoreboard position.
horizOffset = 565
vertOffset = 135

class Scoring(tk.Toplevel):
	"""A simple window providing scoring buttons for two tennis teams (players)"""

	def __init__(self, master,team1,team2,doubles):
		"""
		@type  master: tk.Toplevel
		@param master: The main application window.
		@type  team1:  string
		@param team1:  The first team (or player) in the match.
		@type  team2:  string
		@param team2:  The second team (or player) in the match.
		@type doubles: boolean
		@param doubles: Flag, True if this is a doubles match.
		"""
		# Word for which team scores, depends on singles vs. double match
		s = "\nscore" if doubles else "\nscores"
		tk.Toplevel.__init__(self, master, width=250,height=100)
		self.overrideredirect(1) # No window decorations, no way to close window
		self.geometry('+100+100')
		self.team1Button = tk.Button(self, text=team1+s, width=25, height = 3)
		self.team1Button.config(bg=score1Color,fg='white')
		self.team1Button.pack(side='left')
		self.team2Button = tk.Button(self, text=team2+s, width=25, height = 3)
		self.team2Button.config(bg=score2Color,fg='white')
		self.team2Button.pack(side='left')
		self.title("Scoring") # Won't have any effect, given no decorations
		(x,y) = util.centerCoords(self)
		util.positionWindow(self, x-horizOffset, y-vertOffset)