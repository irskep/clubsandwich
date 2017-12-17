from collections import namedtuple
from numbers import Real


_LayoutOptions = namedtuple(
    '_LayoutOptions',
    ['width', 'height', 'top', 'right', 'bottom', 'left'])


class LayoutOptions(_LayoutOptions):
    """
    :param LayoutOptionValue width: width spec
    :param LayoutOptionValue height: height spec
    :param LayoutOptionValue top: top spec
    :param LayoutOptionValue right: right spec
    :param LayoutOptionValue bottom: bottom spec
    :param LayoutOptionValue left: left spec

    It is possible to define values that conflict. The behavior in these cases
    is undefined.

    .. py:attribute:: width

      A :py:class:`LayoutOptionValue` constraining this view's width (or not).

    .. py:attribute:: height

      A :py:class:`LayoutOptionValue` constraining this view's height (or not).

    .. py:attribute:: top

      A :py:class:`LayoutOptionValue` constraining this view's distance from the
      top of its superview (or not).

    .. py:attribute:: right

      A :py:class:`LayoutOptionValue` constraining this view's distance from the
      right of its superview (or not).

    .. py:attribute:: bottom

      A :py:class:`LayoutOptionValue` constraining this view's distance from the
      bottom of its superview (or not).

    .. py:attribute:: left

      A :py:class:`LayoutOptionValue` constraining this view's distance from the
      left of its superview (or not).
    """

    def __new__(cls, width=None, height=None, top=0, right=0, bottom=0, left=0):
        self = super(LayoutOptions, cls).__new__(
            cls, width, height, top, right, bottom, left)
        return self

    ### Convenience initializers ###

    @classmethod
    def centered(self, width, height):
        """
        Create a :py:class:`LayoutOptions` object that positions the view in the
        center of the superview with a constant width and height.
        """
        return LayoutOptions(
            top=None, bottom=None, left=None, right=None,
            width=width, height=height)

    @classmethod
    def column_left(self, width):
        """
        Create a :py:class:`LayoutOptions` object that positions the view as a
        full-height left column with a constant width.
        """
        return LayoutOptions(
            top=0, bottom=0, left=0, right=None,
            width=width, height=None)

    @classmethod
    def column_right(self, width):
        """
        Create a :py:class:`LayoutOptions` object that positions the view as a
        full-height right column with a constant width.
        """
        return LayoutOptions(
            top=0, bottom=0, left=None, right=0,
            width=width, height=None)

    @classmethod
    def row_top(self, height):
        """
        Create a :py:class:`LayoutOptions` object that positions the view as a
        full-height top row with a constant height.
        """
        return LayoutOptions(
            top=0, bottom=None, left=0, right=0,
            width=None, height=height)

    @classmethod
    def row_bottom(self, height):
        """
        Create a :py:class:`LayoutOptions` object that positions the view as a
        full-height bottom row with a constant height.
        """
        return LayoutOptions(
            top=None, bottom=0, left=0, right=0,
            width=None, height=height)

    ### Convenience modifiers ###

    def with_updates(self, **kwargs):
        """
        Returns a new :py:class:`LayoutOptions` object with the given changes to
        its attributes. For example, here's a view with a constant width, on the
        right side of its superview, with half the height of its superview::

          # "right column, but only half height"
          LayoutOptions.column_right(10).with_updates(bottom=0.5)
        """
        opts = self._asdict()
        opts.update(kwargs)
        return LayoutOptions(**opts)

    ### Semi-internal layout API ###

    def get_type(self, k):
        # Return one of ``{'none', 'frame', 'constant', 'fraction'}``
        val = getattr(self, k)
        if val is None:
            return 'none'
        elif val == 'frame':
            return 'frame'
        elif val == 'intrinsic':
            return 'intrinsic'
        elif isinstance(val, Real):
            if val >= 1:
                return 'constant'
            else:
                return 'fraction'
        else:
            raise ValueError(
                "Unknown type for option {}: {}".format(k, type(k)))

    def get_is_defined(self, k):
        return getattr(self, k) is not None

    def get_debug_string_for_keys(self, keys):
        return ','.join(["{}={}".format(k, self.get_type(k)) for k in keys])

    def get_value(self, k, view):
        if getattr(self, k) is None:
            raise ValueError("Superview isn't relevant to this value")
        elif self.get_type(k) == 'constant':
            return getattr(self, k)
        elif self.get_type(k) == 'intrinsic':
            if k == 'width':
                return view.intrinsic_size.width
            elif k == 'height':
                return view.intrinsic_size.height
            else:
                raise KeyError(
                    "'intrinsic' can only be used with width or height.")
        elif self.get_type(k) == 'frame':
            if k == 'left':
                return view.layout_spec.x
            elif k == 'top':
                return view.layout_spec.y
            elif k == 'right':
                return superview.bounds.width - view.layout_spec.x2
            elif k == 'bottom':
                return superview.bounds.height - view.layout_spec.y2
            elif k == 'width':
                return view.layout_spec.width
            elif k == 'height':
                return view.layout_spec.height
            else:
                raise KeyError("Unknown key:", k)
        elif self.get_type(k) == 'fraction':
            val = getattr(self, k)
            if k in ('left', 'width', 'right'):
                return view.superview.bounds.width * val
            elif k in ('top', 'height', 'bottom'):
                return view.superview.bounds.height * val
            else:
                raise KeyError("Unknown key:", k)
