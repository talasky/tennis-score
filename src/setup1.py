#!/usr/bin/python

"""
setup1.py

Copyright 2014, Ty A. Lasky

Released under the GNU General Public License 3.0

See LICENSE.txt for license information.

---------------------------------------------------

First setup dialog. Just whether singles or doubles.

Exported classes:

Setup1 -- First setup dialog. Just whether singles or doubles.
"""
py = 2
try:
	import Tkinter as tk
except:
	import tkinter as tk
	py = 3

import sys
sys.path.append('../lib')
import util

width1 = 18

class Setup1(tk.Toplevel):
	"""First setup dialog. Just whether singles or doubles."""
	def __init__(self, master):
		"""
		@type master: Toplevel widget
		@param master: Main application window.
		"""
		tk.Toplevel.__init__(self, master)
		self.overrideredirect(1) # No window decorations, no way to close window
		self.geometry('+100+100')
		self.doublesMatch = tk.BooleanVar()
		self.doublesMatch.set(0)
		tk.Radiobutton(self, indicatoron = 0, text="Singles", padx = 20, variable = self.doublesMatch,
			value = False, width = width1, anchor='center').pack()
		tk.Radiobutton(self, indicatoron = 0, text="Doubles", padx = 20, variable = self.doublesMatch,
			value = True, width = width1, anchor='center').pack()
		self.nextButton = tk.Button(self, text='Next', width=8)
		self.nextButton.pack(side='left')
		self.title("Match Info #1") # Won't have any effect, given no decorations
		util.center(self)

	def getDoublesMatch(self):
		"""
		Returns whether this is a doubles match.
		@rtype: boolean
		@return: Flag, True if this is a doubles match.
		"""
		return self.doublesMatch.get()