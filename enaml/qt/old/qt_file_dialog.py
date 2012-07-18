#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import os
from .qt.QtGui import QFileDialog
from .qt_dialog import QtDialog

QT_ACCEPT_MODE = {
    'open' : QFileDialog.AcceptOpen,
    'save' : QFileDialog.AcceptSave
}

class QtFileDialog(QtDialog):
    """ A Qt implementation of a file dialog

    """
    def create(self):
        """ Create the underlying widget

        """
        self.widget = QFileDialog(self.parent_widget)

    def initialize(self, init_attrs):
        """ Initialize the attributes of the file dialog

        """
        super(QtFileDialog, self).initialize(init_attrs)
        self.set_mode(init_attrs.get('mode', 'open'))
        self.set_multi_select(init_attrs.get('multi_select', False))
        self.set_directory(init_attrs.get('directory',
                           os.path.abspath(os.path.curdir)))
        self.set_filename(init_attrs.get('filename',
                          os.path.abspath(__file__)))
        self.set_filters(init_attrs.get('filters', []))
        self.set_selected_filter(init_attrs.get('selected_filter'))
        self.widget.setViewMode(QFileDialog.Detail)



    def bind(self):
        """ Binds the signal handlers for the file dialog.

        """
        super(QtFileDialog, self).bind()
        self.widget.filesSelected.connect(self.on_files_selected)
        self.widget.filterSelected.connect(self.on_filter_selected)

    #--------------------------------------------------------------------------
    # Message Handlers
    #--------------------------------------------------------------------------
    def receive_set_mode(self, ctxt):
        """ Message handler for set_mode

        """
        mode = ctxt.get('mode')
        if mode is not None:
            self.set_mode(mode)

    def receive_set_multi_select(self, ctxt):
        """ Message handler for set_multi_select

        """
        multi_select = ctxt.get('multi_select')
        if multi_select is not None:
            self.set_multi_select(multi_select)

    def receive_set_directory(self, ctxt):
        """ Message handler for set_directory

        """
        directory = ctxt.get('directory')
        if directory is not None:
            self.set_directory(directory)

    def receive_set_filename(self, ctxt):
        """ Message handler for set_filename

        """
        filename = ctxt.get('filename')
        if filename is not None:
            self.set_filename(filename)

    def receive_set_filters(self, ctxt):
        """ Message handler for set_filters

        """
        filters = ctxt.get('filters')
        if filters is not None:
            self.set_filters(filters)

    def receive_set_selected_filter(self, ctxt):
        """ Message handler for set_selected_filter

        """
        selected_filter = ctxt.get('selected_filter')
        if selected_filter is not None:
            self.set_selected_filter(selected_filter)

    #--------------------------------------------------------------------------
    # Event Handlers 
    #--------------------------------------------------------------------------
    def on_files_selected(self, files):
        """ The signal handler for the dialog's `filesSelected` signal.

        """
        first_file = files[0] if files else u''
        directory, filename = os.path.split(first_file)
        self.send({'action':'set_directory', 'directory':directory})
        self.send({'action':'set_filename', 'filename':filename})
        self.send({'action':'set_paths', 'paths':files})

    def on_filter_selected(self, qt_filter):
        """ The signal handler for the dialog's `filterSelected` signal.

        """
        self.send({'action':'set_selected_filter', 'filter':qt_filter})

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_mode(self, mode):
        """ Set the mode of the file dialog

        """
        self.widget.setAcceptMode(QT_ACCEPT_MODE[mode])

    def set_multi_select(self, multi_select):
        """ Set whether the user can select multiple files when in open mode

        """
        if self.widget.acceptMode() == QFileDialog.AcceptSave:
            mode = QFileDialog.AnyFile
        else:
            if multi_select:
                mode = QFileDialog.ExistingFiles
            else:
                mode = QFileDialog.ExistingFile
        self.widget.setFileMode(mode)

    def set_directory(self, directory):
        """ Set the current directory of the file dialog

        """
        self.widget.setDirectory(directory)

    def set_filename(self, filename):
        """ Set the current filename of the file dialog

        """
        self.widget.selectFile(filename)

    def set_filters(self, filters):
        """ Set the list of name filters for the file dialog

        """
        self.widget.setNameFilters(filters)

    def set_selected_filter(self, selected_filter):
        """ Set the selected filter of the file dialog

        """
        self.widget.selectNameFilter(selected_filter)