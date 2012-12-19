#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod

from enaml.signaling import Signal


class TextInterface(object):
    """ A class which defines a data interface for a TextEditor.

    This is a pure abstract class. It provides enough flexibility that
    implementors are free to choose data structures which suit the task.
    These can be in-memory, on-disk, or a hybrid of the two.

    Line endings will be removed from all input and output to and from
    the interface. Proper handling of line endings is an implementation
    detail for a given use of an interface.

    """
    __metaclass__ = ABCMeta

    #: A signal emitted when characters are inserted into the model. It
    #: carries three arguments: the lineno, the position, and the string
    #: of inserted characters.
    chars_inserted = Signal()

    #: A signal emitted when characters are replaced in the model. It
    #: carries four arguments: the lineno, the position, the string of
    #: removed characters, and the string of inserted characters.
    chars_replaced = Signal()

    #: A signal emitted when characters are removed from the model. It
    #: carries three arguments: the lineno, the position, and the string
    #: of removed characters.
    chars_removed = Signal()

    #: A signal emitted when lines are inserted into the model. It
    #: carries two arguments: the lineno, and the list of inserted lines.
    lines_inserted = Signal()

    #: A signal emitted when lines are replaced in the model. It carries
    #: three arguments: the lineno, the list of removed lines, and the
    #: list of inserted lines.
    lines_replaced = Signal()

    #: A signal emitted when lines are removed from the model. It
    #: carries two aruments: the lineno, and the list of removed lines.
    lines_removed = Signal()

    @abstractmethod
    def __iter__(self):
        """ Get an iterator over the lines in the model.

        Returns
        -------
        result : iterable
            An iterable of all the lines in the model. The lines will
            not have line endings. It is assumed that the model will
            not be modified while this iterator is being consumed.

        """
        raise NotImplementedError

    @abstractmethod
    def line_count(self):
        """ Get the number of lines in the model.

        Returns
        -------
        result : int
            The number of lines in the text model.

        """
        raise NotImplementedError

    @abstractmethod
    def line(self, lineno):
        """ Get the line for the given line number.

        Parameters
        ----------
        int : lineno
            The line number for target line. This is zero based and must
            be less than the line count.

        Returns
        -------
        result : unicode
            The line of text at the given line number.

        """
        raise NotImplementedError

    @abstractmethod
    def insert_chars(self, lineno, position, chars):
        """ Insert characters at the given location.

        This method will emit the `chars_inserted` signal.

        Parameters
        ----------
        lineno : int
            The line number at which to perform the insertion. This is
            zero based and must be less than the line count.

        position : int
            The position in the line at which to insert the characters.
            This is zero based and must be less than or equal to the line
            length.

        chars : unicode
            The text to insert into the line.

        """
        raise NotImplementedError

    @abstractmethod
    def replace_chars(self, lineno, start, end, chars):
        """ Replace characters at the given location.

        This method will emit the `chars_replaced` signal.

        Parameters
        ----------
        lineno : int
            The line number at which to perform the replacement. This is
            zero based and must be less than the line count.

        start : int
            The starting index of the substring to remove, inclusive.

        end : int
            The ending index of the substring to remove, inclusive.

        chars : unicode
            The text to insert into the line at the starting position.

        """
        raise NotImplementedError

    @abstractmethod
    def remove_chars(self, lineno, start, end):
        """ Remove characters at the given location.

        This method will emit the `chars_removed` signal.

        Parameters
        ----------
        lineno : int
            The line number at which to perform the removal. This is
            zero based and must be less than the line count.

        start : int
            The starting index of the substring to remove, inclusive.

        end : int
            The ending index of the substring to remove, inclusive.

        """
        raise NotImplementedError

    @abstractmethod
    def insert_lines(self, lineno, lines):
        """ Insert lines at the given location.

        This method will emit the `lines_inserted` signal.

        Parameters
        ----------
        lineno : int
            The line number at which to insert the lines.

        lines : list
            The list of unicode strings to insert. They must be free of
            line endings.

        """
        raise NotImplementedError

    @abstractmethod
    def replace_lines(self, start, end, lines):
        """ Replace lines at the given location.

        This method will emit the `lines_replaced` signal.

        Parameters
        ----------
        start : int
            The starting line number of the lines to remove, inclusive.

        end : int
            The ending line number of the lines to remove, inclusive.

        lines : list
            The list of unicode strings to insert. They must be free of
            line endings.

        """
        raise NotImplementedError

    @abstractmethod
    def remove_lines(self, start, end):
        """ Remove the lines at the given location.

        This method will emit the `lines_removed` signal.

        Parameters
        ----------
        start : int
            The starting line number of the lines to remove, inclusive.

        end : int
            The ending line number of the lines to remove, inclusive.

        """
        raise NotImplementedError
