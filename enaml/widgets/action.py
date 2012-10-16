#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from traits.api import Unicode, Bool

from enaml.core.declarative import Declarative
from enaml.core.trait_types import EnamlEvent


class Action(Declarative):
    """ A non visible widget used in a ToolBar or Menu.

    An Action represents an actionable item in a ToolBar or a Menu.
    Though an Action itself is a non-visible component, it will be
    rendered in an appropriate fashion for the location where it is
    used.

    """
    #: The text label associate with the action.
    text = Unicode

    #: The tool tip text to use for this action. Typically displayed
    #: as a small label when the user hovers over the action.
    tool_tip = Unicode

    #: The text that is displayed in the status bar when the user
    #: hovers over the action.
    status_tip = Unicode

    #: The an icon to display with this action when appropriate, such as
    #: when the action is a member of a menu or a toolbar.
    #icon = Instance(AbstractTkIcon)

    #: Whether or not the action can be checked.
    checkable = Bool(False)

    #: Whether or not the action is checked. This value only has meaning
    #: if 'checkable' is set to True.
    checked = Bool(False)

    #: Whether or not the item representing the action is enabled.
    enabled = Bool(True)

    #: Whether or not the item representing the action is visible.
    visible = Bool(True)

    #: Whether or not the action should be treated as a separator. If
    #: this value is True, none of the other values have meaning.
    separator = Bool(False)

    #: An event fired when the action is triggered by user interaction.
    triggered = EnamlEvent

    #: An event fired when a checkable action changes its checked state.
    toggled = EnamlEvent

    #--------------------------------------------------------------------------
    # Initialization
    #--------------------------------------------------------------------------
    def snapshot(self):
        """ Returns the snapshot dict for the Action.

        """
        snap = super(Action, self).snapshot()
        snap['text'] = self.text
        snap['tool_tip'] = self.tool_tip
        snap['status_tip'] = self.status_tip
        snap['checkable'] = self.checkable
        snap['checked'] = self.checked
        snap['enabled'] = self.enabled
        snap['visible'] = self.visible
        snap['separator'] = self.separator
        return snap

    def bind(self):
        """ Binds the change handlers for the Action.

        """
        super(Action, self).bind()
        attrs = (
            'text', 'tool_tip', 'status_tip', 'checkable', 'checked',
            'enabled', 'visible', 'separator'
        )
        self.publish_attributes(*attrs)

    #--------------------------------------------------------------------------
    # Overrides
    #--------------------------------------------------------------------------
    def validate_children(self, children):
        """ A child validator which rejects all children.

        """
        if children:
            name = type(self).__name__
            msg = 'Cannot add children to component of type `%s`'
            raise ValueError(msg % name)
        return children

    #--------------------------------------------------------------------------
    # Message Handling
    #--------------------------------------------------------------------------
    def on_action_triggered(self, content):
        """ Handle the 'triggered' action from the client widget.

        """
        self.set_guarded(checked=content['checked'])
        self.triggered()

    def on_action_toggled(self, content):
        """ Handle the 'toggled' action from the client widget.

        """
        self.set_guarded(checked=content['checked'])
        self.toggled()

