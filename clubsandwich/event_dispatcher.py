"""
Simple event dispatch system. It works like this::

  class X:
    def __init__(self, name):
      self.name = name

    def on_foo(self, event):
      print("Fire foo on {}".format(name))

  player = dict(id='player')
  a = X('a')
  b = X('b')
  dispatcher = EventDispatcher()
  dispatcher.register_event_type('foo')

  # 'a.on_foo' gets called for all 'foo' events
  dispatcher.add_subscriber(a, 'foo', None)
  # 'b.on_foo' gets called only for events with `entity is player`
  dispatcher.add_subscriber(b, 'foo', player)

  dispatcher.fire('foo', None, None)  # prints 'a'
  dispatcher.fire('foo', player, None)  # prints 'a' and 'b'
"""
from enum import Enum


class Event:
  """
  .. py:attribute:: name

    Event name as registered in :py:meth:`EventDispatcher.register_event_type`

  .. py:attribute:: entity

    Entity associated with this event. May be ``None``.

  .. py:attribute:: data

    Arbitrary data passed to :py:meth:`EventDispatcher.fire`.
  """
  def __init__(self, name, entity, data):
    self.name = name
    self.entity = entity
    self.data = data
    self._is_halted = False
  
  def stop_propagation(self):
    """
    Prevent any more handlers for this event from firing
    """
    self._is_halted = True


class EventDispatcher:
  """
  Collects and calls object methods in response to events.

  For an event ``foo``, your subscriber should have a method ``on_foo()``
  and take one argument, an :py:class:`Event` instance.
  """

  def __init__(self):
    self.handlers = {}
    self._is_halted = False

  def register_event_type(self, name):
    """
    :param str|Enum name: Name of the event. May be a string-valued enum.

    Allow events with the given name to be subscribed to and fired.

    The dispatcher requires you to register events before using them to avoid
    typo-related errors.
    """
    if isinstance(name, Enum):
      name = name.value
    self.handlers[name] = []

  def add_subscriber(self, obj, name, entity):
    """
    :param object obj: Object to be called when the event fires
    :param str|Enum name: Name of the event. May be a string-valued enum.
    :param entity: If ``None``, receive all events regardless of their entity.
                   Otherwise, only receive events whose entity ``is`` this
                   object.

    Store ``(obj, entity)`` as a subscriber for the event *name*. When
    :py:meth:`fire` is called with a pattern that matches ``(obj, entity)``,
    call ``obj.on_[name](Event(name, entity, data))``.

    An event is said to "match" a subscription if the subscription has the same
    event name, and either the subscriber's entity is ``None``, or the
    subscriber's entity ``is`` the event's entity.

    You may subscribe more than once to receive the event multiple times.
    """
    if isinstance(name, Enum):
      name = name.value
    self.handlers[name].append((obj, entity))

  def remove_subscriber(self, obj, name, entity):
    """
    :param object obj: Object that is subscribed
    :param str|Enum name: Name of the event. May be a string-valued enum.
    :param entity: Entity originally subscribed to

    If you subscribed more than once with the same object/entity pair, you will
    need to unsubscribe more than once as well.
    """
    if isinstance(name, Enum):
      name = name.value
    self.handlers[name].remove((obj, entity))

  def fire(self, name, entity, data):
    """
    :param object obj: Object that is subscribed
    :param str|Enum name: Name of the event. May be a string-valued enum.
    :param entity: Entity, or ``None``.
    :param data: Arbitrary data to add to the :py:class:`Event`.

    Call all event handlers for the given *name* + *entity*, and pass *data*.
    """
    if isinstance(name, Enum):
      name = name.value
    method_name = "on_" + name.lower()
    event = Event(name, entity, data)
    for (obj, required_entity) in self.handlers[name]:
      if required_entity is None or entity is required_entity:
        method = getattr(obj, method_name)
        method(event)
      if event._is_halted or self._is_halted:
        break
    self._is_halted = False

  def stop_propagation(self):
    """
    Prevent any more handlers for the active event from firing
    """
    self._is_halted = True
