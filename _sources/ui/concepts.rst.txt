Concepts and core objects
=========================

.. py:currentmodule:: clubsandwich.ui

The Scene
---------

.. autoclass:: clubsandwich.ui.UIScene
  :members:

Layout
------

.. py:class:: LayoutOptionValue

  Conceptual wrapper type (union) of the possible values for the attributes
  of :py:class:`LayoutOptions`.

  * ``None``: Do not constrain this value.
  * ``'frame'``: Derive a constant from the *initial* frame of this view. This
    initial frame is stored in :py:attr:`View.layout_spec`, so
    if you need to change it, you can just change that attribute.
  * ``0.0-1.0`` left-inclusive: Use a fraction of the superview's size on the
    appropriate axis.
  * ``>=1``: Use a constant integer
  * ``'intrinsic'``: The view defines an ``intrinsic_size`` property; use this
    value. Mostly useful for ``LabelView``.

.. autoclass:: clubsandwich.ui.layout_options.LayoutOptions
  :members:

Views
-----

.. autoclass:: clubsandwich.ui.View

Positioning
~~~~~~~~~~~

.. autoattribute:: clubsandwich.ui.View.bounds

.. autoattribute:: clubsandwich.ui.View.frame

.. autoattribute:: clubsandwich.ui.View.scene

.. autoattribute:: clubsandwich.ui.View.intrinsic_size

View hierarchy
~~~~~~~~~~~~~~

.. autoattribute:: clubsandwich.ui.View.superview

.. automethod:: clubsandwich.ui.View.add_subviews

.. automethod:: clubsandwich.ui.View.remove_subviews

Layout
~~~~~~

.. automethod:: clubsandwich.ui.View.set_needs_layout

.. automethod:: clubsandwich.ui.View.layout_subviews

Drawing
~~~~~~~

.. automethod:: clubsandwich.ui.View.draw

First Responder
~~~~~~~~~~~~~~~

You might want to read about :py:class:`FirstResponderContainerView`
before diving into this section.

.. automethod:: clubsandwich.ui.View.terminal_read

.. autoattribute:: clubsandwich.ui.View.can_become_first_responder

.. automethod:: clubsandwich.ui.View.did_become_first_responder

.. automethod:: clubsandwich.ui.View.descendant_did_become_first_responder

.. autoattribute:: clubsandwich.ui.View.can_resign_first_responder

.. automethod:: clubsandwich.ui.View.did_resign_first_responder

.. automethod:: clubsandwich.ui.View.descendant_did_resign_first_responder

.. autoattribute:: clubsandwich.ui.View.first_responder_container_view

Tree traversal
~~~~~~~~~~~~~~

.. autoattribute:: clubsandwich.ui.View.leftmost_leaf

.. autoattribute:: clubsandwich.ui.View.postorder_traversal

.. autoattribute:: clubsandwich.ui.View.ancestors

.. automethod:: clubsandwich.ui.View.get_ancestor_matching

Debugging
~~~~~~~~~

.. autoattribute:: clubsandwich.ui.View.debug_string

.. automethod:: clubsandwich.ui.View.debug_print

First Responder
---------------

.. autoclass:: clubsandwich.ui.FirstResponderContainerView
  :members: