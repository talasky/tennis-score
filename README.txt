
tennisScore application

Copyright 2014, Ty A. Lasky

Released under the GNU General Public License 3.0
(See file LICENSE.txt)

version 1.00.01, November 9, 2014

version 1.0, November 8, 2014

Project contact: Ty A. Lasky	<talasky@gmail.com>

Tennis scoreboard based on model, view, controller architecture.
The main program is tennisScore.py, the controller.

Credit:
	For flag images, using the small freeware flag images from http://www.33ff.com/flags/

Credit:
	Women player's images from rankings pages at http://wtatennis.com

Credit:
	Men player's images from rankings pages at http://www.atpworldtour.com

Credit:
	Player lists, rankings, and countries from http://www.tennischannel.com/scores/rankings.aspx

Credit:
    observable.py copied directly from http://tkinter.unpythonic.net/wiki/ToyMVC
    with (I believe) no modification. GPL licensed.

Tested under:
python 2.7.6 in Linux Mint 17, Cinammon, 64-bit
python 3.4.0 in Linux Mint 17, Cinammon, 64-bit
python 2.7.6 in Windows 7, 64-bit
===========================================================================================================
How to Run:

1) First, get the files. You need the files in src, lib, and util

2) Second, if you don't already have it, you need to install Python. You can get it from http://www.python.org

At this point, you're ready to go.

3) Change into directory src

4) Type: "python tennisScore.py"

Hopefully, the rest is self-explanatory!

===========================================================================================================
To generate source code documentation, use (shell script):

./docgen

Must have epydoc and graphviz installed. On Linux, use either:

(a)
sudo apt-get install python-epydoc graphviz

or

(b) (if have installed pip)
sudo apt-get install graphviz
pip install epydoc

===========================================================================================================

To Do in future versions:

* Add at least one level of "undo" for scoring

* Develop a version / skin with a fancier windowing package. Features might include rounded window
  corners, text animations (e.g. between scoring changes). I think some of this can be done in
  tkinter, but probably not with the default install. At which point, it might be better to
  go to a different windowing package.
  
* Read player info directly from the web. No intermediate files, from:
	women singles: http://www.tennischannel.com/scores/rankings.aspx?page=1&tour0=tour2&tab=0
	women doubles: http://www.tennischannel.com/scores/rankings.aspx?page=1&tour1=tour2&tab=1
	men singles:   http://www.tennischannel.com/scores/rankings.aspx?page=1&tour1=tour2&tab=1
	men doubles:   http://www.tennischannel.com/scores/rankings.aspx?page=1&tour1=tour1&tab=1

* Get entire list of players to show in dropdown menus. Right now, on 30" screen, see only 78 playerStrings
	when using optionMenu. This out of 99 players. Only 57 on a 22" monitor. One possibility is to use a
	listMenu and add a scrollbar. But, I don't like the look or the behavior. Don't think can add 
	scrollbar with optionMenu.

* Consider adding caching capability for countries list, and player lists. This must be across executions
in order to be any use. So, some form of disk-based cache. Or, in-memory cache combined with, perhaps,
pickling (cpicle, faster). I envision checking for data on disk (cache), if not there then grabbing data
via http request. If data is in cache, use a header read from the HTTP request to determine the server file
date, and use whichever is more recent. If read from server, update cache. There are some existig caching
modules for Python. But, I want something in the standard library, or built from that.

* Get better alignment of label "Match type" with optionMenu in setup2.py

* Better handling of dual monitors. Right now, centering may split scoreboard across monitors.
This is particularly problematic for monitors with different resolutions.

* See if can get window minimize to work with overrideredirect.
Right now, get an error if I use the minimize button. Also, find
a better symbol for minimize button in tennisView.py. Right now,
using unicode \u02cd. It's a little narrower than I like.

* Create a utility to directly read:
	http://en.wikipedia.org/wiki/List_of_IOC_country_codes
	and generate res/iocCountries.txt
	Alternately, have util/countryUtil.py read directly from that URL, and generate res/countries.txt

* Add a notification mechanism so that developer is alerted
when a player wins a game, but there is no corresponding photo.
This mechanism could be helpful for other notifications.

* In tennisView.View.readCountries maybe do something more
graceful if cannot read country file. Could set a flag, and
then just skip anything subsequent related to countries
(e.g. showing flags). May require distributed changes.

* In tennisScore, instead of hard-coding global specialCaseNames
for special case names (which will change over the years),
could likely set this automatically, at the time check for
duplicate last names. Should be easy change.

* In tennisScore.Controller.startMatch change the way determine
number of sets to win. Right now, only handle three and five-set
matches. Could likely make this very general, and handle
automatically. On the other hand, is there anything except three
and five set matches?

* In tennisModel.Model.messageCheck might want to revise so
default message is more random, e.g. nothing most of time,
match type maybe 25% of time. Currently, default is always
match type. Should be easy change.

* In tennisModel.Model.singular the approach for setting
word to singular or plural is very crude. Could do something
more sophisticated. However, in Version 1.0, it is fine for
the words I'm using.

* In player.fancyFrstInits I am suspicious that there could
be more exotic first names that I do not currently handle.
Right now, I handle spaces and hyphens. Haven't seen anything
that this won't take care of.

* In playerError perhaps there could be other errors for players
besides just duplicate players. Can't think of any now that
would make it through the setup dialogs.

* In util/countryUtil would be better if can read directly from
the wikipedia IOC web site into iocCountries.txt, or straight
to countries.txt

* In util/countryUtil more thorough testing, e.g. for permissions errors.

* In setup3 not handling Unicode characters in player names.
So, currently, replacing these characters in player list text
files. This is a pain, and it also means less rich UI. I
probably know how to handle this, likely fairly easy.
