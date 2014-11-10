#!/usr/bin/python

"""
observable.py

The observable class for tennis scoreboard based on MVC architecture.

Exported classes:

Observable -- Provides an observable object, useful for MVC. 

Credit:

observable.py copied directly from I{http://tkinter.unpythonic.net/wiki/ToyMVC}
with (I believe) no modification. GPL licensed.
"""

class Observable:
    """Provides an observable object, useful for MVC."""
    def __init__(self, initialValue=None):
        """
        @type initialValue: TBD at runtime
        @param initialValue: Initial value for the observable data.
        """
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        """
        Adds callback routine for when data is modified.
        @type func: function
        @param func: Function to execute when data is modified.
        """
        self.callbacks[func] = 1

    def delCallback(self, func):
        """
        Deletes callback routine.
        @type func: function
        @param func: Function to for callback routine to delete.
        """
        del self.callback[func]

    def _docallbacks(self):
        """
        Executes all callback routines.
        """
        for func in self.callbacks:
             func(self.data)

    def set(self, data):
        """
        Updates the observable's data.
        @type data: TBD at runtime
        @param data: Value to set the observable's data to.
        """
        self.data = data
        self._docallbacks()

    def get(self):
        """
        Returns the observable's data.
        @rtype: TBD at runtime
        @return: The observable's data.
        """
        return self.data

    def unset(self):
        """Resets the observable's data to None."""
        self.data = None