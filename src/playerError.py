#!/usr/bin/python
"""
playerError.py

Copyright 2014, Ty A. Lasky

Released under the GNU General Public License 3.0

See LICENSE.txt for license information.

---------------------------------------------------

Player error dialog.

Exported classes:

PlayerError -- Provides an error message for duplicate players.
"""

fontFace = "Helvetica"
fontSize = "18"
fontMod = "bold"
myFont = (fontFace, fontSize, fontMod)

py = 2
try:
	import Tkinter as tk
except:
	import tkinter as tk
	py = 3

class PlayerError(tk.Toplevel):
	"""Provides an error message for duplicate players."""
	# Perhaps there could be other errors for players. Can't think of any now. Handle in later version if needed.
	def __init__(self, master):
		"""
		@type master: Toplevel widget
		@param master: Main application window.
		"""
		tk.Toplevel.__init__(self, master)
		tk.Label(self,text = "All players must be distinct.\nTry again.", font=myFont).pack()
		self.okButton = tk.Button(self, text='OK', width=8)
		self.okButton.pack()
		self.title("Player Error")