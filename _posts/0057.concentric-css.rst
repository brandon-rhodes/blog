---
categories: Computing
date: 2011/09/10 02:22:46
permalink: http://rhodesmill.org/brandon/2011/concentric-css/
tags: ''
title: Concentric CSS
---

(My official Concentric CSS “style.css” is in a
`GitHub repository <https://github.com/brandon-rhodes/Concentric-CSS/>`_)

Perhaps my mind is unusually visual,
but I have no idea how people clearly picture the effects of their CSS rules
when following the common advice
to sort their properties alphabetically within each declaration block
(as in the answers to
`this Stack Overflow question <http://stackoverflow.com/questions/4878655/conventional-order-of-css-attributes>`_).

The main alternative to alphabetization seems to be a
`CSS property order that claims to be based on the box model <http://fordinteractive.com/2009/02/order-of-the-day-css-properties/>`_
but which tackles properties in a sadly haphazard order.
It starts with ``display`` and ``position``,
which are a great start,
but these are immediately followed by the ``height`` and ``width`` —
even though these dimensions only apply to the content,
which is nestled down inside the deepest level of the box!
The order then continues to skip around wildly,
jumping outside the box to talk about the margins,
then jumping almost all the way back inside
to talk about the padding.
Finally it gets to the borders,
even though they will actually be sandwiched
*between* the margins and the padding
when rendered by the browser.

For reference, here is the box model
as illustrated in the CSS standard itself:

.. image:: http://www.w3.org/TR/CSS2/images/boxdim.png

The fact that ``width`` and ``height`` apply only to the content,
and not to the padding or anything else,
is a crucial issue in CSS —
an issue that causes newcomers a lot of grief.
For everyone's sanity,
I need the order in which I declare properties
to reflect the structure of the box itself,
with the ``width`` and ``height`` coming after
the decorations that wrap around them.

I call the result **Concentric CSS**
and the basic template looks something like this::

 #!css
 {
     display: ;    /* Where and how the box is placed */
     position: ;
     float: ;
     clear: ;

     visibility: ; /* Can the box be seen? */
     opacity: ;
     z-index: ;

     margin: ;     /* Layers of the box model */
     outline: ;
     border: ;
     background: ;
     padding: ;

     width: ;      /* Content dimensions and scrollbars */
     height: ;
     overflow: ;

     color: ;      /* Text */
     text: ;
     font: ;
 }

Are you surprised that I sandwiched ``background``
between the border and padding instead of saving it until later?
My reasoning is that the ``padding`` is the first part of the box
that actually gets painted with the background color —
I have positioned ``background`` so that everything beneath it
gets the background color, while everything above has its own
color (borders) or is transparent (margins).

I am not certain about my choice
of where to place the ``overflow`` property.
Its current position is dictated by the fact that it is often triggered
by too small a height and width —
so it often serves as a kind of “else clause”
to say what should happen if the height and width
are too constraining, and so the property makes sense next to them.
But one of the consequences of ``overflow`` can be
that scrollbars appear around the box,
and an argument could be made for putting ``overflow``
up between the borders and padding,
because that is exactly the place where
`the standard <http://www.w3.org/TR/CSS2/visufx.html#propdef-overflow>`_
insists that scrollbars be drawn.

For the sake of completeness
I have written up my preferred property order —
with a much more exhaustive list of properties
than in the sketch shown above —
as a
`style.css <https://github.com/brandon-rhodes/Concentric-CSS/blob/master/style.css>`_
file that lives in its own
`GitHub repository <https://github.com/brandon-rhodes/Concentric-CSS/>`_.
I welcome comments and improvements,
especially ones that will make this ordering
an even better reflection of the box model.
I want my CSS to make as much sense as possible
both to the newcomer as well as the seasoned professional!
