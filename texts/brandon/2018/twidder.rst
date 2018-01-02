
====================================
 A Driver for the Original Twiddler
====================================

:Date: 1 January 2018

The practical take-away from this post
is that if you are ever trying to debug serial communications
with a device that — against all tradition —
refuses to transmit when Clear to Send is asserted,
never under any circumstances include an ``stty`` in your shell script
to double-check the terminal settings you have just established.

Why?

Because ``stty`` turns Clear to Send back on without even asking you.

So the device will never communicate with you.
You may very nearly conclude that it is broken
before thinking to remove the ``stty`` call
and finally get things working.

So that’s the take-away.
But the full story is a bit longer.

2pm

Typing with one hand
--------------------

After a recent marathon two-day coding session
left my wrists aching slightly,
I decided to look for an alternative keyboard
for tasks like browsing documentation and catching up on email.
While I will always want the bandwidth of a full two-handed keyboard
when composing text,
I decided to try out my old Twiddler keyboard
since the Gmail shortcuts
should be easy enough to type with one hand.

[pic of Twiddler]

But I disliked the native keyboard mapping,
so I came up with my own mapping that I named “TabSpace”
and that’s [still available from my old projects page](http://rhodesmill.org/brandon/projects.html):

[pic]

It may surprise you
to learn that even though I’m the author
of a custom Twiddler keyboard map renowned for its efficiency,
I never wound up using the Twiddler much.
I bought it in grad school
when I was briefly interested in wearable computing —
back when that meant running Emacs in a glasses-mounted display
powered by a computer in an over-the-shoulder satchel.
I wound up pursuing other avenues
after my workplace issued me a [Palm V](https://en.wikipedia.org/wiki/Palm_V)
and I realized that I preferred a mobile experience
that I could stash away in a pocket
over a device that would be constantly intruding in my line of sight.

So many cables
--------------

So pulling the old Twiddler back out for browsing email
seemed like a great chance to finally use the device.
The first surprise was the reminder that its cables
are quite a bit different from those of a modern keyboard:

[pic of cables]

It took a few tries to remember why it needs two connectors.
Why two?
Their design constraints seem to have been:

* They wanted to support both user-defined keystrokes,
  as well as entirely custom user-defined keymaps.

* But if the Twiddler itself
  had implemented the mapping between typed chords
  and the resulting text,
  then it would have required both onboard RAM —
  making its electronics more expensive and complex —
  as well as an incoming data stream
  over which the custom keymap could be uploaded,
  adding complexity to both the protocol and software.

* They therefore decided that the Twiddler itself
  would only transmit the raw chords that the user pressed,
  and perform the translation from chords to text on the computer.

* This meant that the Twiddler could *not* send its input
  to the PS/2 keyboard port,
  since the operating system would have interpreted the data
  as real keystrokes.

* But which incoming data port were operating systems agnostic about?
  The serial port!
  Desktop operating systems tended to ignore it by default,
  leaving applications without any constraint
  and able to use the port as they pleased.

* The Twiddler might thus have been designed
  purely for the serial port,
  but how would it then have been powered?
  One possibility would have been its own A/C power supply.
  Another would have been a compartment for batteries.
  Instead, the designers instead opted for the same power supply
  as is used by normal keyboards:
  the 

so odd
needs power, so, keyboard
but does not have the processing power onboard
to do keyboard - would need:
RAM; incoming signals; settings (and remembering?)
* needs no RAM
* needs no proc of incoming bits
* needs no state
but where else could it send signals?
serial

Driver archaeology
------------------

4pm

hard to trying to find things from 1990s web
looked at drivers

https://www.media.mit.edu/wearables/lizzy/keyboards.html

“Twiddler driver for Linux v.1.01, for X and console (by Jeff Levine-tarred and gzipped-with thanks to Mark Eichin)”



# prior work: https://github.com/mati75/gpm/blob/master/debian/gpm.templates
# https://manpages.debian.org/jessie/gpm/gpm-types.7.en.html



Establishing communication
--------------------------

5pm

how would I learn? I searched

got old driver running, could strace to see data!

wanted to hook to modern X

could I do it in Python?

serial needs baud, bits, parity

look what it used to do: set baud then go back

* turns out this no longer works - was getting bad data!

* had to find alternative way to set CTR

* stty was resetting it!

only thing that kept me going was driver: I could see it worked!
kept being afraid it was broken

(Conclusion?)
-------------

6pm

yeah.




