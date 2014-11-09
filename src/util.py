#!/usr/bin/python
"""
util.py
*****************************************************
* Copyright 2014, Ty A. Lasky                       *
* Released under the GNU General Public License 3.0 *
* See LICENSE.txt for license information.          *
*****************************************************

Utility routines for tennisScore.py.

"""

py = 2
try:
	import Tkinter as tk
except:
	import tkinter as tk
	py = 3
import urllib
if py == 3:
    import urllib.request

# centering routine from:
# http://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
# now split into center(), centerCoords(), and positionWindow()
def center(win):
    """
    Centers a window on the screen.
    @type win: Toplevel widget
    @param win: Window to be centered.
    """
    win.update_idletasks()
    win.attributes('-alpha', 0.0) # should hide the window move. Not working for me.
    (x,y) = centerCoords(win)
    positionWindow(win,x,y)

def centerCoords(win):
    """
    Returns x,y coordinates that would center a window.
    @type win: Toplevel widget
    @param win: Window to be centered.
    @rtype: tuple
    @return: Tuple of (x,y) coordinates to center the window.
    """
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width =  width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    return (x,y)

def positionWindow(win,x,y):
    """
    Positions a window at given coordinates.
    @type win: Toplevel widget
    @param win: Window to be centered.
    @type x: int
    @param x: x-coordinate for window position.
    @type y: int
    @param y: y-coordinate for window position.
    """
    # modified following line, can't specify width, height, as width is variable based on # of sets
    win.geometry('+{}+{}'.format(x, y))
    if win.attributes('-alpha') == 0:
        win.attributes('-alpha', 1.0)
    win.deiconify() # activates the window, which is likely not iconified.

def getUrlAsString(url):
    """
    Returns the contents of the given URL as a single string.
    @type url: string
    @param url: The URL to be converted to a string.
    @rtype: string
    @return: The contents of the URL as a string.
    """
    try:
        if py == 2:
            u = urllib.urlopen(url)
        else: # Python 3
            u = urllib.request.urlopen(url)
    except IOError:
        print("getUrlAsString: Could not locate server {}".format(url))
        u.close()
        return None
    if u.getcode() != 200:
        print("getUrlAsString: Resource not found on server {} : code = {}".format(url,u.getcode()))
        u.close()
        return None
    str = u.read()
    u.close()
    return str

def lineIter(s):
    """
    Provides a line iterator for a string.
    @type s: string
    @param s: Multi-line string to iterate over.
    @rtype: iterator
    @return: Line iterator for a string.
    """
    return iter(s.splitlines())

# next works for python 2.7, and is required for python 3.4:
def decode(bytes):
    """
    Decodes a given list of bytes as UTF-8.
    @type bytes: list of bytes
    @rtype: string
    @return: A decoded version of the input bytes.
    """
    return bytes.decode('utf-8')

def dbgprint(debug, s):
    """
    Prints a string if debug boolean is true.
    @type debug: boolean
    @param debug: Flag, true if string should be printed.
    @type s: string
    @param s: String to be printed.
    """
    if debug:
        print(s)

if __name__ == '__main__':
    root = tk.Tk()
    root.attributes('-alpha', 0.0)    
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)    
    frm = tk.Frame(root, bd=4, relief='raised')
    frm.pack(fill='x')    
    lab = tk.Label(frm, text='Hello World!', bd=4, relief='sunken')
    lab.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')    
    center(root)
    txt = getUrlAsString('http://tylasky.com/res/tennisScore/womenSingles.txt')
    if not txt is None:
        for line in lineIter(txt):
            print('Line: '+line)
    root.mainloop()