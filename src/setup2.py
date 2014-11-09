#!/usr/bin/python

"""
setup2.py
*****************************************************
* Copyright 2014, Ty A. Lasky                       *
* Released under the GNU General Public License 3.0 *
* See LICENSE.txt for license information.          *
*****************************************************

Second setup dialog. Gets further setup information for match.
Based on MVC architecture.

Exported classes:

Setup2 -- Second setup dialog. Gets further setup information for match.
"""
import util
py = 2
try:
	import Tkinter as tk
except:
	import tkinter as tk
	py = 3

mtypeList = ["Round 1", "Round 2", "Round 3", "Round 4",
			"Round of 16", "Quarterfinal", "Semifinal", "Championship"]
width1 = 21

class Setup2(tk.Toplevel):

	def __init__(self, master, singles):
		"""
		Second setup dialog. Gets further setup information for match.
		@type master: Toplevel widget
		@param master: Main application window.
		@type singles: boolean
		@param singles: Flag, True if this is a singles match.
		"""
		tk.Toplevel.__init__(self, master)
		self.overrideredirect(1) # No window decorations, no way to close window
		self.geometry('+100+100')
		self.noEndingTiebreak = tk.BooleanVar()
		self.noEndingTiebreak.set(False)
		self.mensMatch = tk.IntVar()
		self.mensMatch.set(0)
		self.matchType = tk.StringVar(self)
		self.matchType.set(mtypeList[4]) # default value
		tk.Radiobutton(self, indicatoron = 0, text="Women's match", padx = 20,
			width=width1 , variable = self.mensMatch, value = 0, anchor='center').pack()
		tk.Radiobutton(self, indicatoron = 0, text="Men's match", padx = 20,
			width=width1, variable = self.mensMatch, value = 1, anchor='center').pack()
		if not singles:	# Doubles match
			tk.Radiobutton(self, indicatoron = 0, text="Mixed doubles", padx = 20,
				width=width1, variable = self.mensMatch, value = 2, anchor='center').pack()
		self.noEndingTiebreakBox = tk.Checkbutton(self, variable=self.noEndingTiebreak,
			onvalue=True, offvalue=False, text="No ending tiebreaker").pack()
		tk.Label(self, text='Match Type:').pack(side='left')
		w = tk.OptionMenu(self, self.matchType, *mtypeList)
		w.config(bg='black',fg='white')
		w["menu"].config(bg='black',fg='white')
		w.pack()
		self.nextButton = tk.Button(self, text='Next', width=8)
		self.nextButton.pack(side='left')
		self.title("Match Info #2") # Won't have any effect, given no decorations
		util.center(self)

	def getNoEndingTiebreak(self):
		"""
		Returns whether the match can finish final set with a tiebreak.
		@rtype: boolean
		@return: Flag, True if match cannot finish final set with a tiebreak.
		"""
		return bool(self.noEndingTiebreak.get())

	def getMensMatch(self):
		"""
		Returns the value of "Men's Match".
		@rtype: int
		@return: Value of "Men's Match": 0 = women's, 1 = men's, 2 = mixed.
		"""
		return self.mensMatch.get()

	def getMatchType(self):
		"""
		Returns the type of match.
		@rtype: string
		@return: Type of match, e.g. quarterfinal, semifinal, etc.
		"""
		return self.matchTypeEntry.get()